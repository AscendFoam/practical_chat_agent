from __future__ import annotations

from collections import defaultdict

from practical_chat_agent.core.enums import MemoryType
from practical_chat_agent.core.models import (
    MemoryConsolidationResult,
    MemoryDuplicateGroup,
    MemoryFact,
    MemoryProfileFacet,
    MemoryProfileRecord,
    MemoryReviewResult,
    utc_now,
)
from practical_chat_agent.services.memory_utils import (
    is_duplicate_memory_fact,
    memory_fact_similarity,
    merge_memory_fact_text,
)
from practical_chat_agent.storage.repositories.base import MemoryRepository


class MemoryLifecycleService:
    """Review, facet-cluster, and consolidate long-term memory records."""

    def __init__(
        self,
        *,
        memory_repository: MemoryRepository,
        similarity_threshold: float = 0.82,
        facet_similarity_threshold: float = 0.66,
    ) -> None:
        self.memory_repository = memory_repository
        self.similarity_threshold = max(0.0, min(float(similarity_threshold), 1.0))
        self.facet_similarity_threshold = max(0.0, min(float(facet_similarity_threshold), 1.0))

    def list_memories(
        self,
        *,
        agent_id: str,
        user_id: str | None = None,
        limit: int = 100,
    ) -> list[MemoryFact]:
        return self.memory_repository.list_for_agent(
            agent_id=agent_id,
            user_id=user_id,
            limit=limit,
        )

    def get_latest_profile_snapshot(
        self,
        *,
        agent_id: str,
        user_id: str,
    ) -> MemoryProfileRecord | None:
        return self.memory_repository.get_latest_profile_snapshot(agent_id=agent_id, user_id=user_id)

    def list_profile_snapshots(
        self,
        *,
        agent_id: str,
        user_id: str,
        limit: int = 20,
    ) -> list[MemoryProfileRecord]:
        return self.memory_repository.list_profile_snapshots(
            agent_id=agent_id,
            user_id=user_id,
            limit=limit,
        )

    def review(
        self,
        *,
        agent_id: str,
        user_id: str | None = None,
        limit: int = 200,
    ) -> MemoryReviewResult:
        memories = self.list_memories(agent_id=agent_id, user_id=user_id, limit=limit)
        profile_snapshot = self._resolve_profile_snapshot(agent_id=agent_id, user_id=user_id, memories=memories)
        duplicate_groups = self._find_duplicate_groups(memories, profile_snapshot=profile_snapshot)
        notes: list[str] = []
        if not memories:
            notes.append("No memories were found for the requested scope.")
        if profile_snapshot is not None:
            notes.append(
                f"Using latest profile snapshot {profile_snapshot.profile_id} with "
                f"{len(profile_snapshot.snapshot.facets)} facets.",
            )
        if memories and not duplicate_groups:
            notes.append("No likely duplicate groups were detected.")
        return MemoryReviewResult(
            agent_id=agent_id,
            user_id=user_id,
            memory_count=len(memories),
            duplicate_group_count=len(duplicate_groups),
            duplicate_groups=duplicate_groups,
            profile_snapshot=profile_snapshot,
            notes=notes,
        )

    def consolidate(
        self,
        *,
        agent_id: str,
        user_id: str | None = None,
        limit: int = 200,
        dry_run: bool = True,
    ) -> MemoryConsolidationResult:
        memories = self.list_memories(agent_id=agent_id, user_id=user_id, limit=limit)
        profile_snapshot = self._resolve_profile_snapshot(agent_id=agent_id, user_id=user_id, memories=memories)
        duplicate_groups = self._find_duplicate_groups(memories, profile_snapshot=profile_snapshot)
        updated_memories: list[MemoryFact] = []
        deleted_memory_ids: list[str] = []

        for group in duplicate_groups:
            canonical = self._select_canonical_memory(group=group, memories=memories)
            if canonical is None:
                continue
            merged = self._merge_group(
                group=group,
                canonical=canonical,
                memories=memories,
                facet=self._resolve_group_facet(
                    [memory for memory in memories if memory.memory_id in set(group.memory_ids)],
                    facet_map=self._map_memory_facets(profile_snapshot),
                ),
            )
            updated_memories.append(merged)
            deleted_memory_ids.extend(memory_id for memory_id in group.memory_ids if memory_id != merged.memory_id)

        if not dry_run:
            for memory in updated_memories:
                self.memory_repository.upsert(memory)
            for memory_id in deleted_memory_ids:
                self.memory_repository.delete(memory_id)

        notes: list[str] = []
        if profile_snapshot is not None:
            notes.append(
                f"Facet-guided consolidation used snapshot {profile_snapshot.profile_id} "
                f"with {len(profile_snapshot.snapshot.facets)} facets.",
            )
        if not duplicate_groups:
            notes.append("No duplicate groups required consolidation.")
        elif dry_run:
            notes.append("Dry-run mode enabled. No database rows were modified.")
        else:
            notes.append("Duplicate groups were consolidated into canonical memories.")

        return MemoryConsolidationResult(
            agent_id=agent_id,
            user_id=user_id,
            reviewed_count=len(memories),
            merged_group_count=len(updated_memories),
            dry_run=dry_run,
            updated_memories=updated_memories,
            deleted_memory_ids=deleted_memory_ids,
            duplicate_groups=duplicate_groups,
            profile_snapshot=profile_snapshot,
            notes=notes,
        )

    def _resolve_profile_snapshot(
        self,
        *,
        agent_id: str,
        user_id: str | None,
        memories: list[MemoryFact],
    ) -> MemoryProfileRecord | None:
        resolved_user_id = user_id
        if resolved_user_id is None:
            unique_user_ids = {memory.user_id for memory in memories}
            if len(unique_user_ids) != 1:
                return None
            resolved_user_id = next(iter(unique_user_ids))
        return self.memory_repository.get_latest_profile_snapshot(
            agent_id=agent_id,
            user_id=resolved_user_id,
        )

    def _find_duplicate_groups(
        self,
        memories: list[MemoryFact],
        *,
        profile_snapshot: MemoryProfileRecord | None,
    ) -> list[MemoryDuplicateGroup]:
        grouped: dict[tuple[str, str], list[MemoryFact]] = defaultdict(list)
        for memory in memories:
            grouped[(memory.user_id, memory.memory_type.value)].append(memory)

        facet_map = self._map_memory_facets(profile_snapshot)
        duplicate_groups: list[MemoryDuplicateGroup] = []
        for (user_id, _memory_type), items in grouped.items():
            clusters = self._cluster_memories(items, facet_map=facet_map)
            for cluster in clusters:
                if len(cluster) <= 1:
                    continue
                canonical = max(
                    cluster,
                    key=lambda item: (item.salience, item.confidence, item.updated_at, item.created_at),
                )
                baseline_merge_preview = self._build_baseline_merge_preview(
                    canonical=canonical,
                    group_memories=cluster,
                )
                similarity_score = min(
                    memory_fact_similarity(canonical.fact, item.fact)
                    for item in cluster
                )
                facet = self._resolve_group_facet(cluster, facet_map=facet_map)
                canonicalization = self._preview_group_canonicalization(
                    canonical=canonical,
                    group_memories=cluster,
                    facet=facet,
                    similarity_score=similarity_score,
                )
                duplicate_groups.append(
                    MemoryDuplicateGroup(
                        user_id=user_id,
                        memory_type=canonical.memory_type,
                        canonical_memory_id=canonical.memory_id,
                        canonical_fact=canonical.fact,
                        memory_ids=[item.memory_id for item in cluster],
                        facts=[item.fact for item in cluster],
                        merged_fact_preview=canonicalization["merged_fact_preview"],
                        baseline_merge_preview=baseline_merge_preview,
                        similarity_score=similarity_score,
                        facet_family_key=self._facet_family_key(facet),
                        facet_title=facet.title if facet is not None else None,
                        facet_summary=facet.summary if facet is not None else None,
                        facet_confidence=facet.confidence if facet is not None else None,
                        canonicalization_strategy=canonicalization["strategy"],
                        canonicalization_reason=canonicalization["reason"],
                    ),
                )
        duplicate_groups.sort(
            key=lambda group: (
                group.user_id,
                group.memory_type.value,
                (group.facet_family_key or "").casefold(),
                group.canonical_fact.casefold(),
            ),
        )
        return duplicate_groups

    def _cluster_memories(
        self,
        memories: list[MemoryFact],
        *,
        facet_map: dict[str, list[MemoryProfileFacet]],
    ) -> list[list[MemoryFact]]:
        clusters: list[list[MemoryFact]] = []
        consumed: set[str] = set()
        for seed in memories:
            if seed.memory_id in consumed:
                continue
            cluster = [seed]
            consumed.add(seed.memory_id)
            seed_facets = facet_map.get(seed.memory_id, [])
            for candidate in memories:
                if candidate.memory_id in consumed:
                    continue
                if self._should_group_memories(seed, candidate, seed_facets=seed_facets, facet_map=facet_map):
                    cluster.append(candidate)
                    consumed.add(candidate.memory_id)
            clusters.append(cluster)
        return clusters

    def _should_group_memories(
        self,
        seed: MemoryFact,
        candidate: MemoryFact,
        *,
        seed_facets: list[MemoryProfileFacet],
        facet_map: dict[str, list[MemoryProfileFacet]],
    ) -> bool:
        if is_duplicate_memory_fact(
            seed.fact,
            candidate.fact,
            similarity_threshold=self.similarity_threshold,
        ):
            return True
        candidate_facets = facet_map.get(candidate.memory_id, [])
        shared_facet = self._shared_facet(seed_facets, candidate_facets)
        if shared_facet is None:
            return False
        similarity = memory_fact_similarity(seed.fact, candidate.fact)
        if similarity >= self.facet_similarity_threshold:
            return True
        if seed.memory_type == candidate.memory_type and seed.memory_type in {
            MemoryType.REFLECTION,
            MemoryType.PREFERENCE,
            MemoryType.RELATIONSHIP,
        }:
            return similarity >= max(self.facet_similarity_threshold - 0.12, 0.48)
        return similarity >= max(self.facet_similarity_threshold - 0.08, 0.5)

    @staticmethod
    def _shared_facet(
        left_facets: list[MemoryProfileFacet],
        right_facets: list[MemoryProfileFacet],
    ) -> MemoryProfileFacet | None:
        if not left_facets or not right_facets:
            return None
        right_keys = {MemoryLifecycleService._facet_family_key(facet) for facet in right_facets}
        for facet in left_facets:
            if MemoryLifecycleService._facet_family_key(facet) in right_keys:
                return facet
        for left in left_facets:
            left_tags = {tag.casefold() for tag in left.tags}
            left_title_key = left.title.casefold()
            left_summary_key = left.summary.casefold()
            for right in right_facets:
                if left.facet_type != right.facet_type:
                    continue
                right_tags = {tag.casefold() for tag in right.tags}
                if left_tags and right_tags and len(left_tags & right_tags) >= 2:
                    return left if left.confidence >= right.confidence else right
                if memory_fact_similarity(left_title_key, right.title.casefold()) >= 0.72:
                    return left if left.confidence >= right.confidence else right
                if memory_fact_similarity(left_summary_key, right.summary.casefold()) >= 0.72:
                    return left if left.confidence >= right.confidence else right
        return None

    @staticmethod
    def _resolve_group_facet(
        memories: list[MemoryFact],
        *,
        facet_map: dict[str, list[MemoryProfileFacet]],
    ) -> MemoryProfileFacet | None:
        counts: dict[str, tuple[int, MemoryProfileFacet]] = {}
        for memory in memories:
            for facet in facet_map.get(memory.memory_id, []):
                key = MemoryLifecycleService._facet_family_key(facet)
                seen_count, _ = counts.get(key, (0, facet))
                counts[key] = (seen_count + 1, facet)
        if not counts:
            return None
        return max(
            counts.values(),
            key=lambda item: (item[0], item[1].confidence, len(item[1].evidence_memory_ids)),
        )[1]

    @staticmethod
    def _map_memory_facets(profile_snapshot: MemoryProfileRecord | None) -> dict[str, list[MemoryProfileFacet]]:
        mapping: dict[str, list[MemoryProfileFacet]] = defaultdict(list)
        if profile_snapshot is None:
            return mapping
        for facet in profile_snapshot.snapshot.facets:
            for memory_id in facet.evidence_memory_ids:
                mapping[memory_id].append(facet)
        return mapping

    @staticmethod
    def _facet_family_key(facet: MemoryProfileFacet | None) -> str:
        if facet is None:
            return ""
        return f"{facet.facet_type}:{facet.title}".casefold()

    @staticmethod
    def _select_canonical_memory(
        *,
        group: MemoryDuplicateGroup,
        memories: list[MemoryFact],
    ) -> MemoryFact | None:
        by_id = {memory.memory_id: memory for memory in memories}
        if group.canonical_memory_id:
            return by_id.get(group.canonical_memory_id)
        return next((by_id[memory_id] for memory_id in group.memory_ids if memory_id in by_id), None)

    def _merge_group(
        self,
        *,
        group: MemoryDuplicateGroup,
        canonical: MemoryFact,
        memories: list[MemoryFact],
        facet: MemoryProfileFacet | None,
    ) -> MemoryFact:
        by_id = {memory.memory_id: memory for memory in memories}
        group_memories = [by_id[memory_id] for memory_id in group.memory_ids if memory_id in by_id]
        canonicalization = self._preview_group_canonicalization(
            group=group,
            canonical=canonical,
            group_memories=group_memories,
            facet=facet,
            similarity_score=group.similarity_score,
        )
        merged_fact = canonicalization["merged_fact_preview"]
        evidence_refs: list[str] = []
        for item in group_memories:
            for ref in item.evidence_refs:
                if ref not in evidence_refs:
                    evidence_refs.append(ref)
        return canonical.model_copy(
            update={
                "fact": merged_fact,
                "salience": max(item.salience for item in group_memories),
                "confidence": max(item.confidence for item in group_memories),
                "evidence_refs": evidence_refs,
                "updated_at": utc_now(),
            },
        )

    def _preview_group_canonicalization(
        self,
        *,
        canonical: MemoryFact,
        group_memories: list[MemoryFact],
        facet: MemoryProfileFacet | None,
        similarity_score: float,
        group: MemoryDuplicateGroup | None = None,
    ) -> dict[str, str | None]:
        baseline_merge_preview = self._build_baseline_merge_preview(
            canonical=canonical,
            group_memories=group_memories,
        )
        if (
            facet is not None
            and facet.summary
            and canonical.memory_type in {MemoryType.REFLECTION, MemoryType.PREFERENCE, MemoryType.RELATIONSHIP}
            and (
                similarity_score < self.similarity_threshold
                or len(group_memories) >= 3
            )
        ):
            reason_parts = [
                "facet summary chosen as a more stable persona statement",
                f"similarity={similarity_score:.2f}",
                f"group_size={len(group_memories)}",
            ]
            if similarity_score < self.similarity_threshold:
                reason_parts.append(
                    f"below_direct_merge_threshold={self.similarity_threshold:.2f}",
                )
            if len(group_memories) >= 3:
                reason_parts.append("three_or_more_related_memories_detected")
            if facet.title:
                reason_parts.append(f"facet={facet.title}")
            return {
                "merged_fact_preview": facet.summary,
                "strategy": "facet_summary",
                "reason": "; ".join(reason_parts),
                "baseline_merge_preview": baseline_merge_preview,
            }
        reason = (
            "direct merge preview selected because duplicate facts are already close enough"
            f" (similarity={similarity_score:.2f}, group_size={len(group_memories)})"
        )
        return {
            "merged_fact_preview": baseline_merge_preview,
            "strategy": "direct_merge",
            "reason": reason,
            "baseline_merge_preview": baseline_merge_preview,
        }

    @staticmethod
    def _build_baseline_merge_preview(
        *,
        canonical: MemoryFact,
        group_memories: list[MemoryFact],
    ) -> str:
        merged_fact = canonical.fact
        for item in group_memories:
            merged_fact = merge_memory_fact_text(merged_fact, item.fact)
        return merged_fact
