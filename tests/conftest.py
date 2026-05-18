"""Synthetic pytest fixtures for T150 ReplyPlanner regression tests.

All fixtures use short, domain-neutral, synthetic content.
No real chat text, real names, real platform IDs, or private paths are included.
"""
from __future__ import annotations

import pytest

from practical_chat_agent.core.enums import ChatIntent
from practical_chat_agent.core.models import ApprovedStoreContext

from tests.helpers import context, event, memory, memory_brief, skill_brief


@pytest.fixture
def baseline_friend_context():
    """Baseline friend context with approved store loaded."""
    skill = skill_brief(
        record_id="approved_skill_friend_001",
        contact_id="contact_friend",
        relationship_type="friend",
        relationship_summary="casual friend, low frequency",
        strategy_hints=["keep warm"],
        boundary_reminders=["stay friendly and relaxed"],
        evidence_refs=["ev_friend_001", "ev_friend_002"],
    )
    store = ApprovedStoreContext(
        status="loaded",
        contact_id="contact_friend",
        contact_skill=skill,
        memory_facts=[
            memory_brief(record_id="mem_friend_001", claim="likes hiking on weekends"),
        ],
        evidence_refs=["ev_friend_001", "ev_friend_002"],
    )
    return context(
        contact_id="contact_friend",
        latest_message_text="hey, how have you been?",
        recent_events=[event("evt_friend_1", "long time no see")],
        memory_hits=[memory("mem_friend_runtime_1", "enjoys outdoor activities")],
        approved_store_context=store,
    )


@pytest.fixture
def colleague_context():
    """Practical colleague context with approved store loaded."""
    skill = skill_brief(
        record_id="approved_skill_coll_001",
        contact_id="contact_colleague",
        relationship_type="colleague",
        relationship_summary="work colleague, practical communication",
        strategy_hints=["brief and direct", "keep professional"],
        boundary_reminders=[],
        evidence_refs=["ev_coll_001"],
    )
    store = ApprovedStoreContext(
        status="loaded",
        contact_id="contact_colleague",
        contact_skill=skill,
        memory_facts=[
            memory_brief(record_id="mem_coll_001", claim="prefers email over chat"),
        ],
        evidence_refs=["ev_coll_001"],
    )
    return context(
        contact_id="contact_colleague",
        latest_message_text="the project deadline is next Friday",
        recent_events=[event("evt_coll_1", "can you review the document?")],
        memory_hits=[memory("mem_coll_runtime_1", "works on project alpha")],
        approved_store_context=store,
    )


@pytest.fixture
def thin_context():
    """Thin context with no approved store configured."""
    return context(
        contact_id="contact_thin",
        latest_message_text="random text message",
        recent_events=[event("evt_thin_1", "some event text")],
        approved_store_context=ApprovedStoreContext(status="not_configured"),
    )


@pytest.fixture
def sensitive_context():
    """Sensitive/boundary context with emotional topic and boundary cues."""
    skill = skill_brief(
        record_id="approved_skill_sens_001",
        contact_id="contact_sensitive",
        relationship_type="friend",
        relationship_summary="close friend going through difficult time",
        strategy_hints=["give space", "do not push"],
        boundary_reminders=["keep distance emotionally", "do not追问"],
        evidence_refs=["ev_sens_001"],
    )
    store = ApprovedStoreContext(
        status="loaded",
        contact_id="contact_sensitive",
        contact_skill=skill,
        memory_facts=[
            memory_brief(record_id="mem_sens_001", claim="recent family difficulties"),
        ],
        evidence_refs=["ev_sens_001"],
    )
    return context(
        contact_id="contact_sensitive",
        latest_message_text="I've been having a hard time with family stuff lately",
        recent_events=[event("evt_sens_1", "not feeling great about things at home")],
        memory_hits=[memory("mem_sens_runtime_1", "mentioned feeling overwhelmed")],
        intent=ChatIntent.EMOTION,
        approved_store_context=store,
    )


@pytest.fixture
def false_positive_probe_context():
    """Normal work text containing 'money' in a budgeting context.

    The keyword 'money' triggers sensitive_topic=True, but because
    intent is GENERAL and no boundary cues exist, boundary_sensitive
    should remain False.
    """
    skill = skill_brief(
        record_id="approved_skill_fp_001",
        contact_id="contact_fp",
        relationship_type="colleague",
        relationship_summary="colleague on another team",
        strategy_hints=["concise"],
        boundary_reminders=[],
        evidence_refs=["ev_fp_001"],
    )
    store = ApprovedStoreContext(
        status="loaded",
        contact_id="contact_fp",
        contact_skill=skill,
        evidence_refs=["ev_fp_001"],
    )
    return context(
        contact_id="contact_fp",
        latest_message_text="can we go over the money allocation for the project?",
        recent_events=[event("evt_fp_1", "the team needs to finalize the plan")],
        approved_store_context=store,
    )


@pytest.fixture
def false_negative_probe_context():
    """Subtle pacing pressure that keyword detection may miss.

    "you should really call me sometime soon" does not match any
    _BOUNDARY_CUE_KEYWORDS, _SENSITIVE_TOPIC_KEYWORDS, or
    _AVOID_FOLLOW_UP_KEYWORDS.  This is a documented accepted
    limitation under M3 Conditional.
    """
    skill = skill_brief(
        record_id="approved_skill_fn_001",
        contact_id="contact_fn",
        relationship_type="friend",
        relationship_summary="acquaintance, not very close",
        strategy_hints=[],
        boundary_reminders=[],
        evidence_refs=["ev_fn_001"],
    )
    store = ApprovedStoreContext(
        status="loaded",
        contact_id="contact_fn",
        contact_skill=skill,
        evidence_refs=["ev_fn_001"],
    )
    return context(
        contact_id="contact_fn",
        latest_message_text="you should really call me sometime soon",
        recent_events=[event("evt_fn_1", "we haven't talked in a while")],
        approved_store_context=store,
    )


@pytest.fixture
def privacy_probe_context():
    """Context with unique private markers to test leakage.

    Each marker (abcdef9876, zyxwv6543, qprstu3210, xyzzy123) appears
    only in the input side and must never appear in the output ReplyPlan.
    """
    skill = skill_brief(
        record_id="approved_skill_priv_001",
        contact_id="contact_priv",
        relationship_type="friend",
        relationship_summary="friend with private details",
        strategy_hints=[],
        boundary_reminders=[],
        evidence_refs=["ev_priv_001"],
    )
    store = ApprovedStoreContext(
        status="loaded",
        contact_id="contact_priv",
        contact_skill=skill,
        memory_facts=[
            memory_brief(record_id="mem_priv_001", claim="private marker claim xyzzy123"),
        ],
        evidence_refs=["ev_priv_001"],
    )
    return context(
        contact_id="contact_priv",
        latest_message_text="unique private marker abcdef9876 in message text",
        recent_events=[event("evt_priv_1", "unique private marker zyxwv6543 in event text")],
        memory_hits=[memory("mem_priv_runtime_1", "unique private marker qprstu3210 in memory")],
        approved_store_context=store,
    )


@pytest.fixture
def loaded_no_skill_context():
    """Loaded store but contact_skill is None.

    Demonstrates thin_context=True even when status='loaded',
    because the approved skill brief is absent.  Distinct from
    the generic thin_context fixture which uses status='not_configured'.
    """
    store = ApprovedStoreContext(
        status="loaded",
        contact_id="contact_no_skill",
        contact_skill=None,
        evidence_refs=["ev_noskill_001"],
    )
    return context(
        contact_id="contact_no_skill",
        latest_message_text="hey there",
        recent_events=[event("evt_noskill_1", "just saying hi")],
        approved_store_context=store,
    )


@pytest.fixture
def degraded_store_context():
    """Store with status='store_path_missing' and no contact_skill.

    Demonstrates thin_context for a non-loaded, non-not_configured status.
    """
    store = ApprovedStoreContext(
        status="store_path_missing",
        contact_id=None,
        contact_skill=None,
        evidence_refs=[],
    )
    return context(
        contact_id="contact_degraded",
        latest_message_text="random message text",
        recent_events=[event("evt_degraded_1", "some event")],
        approved_store_context=store,
    )


@pytest.fixture
def over_proactivity_probe_context():
    """Context where conservative_mode and avoid_follow_up are both True,
    making over-proactive detection more sensitive.

    Skill carries boundary reminders with 'do not push' and 'low pressure'
    cues that trigger both boundary_sensitive and avoid_follow_up via
    explicit boundary keyword matching (not via EMOTION intent).
    """
    skill = skill_brief(
        record_id="approved_skill_op_001",
        contact_id="contact_op",
        relationship_type="friend",
        relationship_summary="friend who needs space",
        strategy_hints=["give space", "optional follow-up only"],
        boundary_reminders=["do not push for details", "keep low pressure"],
        evidence_refs=["ev_op_001"],
    )
    store = ApprovedStoreContext(
        status="loaded",
        contact_id="contact_op",
        contact_skill=skill,
        memory_facts=[
            memory_brief(record_id="mem_op_001", claim="going through a difficult period"),
        ],
        evidence_refs=["ev_op_001"],
    )
    return context(
        contact_id="contact_op",
        latest_message_text="I need some time to think about things",
        recent_events=[event("evt_op_1", "mentioned needing space")],
        approved_store_context=store,
    )
