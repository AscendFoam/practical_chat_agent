from __future__ import annotations

import re
from difflib import SequenceMatcher

_PREFIX_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"^user (shared|recently said|mentioned):\s*", re.IGNORECASE), "User shared"),
    (re.compile(r"^user preference:\s*", re.IGNORECASE), "User preference"),
    (re.compile(r"^user interest:\s*", re.IGNORECASE), "User preference"),
    (re.compile(r"^user favorite [^:]+:\s*", re.IGNORECASE), "User preference"),
    (re.compile(r"^user fact:\s*", re.IGNORECASE), "User fact"),
    (re.compile(r"^user relationship detail:\s*", re.IGNORECASE), "User relationship detail"),
    (re.compile(r"^user close relationship:\s*", re.IGNORECASE), "User relationship detail"),
    (re.compile(r"^user relationship reflection:\s*", re.IGNORECASE), "User relationship detail"),
    (re.compile(r"^user reflection:\s*", re.IGNORECASE), "User reflection"),
    (re.compile(r"^user emotional reflection:\s*", re.IGNORECASE), "User reflection"),
    (re.compile(r"^user concern:\s*", re.IGNORECASE), "User reflection"),
    (re.compile(r"^user positive anticipation:\s*", re.IGNORECASE), "User reflection"),
    (re.compile(r"^user stress point:\s*", re.IGNORECASE), "User reflection"),
    (re.compile(r"^user value reflection:\s*", re.IGNORECASE), "User reflection"),
)

_LABEL_PRIORITY = {
    "User relationship detail": 5,
    "User preference": 5,
    "User fact": 4,
    "User reflection": 4,
    "User shared": 2,
}


def clean_memory_fact_text(text: str | None) -> str:
    return " ".join((text or "").split()).strip()


def split_memory_fact(text: str | None) -> tuple[str | None, str]:
    cleaned = clean_memory_fact_text(text)
    if not cleaned:
        return None, ""
    for pattern, label in _PREFIX_PATTERNS:
        match = pattern.match(cleaned)
        if match is not None:
            body = cleaned[match.end() :].strip(" .,!?:;，。！？；：")
            return label, body
    return None, cleaned


def render_memory_fact(label: str | None, body: str | None) -> str:
    cleaned_body = clean_memory_fact_text(body).strip(" .,!?:;，。！？；：")
    if not cleaned_body:
        return ""
    if label:
        return f"{label}: {cleaned_body}"
    return cleaned_body


def memory_fact_similarity_key(text: str | None) -> str:
    _label, body = split_memory_fact(text)
    candidate = body or clean_memory_fact_text(text)
    normalized = re.sub(r"[^\w\u4e00-\u9fff ]+", "", candidate.casefold())
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def memory_fact_similarity(left: str | None, right: str | None) -> float:
    left_key = memory_fact_similarity_key(left)
    right_key = memory_fact_similarity_key(right)
    if not left_key or not right_key:
        return 0.0
    if left_key == right_key:
        return 1.0
    return SequenceMatcher(None, left_key, right_key).ratio()


def is_duplicate_memory_fact(
    left: str | None,
    right: str | None,
    *,
    similarity_threshold: float = 0.82,
) -> bool:
    left_key = memory_fact_similarity_key(left)
    right_key = memory_fact_similarity_key(right)
    if not left_key or not right_key:
        return False
    if left_key == right_key:
        return True
    if left_key in right_key or right_key in left_key:
        return True
    return memory_fact_similarity(left, right) >= similarity_threshold


def merge_memory_fact_text(
    existing_fact: str | None,
    new_fact: str | None,
    *,
    similarity_threshold: float = 0.88,
) -> str:
    existing_clean = clean_memory_fact_text(existing_fact)
    new_clean = clean_memory_fact_text(new_fact)
    if not existing_clean:
        return new_clean
    if not new_clean:
        return existing_clean

    existing_label, existing_body = split_memory_fact(existing_clean)
    new_label, new_body = split_memory_fact(new_clean)
    if is_duplicate_memory_fact(existing_clean, new_clean, similarity_threshold=similarity_threshold):
        chosen_label = _preferred_label(existing_label, new_label)
        chosen_body = _choose_more_informative_text(
            existing_body or existing_clean,
            new_body or new_clean,
        )
        rendered = render_memory_fact(chosen_label, chosen_body)
        if rendered:
            return rendered
    return _choose_more_informative_text(existing_clean, new_clean)


def _preferred_label(left: str | None, right: str | None) -> str | None:
    candidates = [label for label in (left, right) if label]
    if not candidates:
        return None
    return max(
        candidates,
        key=lambda label: (_LABEL_PRIORITY.get(label, 0), len(label)),
    )


def _choose_more_informative_text(left: str, right: str) -> str:
    candidates = [clean_memory_fact_text(left), clean_memory_fact_text(right)]
    candidates = [candidate for candidate in candidates if candidate]
    if not candidates:
        return ""
    return max(
        candidates,
        key=lambda text: (_information_score(text), len(text)),
    )


def _information_score(text: str) -> int:
    tokens = [token for token in re.split(r"\s+", text.casefold()) if token]
    alpha_chars = sum(ch.isalnum() or ("\u4e00" <= ch <= "\u9fff") for ch in text)
    return alpha_chars + len(set(tokens)) * 4
