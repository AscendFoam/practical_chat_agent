"""Local JSON store for review workspace bundles.

This store persists safe `ReviewWorkspaceBundle` records under a caller-owned
local root. It does not apply decisions, mutate memory/persona stores, call
providers, send messages, or connect to platform/media runtimes.
"""

from __future__ import annotations

from pathlib import Path

from practical_chat_agent.services.review_queue import ReviewCandidateKind
from practical_chat_agent.services.review_workspace import ReviewWorkspaceBundle


class ReviewWorkspaceSnapshotStore:
    """Persist and query safe local review workspace snapshots."""

    def __init__(self, root: Path | str) -> None:
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def save_bundle(
        self,
        bundle: ReviewWorkspaceBundle,
        *,
        file_name: str | None = None,
    ) -> Path:
        path = self._bundle_path(file_name or f"{bundle.bundle_id}.json")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(bundle.model_dump_json(indent=2), encoding="utf-8")
        return path

    def load_bundle(self, bundle_id_or_file_name: str) -> ReviewWorkspaceBundle:
        path = self._bundle_path(_json_file_name(bundle_id_or_file_name))
        return ReviewWorkspaceBundle.model_validate_json(path.read_text(encoding="utf-8"))

    def list_bundles(self) -> list[ReviewWorkspaceBundle]:
        bundles = [
            ReviewWorkspaceBundle.model_validate_json(path.read_text(encoding="utf-8"))
            for path in self.root.glob("*.json")
            if path.is_file()
        ]
        return sorted(bundles, key=lambda bundle: (bundle.created_at, bundle.bundle_id))

    def filter_bundles(
        self,
        *,
        candidate_kind: ReviewCandidateKind | None = None,
        owner_user_id: str | None = None,
        persona_id: str | None = None,
        priority_band: str | None = None,
        has_blockers: bool | None = None,
    ) -> list[ReviewWorkspaceBundle]:
        bundles = self.list_bundles()
        return [
            bundle
            for bundle in bundles
            if _matches_candidate_kind(bundle, candidate_kind)
            and _matches_owner_user_id(bundle, owner_user_id)
            and _matches_persona_id(bundle, persona_id)
            and _matches_priority_band(bundle, priority_band)
            and _matches_blocker_state(bundle, has_blockers)
        ]

    def _bundle_path(self, file_name: str) -> Path:
        if Path(file_name).is_absolute():
            raise ValueError("review workspace snapshot path must be relative to store root")
        candidate = (self.root / file_name).resolve()
        if not candidate.is_relative_to(self.root):
            raise ValueError("review workspace snapshot path escapes store root")
        if candidate.suffix != ".json":
            raise ValueError("review workspace snapshot files must use .json")
        return candidate


def _json_file_name(bundle_id_or_file_name: str) -> str:
    return bundle_id_or_file_name if bundle_id_or_file_name.endswith(".json") else f"{bundle_id_or_file_name}.json"


def _matches_candidate_kind(
    bundle: ReviewWorkspaceBundle,
    candidate_kind: ReviewCandidateKind | None,
) -> bool:
    if candidate_kind is None:
        return True
    return any(binding.candidate_kind == candidate_kind for binding in bundle.candidate_bindings)


def _matches_owner_user_id(bundle: ReviewWorkspaceBundle, owner_user_id: str | None) -> bool:
    if owner_user_id is None:
        return True
    return any(binding.owner_user_id == owner_user_id for binding in bundle.candidate_bindings)


def _matches_persona_id(bundle: ReviewWorkspaceBundle, persona_id: str | None) -> bool:
    if persona_id is None:
        return True
    return any(binding.persona_id == persona_id for binding in bundle.candidate_bindings)


def _matches_priority_band(bundle: ReviewWorkspaceBundle, priority_band: str | None) -> bool:
    if priority_band is None:
        return True
    return any(binding.priority_band == priority_band for binding in bundle.candidate_bindings)


def _matches_blocker_state(
    bundle: ReviewWorkspaceBundle,
    has_blockers: bool | None,
) -> bool:
    if has_blockers is None:
        return True
    return bool(bundle.blocking_issue_codes) is has_blockers
