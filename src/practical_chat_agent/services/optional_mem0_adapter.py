"""T203: Optional Mem0-backed MemoryRetriever adapter (feasibility spike).

This module provides a minimal ``Mem0AdapterRetriever`` that implements the
``MemoryRetriever`` protocol and evaluates whether an external-memory provider
can sit behind the existing retrieval contract.

Spike scope
-----------

- The adapter **degrades safely** to ``status="not_configured"`` when the
  ``mem0`` package is not installed or no API key is provided.
- It does **not** auto-write, index, or mutate memories.
- It does **not** read raw chat transcripts.
- Returned ``MemoryHit`` items carry ``source="external_adapter"``.
- ``MemoryRetrieverResult`` is the public result shape (unchanged).

Why a separate module
---------------------

The adapter is optional spike code that may be removed if Mem0 adoption is
rejected.  Keeping it separate from ``memory_retrieval.py`` avoids coupling
the core local-retrieval path to an experimental external dependency.

"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from practical_chat_agent.core.enums import MemoryType
from practical_chat_agent.core.models import MemoryHit, MemoryRetrieverResult

if TYPE_CHECKING:  # pragma: no cover
    from practical_chat_agent.services.memory_retrieval import MemoryRetriever

_PREFERENCE_HINTS = (
    "likes",
    "loves",
    "prefers",
    "favorite",
    "enjoys",
    "hates",
    "dislikes",
    "allergic",
    "drinks",
    "eats",
)
_RELATIONSHIP_HINTS = (
    "friend",
    "partner",
    "family",
    "colleague",
    "met at",
    "knows",
    "married",
    "dating",
    "boss",
    "classmate",
    "college friend",
)
_REFLECTION_HINTS = (
    "feels",
    "thinks",
    "believes",
    "worries",
    "stressed",
    "anxious",
    "values",
    "cares about",
    "overwhelmed",
    "frustrated",
)

_DEFAULT_MEM0_SCORE = 0.5


def _infer_memory_type(fact: str) -> MemoryType:
    """Heuristic memory-type inference from fact text.

    Mem0 does not categorise memories by type.  This function provides a
    best-effort mapping using keyword heuristics, defaulting to ``FACT``.
    """
    text = fact.casefold()
    if any(h in text for h in _PREFERENCE_HINTS):
        return MemoryType.PREFERENCE
    if any(h in text for h in _RELATIONSHIP_HINTS):
        return MemoryType.RELATIONSHIP
    if any(h in text for h in _REFLECTION_HINTS):
        return MemoryType.REFLECTION
    return MemoryType.FACT


class Mem0AdapterRetriever:
    """Optional Mem0-backed retriever (feasibility spike).

    Implements the ``MemoryRetriever`` protocol.  Degrades to
    ``status="not_configured"`` when:

    - No ``api_key`` is provided.
    - The ``mem0`` package is not installed.
    - Client initialisation fails.

    Does **not** auto-write, index, or mutate memories.  Does **not** read
    raw chat transcripts.

    Parameters
    ----------
    api_key
        Mem0 cloud API key.  If *None* or empty, the adapter reports
        ``not_configured`` on every ``retrieve()`` call.
    _client
        Pre-built Mem0 client **for testing only**.  When provided, the
        lazy import and initialisation are skipped entirely.  This is a
        prototype placeholder documented by the T203 spike task.
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        _client: Any = None,
    ) -> None:
        self._client: Any = None
        self._unavailable_reason: str | None = None

        if _client is not None:
            self._client = _client
            return

        if not api_key or not api_key.strip():
            self._unavailable_reason = "No Mem0 API key configured."
            return

        self._try_init_client(api_key=api_key)

    # -- MemoryRetriever protocol ----------------------------------------

    def retrieve(
        self,
        *,
        contact_id: str,
        query: str | None = None,
        limit: int = 8,
    ) -> MemoryRetrieverResult:
        if self._client is None:
            return MemoryRetrieverResult(
                status="not_configured",
                contact_id=contact_id,
                notes=[self._unavailable_reason or "Mem0 adapter is not configured."],
            )

        try:
            return self._retrieve_from_client(
                contact_id=contact_id,
                query=query,
                limit=limit,
            )
        except Exception as exc:  # noqa: BLE001
            return MemoryRetrieverResult(
                status="error",
                contact_id=contact_id,
                notes=[f"Mem0 retrieval failed: {exc}"],
            )

    # -- Internal helpers ------------------------------------------------

    def _try_init_client(self, *, api_key: str) -> None:
        try:
            from mem0 import Memory  # type: ignore[import-untyped]

            self._client = Memory(api_key=api_key)
        except ImportError:
            self._unavailable_reason = "mem0 package is not installed."
        except Exception as exc:  # noqa: BLE001
            self._unavailable_reason = f"Mem0 client initialisation failed: {exc}"

    def _retrieve_from_client(
        self,
        *,
        contact_id: str,
        query: str | None,
        limit: int,
    ) -> MemoryRetrieverResult:
        if query and query.strip():
            raw_results = self._client.search(
                query=query.strip(),
                user_id=contact_id,
                limit=limit,
            )
        else:
            raw_results = self._client.get_all(user_id=contact_id)

        hits = self._convert_results(raw_results, limit=limit)

        total = len(raw_results) if isinstance(raw_results, list) else len(hits)

        notes: list[str] = [
            f"mem0 adapter: {len(hits)} hits from {total} raw results",
        ]
        if query and query.strip():
            notes.append(f"query: '{query.strip()}'")

        return MemoryRetrieverResult(
            status="success",
            contact_id=contact_id,
            hits=hits,
            candidate_count=total,
            notes=notes,
        )

    @staticmethod
    def _convert_results(
        raw_results: Any,
        *,
        limit: int,
    ) -> list[MemoryHit]:
        if not isinstance(raw_results, list):
            return []

        hits: list[MemoryHit] = []
        for item in raw_results[:limit]:
            if not isinstance(item, dict):
                continue
            memory_id = str(item.get("id") or "").strip()
            fact = str(item.get("memory") or "").strip()
            if not memory_id or not fact:
                continue
            score = _DEFAULT_MEM0_SCORE
            raw_score = item.get("score")
            if raw_score is not None:
                try:
                    score = max(0.0, min(float(raw_score), 1.0))
                except (TypeError, ValueError):
                    pass
            hits.append(
                MemoryHit(
                    memory_id=memory_id,
                    fact=fact,
                    memory_type=_infer_memory_type(fact),
                    score=score,
                    evidence_refs=[f"mem0:{memory_id}"],
                    source="external_adapter",
                ),
            )
        return hits
