"""Memory retrieval packaging with reviewable explanation traces.

This service is deterministic and record-only. It does not rank search
results, mutate stores, generate replies, call providers, send messages, or
connect to media/platform delivery.
"""

from __future__ import annotations

from collections.abc import Iterable

from pydantic import BaseModel, ConfigDict

from practical_chat_agent.core.models import (
    MemoryEvent,
    MemoryRetrievalBundle,
    MemoryRetrievalBundleItem,
    MemoryRetrievalContext,
    MemoryRetrievalPurpose,
)
from practical_chat_agent.services.memory_governance import (
    MemoryContradictionCandidate,
    MemoryDeletionCascadePlan,
    MemoryExplanationTrace,
    MemorySupersessionCandidate,
    PersonaGrowthEvidenceBundle,
)
from practical_chat_agent.services.synthetic_distillation_input import (
    DeidentifiedStyleFeatureCandidate,
)


_PURPOSE_CONTEXT: dict[MemoryRetrievalPurpose, MemoryRetrievalContext | None] = {
    "factual_response": "factual",
    "inferred_context": "inferred",
    "relationship_context": "relational",
    "procedural_context": "procedural",
    "imagined_context": "imagined",
    "review_surface": None,
}

_EVENT_CONTEXT: dict[str, MemoryRetrievalContext] = {
    "factual": "factual",
    "inferred": "inferred",
    "relational": "relational",
    "procedural": "procedural",
    "imagined": "imagined",
}

_EXCLUDED_LIFECYCLE_STATES = frozenset({"deleted", "frozen", "archived", "superseded"})


class MemoryRetrievalExplanationResult(BaseModel):
    """Reviewable output for retrieval bundles and their inclusion traces."""

    model_config = ConfigDict(extra="forbid")

    schema_version: str = "memory_retrieval_explanation_result_v1"
    bundle: MemoryRetrievalBundle
    explanation_traces: list[MemoryExplanationTrace]
    deletion_cascade_plan: MemoryDeletionCascadePlan | None = None

    def trace_by_memory_id(self, memory_id: str) -> MemoryExplanationTrace:
        for trace in self.explanation_traces:
            if trace.memory_id == memory_id:
                return trace
        raise KeyError(memory_id)


class MemoryRetrievalExplanationService:
    """Build retrieval bundles and companion governance candidates."""

    def build_bundle(
        self,
        events: Iterable[MemoryEvent],
        *,
        purpose: MemoryRetrievalPurpose,
        query_summary: str,
        withdrawn_memory_ids: set[str] | list[str] | tuple[str, ...] | None = None,
        include_review_required: bool = False,
    ) -> MemoryRetrievalExplanationResult:
        event_list = list(events)
        withdrawn_ids = set(withdrawn_memory_ids or [])
        items: list[MemoryRetrievalBundleItem] = []
        excluded_memory_ids: list[str] = []
        exclusion_reasons: dict[str, str] = {}
        traces: list[MemoryExplanationTrace] = []
        warnings: list[str] = []

        for event in event_list:
            context = self._retrieval_context_for(event, purpose)
            exclusion_reason, trace_warnings = self._exclusion_reason(
                event,
                purpose=purpose,
                context=context,
                withdrawn_ids=withdrawn_ids,
                include_review_required=include_review_required,
            )
            if exclusion_reason:
                excluded_memory_ids.append(event.event_id)
                exclusion_reasons[event.event_id] = exclusion_reason
                warnings.extend(trace_warnings)
                traces.append(
                    MemoryExplanationTrace.excluded_from_event(
                        event,
                        surface="retrieval_bundle",
                        reason=exclusion_reason,
                        safety_warnings=trace_warnings,
                    )
                )
                continue

            items.append(MemoryRetrievalBundleItem.from_event(event, retrieval_context=context))
            traces.append(
                MemoryExplanationTrace.included_from_event(
                    event,
                    surface="retrieval_bundle",
                    reason=f"included_for_{purpose}",
                )
            )

        bundle = MemoryRetrievalBundle(
            purpose=purpose,
            query_summary=query_summary,
            items=items,
            excluded_memory_ids=excluded_memory_ids,
            exclusion_reasons=exclusion_reasons,
            safety_warnings=_ordered_unique(warnings),
            include_review_required=include_review_required,
        )
        deletion_plan = self._deletion_cascade_plan(
            events=event_list,
            withdrawn_ids=withdrawn_ids,
            bundle_id=bundle.bundle_id,
        )
        return MemoryRetrievalExplanationResult(
            bundle=bundle,
            explanation_traces=traces,
            deletion_cascade_plan=deletion_plan,
        )

    def create_contradiction_candidate(
        self,
        events: Iterable[MemoryEvent],
        *,
        safe_summary: str,
    ) -> MemoryContradictionCandidate:
        return MemoryContradictionCandidate.from_events(
            list(events),
            conflict_type="preference_change",
            safe_summary=safe_summary,
            proposed_resolution="request_clarification",
            safety_warnings=["needs_user_confirmation"],
        )

    def create_supersession_candidate(
        self,
        *,
        source_memory_id: str,
        replacement_memory_id: str,
        reason: str,
    ) -> MemorySupersessionCandidate:
        return MemorySupersessionCandidate.from_memory_ids(
            source_memory_id=source_memory_id,
            replacement_memory_id=replacement_memory_id,
            reason=reason,
        )

    def prepare_persona_growth_evidence(
        self,
        *,
        persona_id: str,
        events: Iterable[MemoryEvent],
    ) -> PersonaGrowthEvidenceBundle:
        return PersonaGrowthEvidenceBundle.from_events(
            persona_id=persona_id,
            events=list(events),
            evidence_purpose="factual_persona_growth",
        )

    def is_distillation_feature_review_only(
        self,
        feature: DeidentifiedStyleFeatureCandidate,
    ) -> bool:
        return (
            feature.review_required
            and not feature.source_text_retained
            and not feature.blocked_from_persona_synthesis
        )

    def _retrieval_context_for(
        self,
        event: MemoryEvent,
        purpose: MemoryRetrievalPurpose,
    ) -> MemoryRetrievalContext:
        context = _PURPOSE_CONTEXT[purpose]
        if context is not None:
            return context
        return _EVENT_CONTEXT[event.event_type]

    def _exclusion_reason(
        self,
        event: MemoryEvent,
        *,
        purpose: MemoryRetrievalPurpose,
        context: MemoryRetrievalContext,
        withdrawn_ids: set[str],
        include_review_required: bool,
    ) -> tuple[str | None, list[str]]:
        if event.event_id in withdrawn_ids:
            return "withdrawn_consent", ["withdrawn_consent"]
        if purpose == "factual_response" and event.event_type == "imagined":
            return "imagined_memory_excluded_from_factual_response", ["imagined_memory"]
        if event.lifecycle_state in _EXCLUDED_LIFECYCLE_STATES:
            return f"{event.lifecycle_state}_memory_excluded", [event.lifecycle_state]
        if event.retrieval_permission.review_required and not include_review_required:
            return "review_required_memory_excluded", ["review_required"]
        if not self._is_route_allowed(event, context, include_review_required=include_review_required):
            return "retrieval_permission_excluded", ["retrieval_permission"]
        return None, []

    def _is_route_allowed(
        self,
        event: MemoryEvent,
        context: MemoryRetrievalContext,
        *,
        include_review_required: bool,
    ) -> bool:
        if event.retrieval_permission.review_required and include_review_required:
            if context == "factual":
                return event.retrieval_permission.allow_factual_retrieval
            if context == "inferred":
                return event.retrieval_permission.allow_inferred_retrieval
            if context == "relational":
                return event.retrieval_permission.allow_relational_retrieval
            if context == "procedural":
                return event.retrieval_permission.allow_procedural_retrieval
            return event.retrieval_permission.allow_imagined_retrieval
        return event.is_retrieval_eligible(context)

    def _deletion_cascade_plan(
        self,
        *,
        events: list[MemoryEvent],
        withdrawn_ids: set[str],
        bundle_id: str,
    ) -> MemoryDeletionCascadePlan | None:
        target_ids = [event.event_id for event in events if event.event_id in withdrawn_ids]
        if not target_ids:
            return None
        user_id = next((event.user_id for event in events if event.event_id in withdrawn_ids), "user_synthetic")
        return MemoryDeletionCascadePlan.for_consent_withdrawal(
            user_id=user_id,
            target_memory_ids=target_ids,
            affected_artifact_refs=[f"retrieval_bundle:{bundle_id}"],
        )


def _ordered_unique(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result
