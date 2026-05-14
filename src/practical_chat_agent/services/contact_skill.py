from __future__ import annotations

from practical_chat_agent.core.models import ChunkSummary, MemoryFactCandidate


def summarize_distillation_inputs(
    *,
    chunk_summary_count: int,
    memory_fact_count: int,
) -> str:
    """Return a tiny status string for downstream ContactSkill work."""

    return (
        f"distillation_inputs_ready:"
        f" chunk_summaries={chunk_summary_count}"
        f" memory_facts={memory_fact_count}"
    )


def collect_source_refs(
    *,
    chunk_summaries: list[ChunkSummary],
    memory_facts: list[MemoryFactCandidate],
) -> list[str]:
    """Collect unique refs for future ContactSkill review assembly."""

    refs: list[str] = []
    seen: set[str] = set()
    for summary in chunk_summaries:
        for ref in summary.evidence_refs:
            if ref not in seen:
                seen.add(ref)
                refs.append(ref)
    for fact in memory_facts:
        for ref in fact.evidence_refs:
            if ref not in seen:
                seen.add(ref)
                refs.append(ref)
    return refs
