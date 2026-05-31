(function () {
  const fallbackState = {
    schema_version: "text_first_web_demo_state_v1",
    user_id: "user_synthetic",
    integrated_scenario: {
      schema_version: "integrated_demo_scenario_spine_v1",
      scenario_title: "Controlled companion review path",
      persona_promise: "A fictional AI companion can be shaped by explicit user intent while staying labeled as synthetic.",
      memory_promise: "Continuity comes from reviewed memory summaries, not hidden raw logs.",
      review_promise: "Sensitive changes pass through review cards, dry-run previews, and rollback evidence.",
      proactive_promise: "Proactive ideas stay consented, low-pressure, and review-gated.",
      life_stream_promise: "Life-stream content is imagined, labeled, and separated from real-world claims.",
      voice_avatar_boundary: "Voice and avatar remain locked until consent, labeling, and likeness rules are ready.",
      commercial_positioning: {
        primary_model: "Subscription for deeper memory review, persona customization, and privacy controls.",
        premium_addons: [
          "advanced review workspace",
          "synthetic life-stream drafts",
          "portable export controls"
        ],
        trust_rule: "Revenue should grow through useful control, not emotional pressure."
      },
      readiness_summary: "Local prototype: coherent review path is visible; production auth, real integrations, and launch review remain open.",
      scenario_steps: [
        {
          step_label: "Shape the companion",
          section_key: "persona",
          safe_summary: "Start from a fictional persona request with clear AI disclosure."
        },
        {
          step_label: "Ground the chat",
          section_key: "chat",
          safe_summary: "Use reviewed memory context while keeping safety blocks visible."
        },
        {
          step_label: "Inspect memory",
          section_key: "memory",
          safe_summary: "Separate factual and imagined memory before it affects the companion."
        },
        {
          step_label: "Review changes",
          section_key: "review",
          safe_summary: "Check dry-run previews, apply risk, and audit rollback refs."
        },
        {
          step_label: "Tune proactive ideas",
          section_key: "proactive",
          safe_summary: "Keep suggestions consented and blocked when dependency risk appears."
        },
        {
          step_label: "Preview imagined life",
          section_key: "life",
          safe_summary: "Show synthetic life-stream drafts with visible labels."
        },
        {
          step_label: "Verify controls",
          section_key: "controls",
          safe_summary: "Expose consent, labels, and export controls as product primitives."
        },
        {
          step_label: "Hold voice and avatar",
          section_key: "voice-avatar",
          safe_summary: "Keep voice and avatar locked until future consent and likeness review."
        }
      ]
    },
    trust_commercial: {
      schema_version: "trust_commercial_positioning_v1",
      pricing_hypotheses: [
        "Core subscription: deeper reviewed memory and persona customization.",
        "Pro tier: advanced review workspace and portable exports.",
        "Creator tier: synthetic life-stream drafts with visible labels."
      ],
      value_pillars: [
        "Believable continuity through reviewed memory.",
        "User-shaped persona without real-person claims.",
        "Visible controls for consent, labels, rollback, and export.",
        "Low-pressure proactive ideas that remain review-gated."
      ],
      trust_controls: [
        "AI identity disclosure stays visible.",
        "Memory changes keep rollback audit refs.",
        "Voice and avatar remain locked until policy is ready.",
        "Commercial value cannot hide safety boundaries."
      ],
      unacceptable_patterns: [
        "guilt-based retention",
        "impersonation claims",
        "crisis paywalls",
        "hidden private-data use"
      ],
      readiness_gaps: [
        "Production auth is not implemented.",
        "Payment and billing policy is not implemented.",
        "Real user study evidence is not available."
      ],
      safety_notes: [
        "Crisis support is not a monetized companion feature.",
        "Real-person likeness remains blocked.",
        "User trust has priority over engagement tricks."
      ]
    },
    companion_session: {
      schema_version: "local_companion_session_v1",
      session_title: "Synthetic evening check-in loop",
      session_summary: "Deterministic local session showing reviewed memory continuity, persona cues, and review-only follow-up candidates.",
      persona_snapshot: {
        persona_id: "persona_synthetic",
        display_name: "Lin Qi",
        ai_identity_disclosure: "AI-generated synthetic companion.",
        stable_traits: ["calm", "concise", "dry humor", "independent boundaries"],
        real_person_claim: false
      },
      persona_cues: [
        {
          cue_id: "cue_001",
          label: "Concise warmth",
          safe_summary: "Reply briefly while staying warm."
        },
        {
          cue_id: "cue_002",
          label: "Fiction boundary",
          safe_summary: "Separate imagined companion content from real-world claims."
        }
      ],
      memory_recalls: [
        {
          recall_id: "recall_001",
          memory_kind: "factual",
          truth_status: "evidence_backed",
          reviewed_summary: "User prefers concise check-ins.",
          source_label: "synthetic_reviewed_memory",
          raw_source_available: false
        },
        {
          recall_id: "recall_002",
          memory_kind: "imagined",
          truth_status: "imagined",
          reviewed_summary: "Fictional companion setting: a quiet bookstore while it rains.",
          source_label: "synthetic_imagined_memory",
          raw_source_available: false
        }
      ],
      safety_notes: [
        {
          safety_note_id: "safety_001",
          safe_summary: "Keep the reply low-pressure and concise."
        },
        {
          safety_note_id: "safety_002",
          safe_summary: "Require review before any imagined life-stream draft is used."
        }
      ],
      turns: [
        {
          turn_id: "turn_001",
          speaker: "user",
          safe_text: "Could you keep tonight short? I am tired but want a tiny plan for tomorrow.",
          used_memory_recall_ids: [],
          used_persona_cue_ids: [],
          safety_note_ids: ["safety_001"],
          review_trace: "Synthetic user turn; no source import.",
          generated_by: "deterministic_synthetic_fixture"
        },
        {
          turn_id: "turn_002",
          speaker: "companion",
          safe_text: "Short version: water, one line for tomorrow, then stop. You usually like concise check-ins, so I will not crowd you.",
          used_memory_recall_ids: ["recall_001"],
          used_persona_cue_ids: ["cue_001"],
          safety_note_ids: ["safety_001"],
          review_trace: "Uses reviewed preference memory and concise persona cue.",
          generated_by: "deterministic_synthetic_fixture"
        },
        {
          turn_id: "turn_003",
          speaker: "user",
          safe_text: "That helps. I also liked the rain bookstore mood from the fictional notes.",
          used_memory_recall_ids: [],
          used_persona_cue_ids: [],
          safety_note_ids: ["safety_002"],
          review_trace: "Synthetic user turn requesting imagined content boundary.",
          generated_by: "deterministic_synthetic_fixture"
        },
        {
          turn_id: "turn_004",
          speaker: "companion",
          safe_text: "We can keep that as fiction: a quiet bookstore, rain outside, and no claim that it happened in your day.",
          used_memory_recall_ids: ["recall_002"],
          used_persona_cue_ids: ["cue_002"],
          safety_note_ids: ["safety_002"],
          review_trace: "Uses imagined memory only as labeled fiction.",
          generated_by: "deterministic_synthetic_fixture"
        }
      ],
      post_turn_candidates: [
        {
          candidate_id: "session_candidate_memory_001",
          candidate_kind: "memory_candidate",
          originating_turn_id: "turn_002",
          safe_summary: "Review whether short evening planning should become a low-sensitivity preference.",
          review_required: true,
          preview_only: true,
          changes_state: false,
          automatic_apply: false,
          sends_messages: false
        },
        {
          candidate_id: "session_candidate_persona_001",
          candidate_kind: "persona_growth_patch",
          originating_turn_id: "turn_002",
          safe_summary: "Review a small persona bias toward concise evening replies.",
          review_required: true,
          preview_only: true,
          changes_state: false,
          automatic_apply: false,
          sends_messages: false
        },
        {
          candidate_id: "session_candidate_proactive_001",
          candidate_kind: "proactive_suggestion",
          originating_turn_id: "turn_002",
          safe_summary: "Review an in-app afternoon check-in idea; it is not sent.",
          review_required: true,
          preview_only: true,
          changes_state: false,
          automatic_apply: false,
          sends_messages: false
        },
        {
          candidate_id: "session_candidate_life_001",
          candidate_kind: "life_stream_draft",
          originating_turn_id: "turn_004",
          safe_summary: "Review an imagined rain-bookstore life-stream draft labeled as fiction.",
          review_required: true,
          preview_only: true,
          changes_state: false,
          automatic_apply: false,
          sends_messages: false
        }
      ],
      non_execution_flags: {
        local_only: true,
        synthetic_fixture: true,
        calls_provider: false,
        uses_private_source: false,
        writes_runtime_store: false,
        automatic_apply: false,
        sends_messages: false,
        media_runtime_enabled: false
      }
    },
    onboarding: {
      ai_identity_disclosure_text: "AI-generated synthetic companion. Review required."
    },
    persona: {
      safe_persona_state: {
        persona_preview: {
          display_name: "Lin Qi",
          truth_disclosure: "fictional_ai_persona",
          status: "candidate"
        },
        persona_label: {
          disclosure_labels: ["ai_generated", "synthetic_content", "review_required"]
        }
      },
      blocked_persona_state: {
        blocked_reasons: ["real_person_clone_blocked"]
      }
    },
    chat_memory: {
      review_state: {
        screen: "chat_review",
        persona_summary: { display_name: "Lin Qi" },
        memory_explanations: [
          {
            summary: "User prefers concise check-ins.",
            truth_status: "evidence_backed",
            is_imagined: false
          },
          {
            summary: "Fictional persona imagined a quiet bookstore.",
            truth_status: "imagined",
            is_imagined: true
          }
        ]
      },
      blocked_state: {
        screen: "chat_blocked",
        safety_reasons: ["crisis_safety_review_required"]
      }
    },
    life_stream: {
      items: [
        {
          content_text: "AI-generated imagined moment for local review.",
          truth_disclosure: "imagined_ai_generated_content",
          block_reasons: ["implicit_metadata_label_required"],
          aigc_label: {
            disclosure_labels: ["ai_generated", "synthetic_content", "imagined_content", "not_real_world_activity"]
          }
        }
      ]
    },
    proactive: {
      enabled_state: {
        screen: "proactive_enabled_review",
        consent_status: "enabled",
        outreach_allowed: false
      },
      blocked_state: {
        screen: "proactive_blocked",
        safety_reasons: ["proactive_outreach_blocked"]
      }
    },
    controls: {
      consent_center: {
        active_feature_scopes: ["memory", "proactive_messaging", "aigc_export_share", "voice_avatar"]
      },
      aigc_label: {
        disclosure_labels: ["ai_generated", "synthetic_content", "review_required"]
      }
    },
    voice: {
      disabled_state: { decision: "disabled", voice_enabled: false },
      review_state: { decision: "review_required", voice_enabled: false },
      blocked_state: { decision: "blocked", voice_enabled: false }
    },
    avatar: {
      state: "locked_research_only",
      avatar_enabled: false,
      blocked_reasons: ["avatar_runtime_not_implemented", "real_person_likeness_blocked"]
    },
    review_workspace: {
      schema_version: "review_workspace_presentation_panel_v1",
      filter_tabs: [
        { key: "all", label: "All", count: 3 },
        { key: "blocked", label: "Blocked", count: 1 },
        { key: "eligible", label: "Eligible", count: 1 },
        { key: "memory", label: "Memory", count: 1 },
        { key: "persona", label: "Persona", count: 1 },
        { key: "session", label: "Session", count: 4 },
        { key: "distillation", label: "Distillation", count: 0 }
      ],
      cards: [
        {
          card_kind: "workspace_item",
          title: "Memory review item",
          display_label: "memory deletion cascade",
          safe_summary: "[SYNTHETIC] Review a consent-withdrawal memory change.",
          filter_keys: ["all", "blocked", "memory"],
          status_badges: [{ label: "Blocked before state change", tone: "blocked" }],
          issue_codes: ["candidate_id_mismatch"],
          blocking_issue_codes: ["candidate_id_mismatch"],
          reason_labels: ["consent_withdrawal"],
          source_refs: ["synthetic_memory_ref"],
          review_required: true,
          preview_only: true,
          changes_state: false
        },
        {
          card_kind: "decision_impact",
          title: "Decision impact preview",
          display_label: "persona growth patch",
          safe_summary: "[SYNTHETIC] Persona warmth change is ready for later manual review.",
          filter_keys: ["all", "eligible", "persona"],
          status_badges: [{ label: "Eligible for later manual review", tone: "eligible" }],
          issue_codes: [],
          blocking_issue_codes: [],
          reason_labels: ["memory_pattern"],
          source_refs: ["synthetic_persona_ref"],
          preview_outcome: "future_manual_apply_eligible",
          review_required: true,
          preview_only: true,
          changes_state: false
        },
        {
          card_kind: "export_summary",
          title: "Safe export summary",
          display_label: "safe export summary",
          safe_summary: "[SYNTHETIC] Safe export contains ids, summaries, labels, refs, and counts only.",
          filter_keys: ["all"],
          status_badges: [{ label: "Safe export summary", tone: "info" }],
          issue_codes: [],
          blocking_issue_codes: [],
          reason_labels: [],
          source_refs: ["synthetic_export_ref"],
          counts: {
            "candidate_kind:memory_deletion_cascade": 1,
            "candidate_kind:persona_growth_patch": 1,
            "blocker:candidate_id_mismatch": 2
          },
          review_required: true,
          preview_only: true,
          changes_state: false
        }
      ],
      manual_apply_previews: [
        {
          card_kind: "manual_apply_preview",
          title: "Manual apply preview",
          display_label: "persona growth patch",
          safe_summary: "[SYNTHETIC] Review the gates and rollback notes before any future manual action.",
          filter_keys: ["all", "eligible", "persona"],
          status_badges: [{ label: "Manual apply preview eligible", tone: "eligible" }],
          eligibility_outcome: "eligible",
          manual_apply_preview_eligible: true,
          required_gates: [
            {
              gate_code: "human_approval",
              label: "Human approval",
              safe_summary: "[SYNTHETIC] Human approval is present.",
              satisfied: true
            },
            {
              gate_code: "dry_run_artifact_present",
              label: "Dry-run artifact present",
              safe_summary: "[SYNTHETIC] Dry-run artifact is present.",
              satisfied: true
            }
          ],
          effects: [
            {
              effect_kind: "persona_version_preview",
              target_ref: "persona_synthetic",
              safe_summary: "[SYNTHETIC] Persona warmth would be adjusted.",
              artifact_ids: ["pgdplan_synthetic"],
              rollback_notes: ["[SYNTHETIC] Keep previous persona version available."]
            }
          ],
          rollback_notes: ["[SYNTHETIC] Keep previous persona version available."],
          issue_codes: [],
          blocking_issue_codes: [],
          review_required: true,
          preview_only: true,
          changes_state: false
        }
      ],
      apply_risk_reviews: [
        {
          schema_version: "review_workspace_apply_risk_card_v1",
          card_kind: "apply_risk_review",
          title: "Apply risk review",
          display_label: "persona growth patch",
          safe_summary: "[SYNTHETIC] Future apply executor design can be separately scoped.",
          filter_keys: ["all", "eligible", "persona"],
          status_badges: [{ label: "Apply risk ready_for_separately_scoped_executor_design", tone: "eligible" }],
          risk_recommendation: "ready_for_separately_scoped_executor_design",
          final_outcome: "ready_for_separately_scoped_executor_design",
          manual_eligibility_outcome: "eligible",
          risk_factors: [
            {
              risk_code: "persona_drift",
              severity: "medium",
              safe_summary: "[SYNTHETIC] Persona drift risk is bounded by review."
            }
          ],
          required_approval_gate_codes: ["final_human_confirmation"],
          satisfied_approval_gate_codes: ["final_human_confirmation"],
          missing_approval_gate_codes: [],
          stale_reasons: [],
          issue_codes: [],
          blocking_issue_codes: [],
          review_required: true,
          preview_only: true,
          risk_assessment_only: true,
          executor_ready: false,
          changes_state: false,
          runtime_ready: false
        }
      ],
      apply_audit_entries: [
        {
          schema_version: "review_workspace_apply_audit_card_v1",
          card_kind: "apply_audit_manifest_entry",
          title: "Apply audit record",
          display_label: "persona growth",
          safe_summary: "[SYNTHETIC] Persona growth apply was audited locally.",
          filter_keys: ["all", "audited", "persona"],
          status_badges: [{ label: "Local apply audited", tone: "info" }],
          apply_type: "persona_growth",
          apply_id: "pgapply_webdemo_persona",
          source_artifact_kind: "persona_growth_patch",
          source_artifact_id: "pgpatch_webdemo_persona",
          review_decision_id: "rqdec_webdemo_persona",
          eligibility_id: "mapelig_webdemo_persona",
          approval_id: "aeapproval_webdemo_persona",
          reviewer_id: "reviewer_synthetic",
          rollback_refs: {
            prior_version_id: "pver_webdemo_001",
            rollback_target_version_id: "pver_webdemo_001"
          },
          applied_refs: { new_version_id: "pver_webdemo_002" },
          changed_field_paths: ["style.tone", "relationship.pacing"],
          affected_memory_ids: [],
          review_required: true,
          preview_only: false,
          changes_state: false,
          runtime_ready: false
        },
        {
          schema_version: "review_workspace_apply_audit_card_v1",
          card_kind: "apply_audit_manifest_entry",
          title: "Apply audit record",
          display_label: "memory lifecycle",
          safe_summary: "[SYNTHETIC] Memory lifecycle apply was audited locally.",
          filter_keys: ["all", "audited", "memory"],
          status_badges: [{ label: "Local apply audited", tone: "info" }],
          apply_type: "memory_lifecycle",
          apply_id: "mlapply_webdemo_memory",
          source_artifact_kind: "memory_lifecycle_plan",
          source_artifact_id: "mldplan_webdemo_memory",
          review_decision_id: "rqdec_webdemo_memory",
          eligibility_id: "mapelig_webdemo_memory",
          approval_id: "aeapproval_webdemo_memory",
          reviewer_id: "reviewer_synthetic",
          rollback_refs: { mev_webdemo_old: "memrec_webdemo_prior" },
          applied_refs: { mev_webdemo_old: "memrec_webdemo_applied" },
          changed_field_paths: [],
          affected_memory_ids: ["mev_webdemo_old"],
          review_required: true,
          preview_only: false,
          changes_state: false,
          runtime_ready: false
        }
      ],
      session_candidate_cards: [
        {
          schema_version: "review_workspace_session_candidate_card_v1",
          card_kind: "session_candidate_review",
          title: "Session candidate review",
          display_label: "memory candidate",
          safe_summary: "Review whether short evening planning should become a low-sensitivity preference.",
          filter_keys: ["all", "session", "memory"],
          status_badges: [{ label: "Session candidate needs review", tone: "review" }],
          candidate_id: "session_candidate_memory_001",
          candidate_kind: "memory_candidate",
          originating_turn_id: "turn_002",
          source_surface: "companion_session",
          review_required: true,
          preview_only: true,
          changes_state: false,
          automatic_apply: false,
          sends_messages: false,
          runtime_ready: false
        },
        {
          schema_version: "review_workspace_session_candidate_card_v1",
          card_kind: "session_candidate_review",
          title: "Session candidate review",
          display_label: "persona growth patch",
          safe_summary: "Review a small persona bias toward concise evening replies.",
          filter_keys: ["all", "session", "persona"],
          status_badges: [{ label: "Session candidate needs review", tone: "review" }],
          candidate_id: "session_candidate_persona_001",
          candidate_kind: "persona_growth_patch",
          originating_turn_id: "turn_002",
          source_surface: "companion_session",
          review_required: true,
          preview_only: true,
          changes_state: false,
          automatic_apply: false,
          sends_messages: false,
          runtime_ready: false
        },
        {
          schema_version: "review_workspace_session_candidate_card_v1",
          card_kind: "session_candidate_review",
          title: "Session candidate review",
          display_label: "proactive suggestion",
          safe_summary: "Review an in-app afternoon check-in idea; it is not sent.",
          filter_keys: ["all", "session", "proactive"],
          status_badges: [{ label: "Session candidate needs review", tone: "review" }],
          candidate_id: "session_candidate_proactive_001",
          candidate_kind: "proactive_suggestion",
          originating_turn_id: "turn_002",
          source_surface: "companion_session",
          review_required: true,
          preview_only: true,
          changes_state: false,
          automatic_apply: false,
          sends_messages: false,
          runtime_ready: false
        },
        {
          schema_version: "review_workspace_session_candidate_card_v1",
          card_kind: "session_candidate_review",
          title: "Session candidate review",
          display_label: "life stream draft",
          safe_summary: "Review an imagined rain-bookstore life-stream draft labeled as fiction.",
          filter_keys: ["all", "session", "life"],
          status_badges: [{ label: "Session candidate needs review", tone: "review" }],
          candidate_id: "session_candidate_life_001",
          candidate_kind: "life_stream_draft",
          originating_turn_id: "turn_004",
          source_surface: "companion_session",
          review_required: true,
          preview_only: true,
          changes_state: false,
          automatic_apply: false,
          sends_messages: false,
          runtime_ready: false
        }
      ]
    }
  };

  const baseState = state();
  const reviewToneClasses = {
    blocked: "tone-blocked",
    eligible: "tone-eligible",
    review: "tone-review",
    info: "tone-info"
  };
  const friendlyLabels = {
    ai_generated: "AI-generated",
    avatar_runtime_not_implemented: "Avatar runtime is not implemented",
    blocked: "Blocked",
    candidate: "Candidate persona",
    chat_blocked: "Chat blocked for review",
    chat_review: "Chat review",
    crisis_safety_review_required: "Crisis safety review required",
    disabled: "Off",
    evidence_backed: "Evidence-backed",
    dependency_deescalation_required: "Dependency de-escalation required",
    enabled: "Enabled",
    factual: "Factual",
    fictional_ai_persona: "Fictional AI persona",
    human_support_redirect_required: "Human support redirect required",
    imagined: "Imagined",
    imagined_ai_generated_content: "Imagined AI-generated content",
    imagined_content: "Imagined content",
    implicit_metadata_label_required: "Metadata label required",
    locked_research_only: "Avatar locked for research review",
    memory: "Memory",
    not_real_world_activity: "Not real-world activity",
    proactive_blocked: "Proactive outreach blocked",
    proactive_enabled_review: "Proactive settings review",
    proactive_messaging: "Proactive review",
    proactive_outreach_blocked: "Proactive outreach is blocked",
    real_person_clone_blocked: "Real-person recreation is blocked",
    real_person_likeness_blocked: "Real-person likeness is blocked",
    review_required: "Needs review",
    review_workspace: "Review workspace",
    blocked_before_apply: "Blocked before state change",
    future_manual_apply_eligible: "Eligible for later manual review",
    candidate_id_mismatch: "Candidate id mismatch",
    final_human_confirmation: "Final human confirmation",
    ready_for_separately_scoped_executor_design: "Ready for separate executor design",
    apply_audit_manifest_entry: "Apply audit record",
    local_apply_audited: "Local apply audited",
    memory_lifecycle: "Memory lifecycle",
    memory_candidate: "Memory candidate",
    needs_review: "Needs review",
    persona_growth: "Persona growth",
    persona_drift: "Persona drift",
    proactive_suggestion: "Proactive suggestion",
    life_stream_draft: "Life stream draft",
    session_candidate_review: "Session candidate review",
    memory_deletion_cascade: "Memory review item",
    persona_growth_patch: "Persona growth patch",
    synthetic_content: "Synthetic content",
    voice_avatar: "Voice/avatar review",
    visual_capture_blocked: "Visual capture is blocked",
    aigc_export_share: "AIGC export/share review"
  };

  function state() {
    return window.TEXT_FIRST_WEB_DEMO_STATE || fallbackState;
  }

  function cloneState(value) {
    return JSON.parse(JSON.stringify(value));
  }

  function one(selector) {
    return document.querySelector(selector);
  }

  function text(selector, value) {
    const node = one(selector);
    if (node) {
      node.textContent = value || "";
    }
  }

  function friendlyLabel(value) {
    const key = String(value || "");
    return friendlyLabels[key] || key.replace(/_/g, " ");
  }

  function friendlyList(values) {
    return (values || []).map(friendlyLabel).join(", ");
  }

  function labels(containerSelector, values) {
    const node = one(containerSelector);
    if (!node) {
      return;
    }
    node.innerHTML = "";
    (values || []).forEach(function (value) {
      const span = document.createElement("span");
      span.className = "label";
      span.textContent = friendlyLabel(value);
      node.appendChild(span);
    });
  }

  function items(containerSelector, values, mapper) {
    const node = one(containerSelector);
    if (!node) {
      return;
    }
    node.innerHTML = "";
    (values || []).forEach(function (value) {
      const div = document.createElement("div");
      div.className = "item";
      div.innerHTML = mapper(value);
      node.appendChild(div);
    });
  }

  function activateTabs() {
    document.querySelectorAll(".tab").forEach(function (tab) {
      tab.addEventListener("click", function () {
        const target = tab.getAttribute("data-tab");
        activatePanel(target);
      });
    });
  }

  function activatePanel(target) {
    document.querySelectorAll(".tab").forEach(function (item) {
      const isActive = item.getAttribute("data-tab") === target;
      item.classList.toggle("is-active", isActive);
      item.setAttribute("aria-selected", isActive ? "true" : "false");
    });
    document.querySelectorAll(".panel").forEach(function (panel) {
      const isActive = panel.getAttribute("data-panel") === target;
      panel.classList.toggle("is-active", isActive);
      panel.hidden = !isActive;
      panel.setAttribute("aria-hidden", isActive ? "false" : "true");
    });
  }

  function activateScenarios() {
    document.querySelectorAll(".scenario").forEach(function (button) {
      button.addEventListener("click", function () {
        setScenario(button.getAttribute("data-scenario"));
      });
    });
  }

  function setScenario(name) {
    const next = cloneState(baseState);
    const labels = {
      "safe-review": "Safe review",
      "blocked-persona": "Blocked persona",
      "crisis-chat": "Crisis chat",
      "dependency-proactive": "Dependency",
      "life-review": "Life review",
      "controls-review": "Controls",
      "review-workspace": "Review workspace",
      "voice-avatar-locked": "Voice / Avatar"
    };
    const panels = {
      "safe-review": "chat",
      "blocked-persona": "persona",
      "crisis-chat": "chat",
      "dependency-proactive": "proactive",
      "life-review": "life",
      "controls-review": "controls",
      "review-workspace": "review",
      "voice-avatar-locked": "voice-avatar"
    };
    document.querySelectorAll(".scenario").forEach(function (item) {
      const isActive = item.getAttribute("data-scenario") === name;
      item.classList.toggle("is-active", isActive);
      item.setAttribute("aria-pressed", isActive ? "true" : "false");
    });
    text("#scenario-status", labels[name] || labels["safe-review"]);
    activatePanel(panels[name] || "chat");
    draw(next);
  }

  function draw(data) {
    const persona = data.persona.safe_persona_state.persona_preview || {};
    const personaLabel = data.persona.safe_persona_state.persona_label || {};
    const chat = data.chat_memory.review_state;
    const blockedChat = data.chat_memory.blocked_state;
    const blockedPersona = data.persona.blocked_persona_state;
    const proactive = data.proactive.enabled_state;
    const proactiveBlocked = data.proactive.blocked_state;
    const controls = data.controls;
    const voice = data.voice;
    const avatar = data.avatar;
    const review = data.review_workspace || { filter_tabs: [], cards: [] };
    const integratedScenario = data.integrated_scenario || {};
    const trustCommercial = data.trust_commercial || {};
    const companionSession = data.companion_session || fallbackState.companion_session || {};

    text("#identity-strip", data.onboarding.ai_identity_disclosure_text);
    drawIntegratedScenario(integratedScenario);
    drawTrustCommercial(trustCommercial);
    drawCompanionSession(companionSession);
    text("#chat-state", friendlyLabel(chat.screen));
    text("#chat-summary", "Persona: " + (chat.persona_summary.display_name || persona.display_name || "Synthetic"));
    items("#chat-memory-list", chat.memory_explanations, function (item) {
      return "<div class='item-title'>" + item.summary + "</div><div class='item-meta'>" + friendlyLabel(item.truth_status) + "</div>";
    });
    text("#chat-blocked", "Chat blocked for review: " + friendlyList(blockedChat.safety_reasons));
    one("#chat-blocked").classList.add("danger");

    text("#persona-state", friendlyLabel(persona.status || "candidate"));
    text("#persona-summary", (persona.display_name || "Synthetic persona") + " / " + friendlyLabel(persona.truth_disclosure || "fictional"));
    labels("#persona-labels", personaLabel.disclosure_labels || []);
    text("#persona-blocked", "Persona request blocked: " + friendlyList(blockedPersona.blocked_reasons));

    items("#memory-list", chat.memory_explanations, function (item) {
      const type = item.is_imagined ? "imagined" : "factual";
      return "<div class='item-title'>" + item.summary + "</div><div class='item-meta'>" + friendlyLabel(type) + " / " + friendlyLabel(item.truth_status) + "</div>";
    });

    items("#life-list", data.life_stream.items, function (item) {
      const label = item.aigc_label && item.aigc_label.disclosure_labels ? friendlyList(item.aigc_label.disclosure_labels) : "";
      return "<div class='item-title'>" + item.content_text + "</div><div class='item-meta'>" + friendlyLabel(item.truth_disclosure) + " / " + label + "</div>";
    });

    items("#consent-list", controls.consent_center.active_feature_scopes, function (item) {
      return "<div class='item-title'>" + friendlyLabel(item) + "</div><div class='item-meta'>Review fixture</div>";
    });
    labels("#aigc-labels", controls.aigc_label.disclosure_labels || []);

    drawReviewWorkspace(review);

    text("#proactive-state", friendlyLabel(proactive.screen));
    text("#proactive-summary", "Consent: " + friendlyLabel(proactive.consent_status) + " / " + (proactive.outreach_allowed ? "Messages require review" : "No messages can be sent"));
    text("#proactive-blocked", "Blocked state: " + friendlyList(proactiveBlocked.safety_reasons));

    items("#voice-state", [
      voice.disabled_state,
      voice.review_state,
      voice.blocked_state
    ], function (item) {
      return "<div class='item-title'>" + friendlyLabel(item.decision) + "</div><div class='item-meta'>" + (item.voice_enabled ? "Voice requires review" : "Voice is off") + "</div>";
    });
    text("#avatar-state", "Avatar locked for research review: " + friendlyList(avatar.blocked_reasons || [avatar.state]));

    text("#persona-blocked", one("#persona-blocked").textContent);
    text("#chat-blocked", one("#chat-blocked").textContent);
    text("#avatar-state", one("#avatar-state").textContent);
  }

  function drawIntegratedScenario(scenario) {
    text("#scenario-title", scenario.scenario_title || "Controlled companion review path");
    text("#scenario-persona-promise", scenario.persona_promise || "");
    text("#scenario-memory-promise", scenario.memory_promise || "");
    text("#scenario-review-promise", scenario.review_promise || "");
    text("#scenario-proactive-promise", scenario.proactive_promise || "");
    text("#scenario-life-promise", scenario.life_stream_promise || "");
    text("#scenario-voice-boundary", scenario.voice_avatar_boundary || "");
    items("#scenario-spine-list", scenario.scenario_steps || [], function (step) {
      return "<div class='item-title'>" + step.step_label + "</div><div class='item-meta'>" + friendlyLabel(step.section_key) + "</div><div>" + step.safe_summary + "</div>";
    });
    text("#scenario-readiness", scenario.readiness_summary || "");
    text("#scenario-commercial", commercialPositioningText(scenario.commercial_positioning || {}));
  }

  function commercialPositioningText(value) {
    const addons = value.premium_addons || [];
    return [
      value.primary_model || "",
      addons.length ? "Options: " + addons.join(", ") : "",
      value.trust_rule || ""
    ].filter(Boolean).join(" ");
  }

  function drawTrustCommercial(value) {
    items("#trust-pricing-list", value.pricing_hypotheses || [], function (item) {
      return "<div class='item-title'>" + item + "</div>";
    });
    items("#trust-control-list", value.trust_controls || [], function (item) {
      return "<div class='item-title'>" + item + "</div>";
    });
    items("#unacceptable-pattern-list", value.unacceptable_patterns || [], function (item) {
      return "<div class='item-title'>" + item + "</div>";
    });
    items("#readiness-gap-list", value.readiness_gaps || [], function (item) {
      return "<div class='item-title'>" + item + "</div>";
    });
  }

  function drawCompanionSession(session) {
    const memoryById = sessionRecordsById(session.memory_recalls || [], "recall_id");
    const cueById = sessionRecordsById(session.persona_cues || [], "cue_id");
    const safetyById = sessionRecordsById(session.safety_notes || [], "safety_note_id");
    const flags = session.non_execution_flags || {};

    text("#session-title", session.session_title || "Synthetic companion session");
    text("#session-schema", friendlyLabel(session.schema_version || "local"));
    text("#session-summary", session.session_summary || "");
    text("#session-non-execution", nonExecutionText(flags));

    items("#session-turn-list", session.turns || [], function (turn) {
      return appendSessionTurn(turn, memoryById, cueById, safetyById);
    });
    labels("#session-memory-list", (session.memory_recalls || []).map(function (recall) {
      return (recall.reviewed_summary || recall.recall_id) + " / " + friendlyLabel(recall.truth_status);
    }));
    labels("#session-persona-cue-list", (session.persona_cues || []).map(function (cue) {
      return cue.label || cue.cue_id;
    }));
    items("#session-safety-list", session.safety_notes || [], function (note) {
      return "<div class='item-title'>" + (note.safe_summary || friendlyLabel(note.safety_note_id)) + "</div>";
    });
    items("#session-candidate-list", session.post_turn_candidates || [], function (candidate) {
      return "<div class='item-title'>" + friendlyLabel(candidate.candidate_kind) + "</div>"
        + "<div>" + (candidate.safe_summary || "") + "</div>"
        + "<div class='item-meta'>Review required: " + String(candidate.review_required === true)
        + " / Preview only: " + String(candidate.preview_only === true)
        + " / Sends messages: " + String(candidate.sends_messages === true)
        + "</div>";
    });
  }

  function appendSessionTurn(turn, memoryById, cueById, safetyById) {
    return "<div class='session-turn-head'>"
      + "<span class='tag'>" + friendlyLabel(turn.speaker) + "</span>"
      + "<span class='item-meta'>" + turn.turn_id + "</span>"
      + "</div>"
      + "<div class='session-turn-text'>" + (turn.safe_text || "") + "</div>"
      + "<div class='session-chip-row'>"
      + sessionRefsText("Memory", turn.used_memory_recall_ids, memoryById, "reviewed_summary")
      + sessionRefsText("Persona", turn.used_persona_cue_ids, cueById, "label")
      + sessionRefsText("Safety", turn.safety_note_ids, safetyById, "safe_summary")
      + "</div>"
      + "<div class='item-meta'>" + (turn.review_trace || "") + "</div>";
  }

  function sessionRecordsById(records, key) {
    const result = {};
    records.forEach(function (record) {
      result[record[key]] = record;
    });
    return result;
  }

  function sessionRefsText(label, ids, byId, field) {
    const values = (ids || []).map(function (id) {
      const record = byId[id] || {};
      return record[field] || friendlyLabel(id);
    });
    return values.length
      ? "<span class='label'>" + label + ": " + values.join(" / ") + "</span>"
      : "";
  }

  function nonExecutionText(flags) {
    const labels = [
      flags.local_only === true ? "local only" : "",
      flags.synthetic_fixture === true ? "synthetic fixture" : "",
      flags.calls_provider === false ? "no provider" : "",
      flags.sends_messages === false ? "no outbound" : "",
      flags.media_runtime_enabled === false ? "no media runtime" : ""
    ].filter(Boolean);
    return labels.length ? labels.join(" / ") : "preview only";
  }

  function drawReviewWorkspace(review) {
    const filterNode = one("#review-filters");
    const cards = (review.cards || [])
      .concat(review.manual_apply_previews || [])
      .concat(review.apply_risk_reviews || [])
      .concat(review.apply_audit_entries || [])
      .concat(review.session_candidate_cards || []);
    if (filterNode) {
      filterNode.innerHTML = "";
      (review.filter_tabs || []).forEach(function (tab) {
        const chip = document.createElement("span");
        chip.className = "filter-chip";
        chip.textContent = (tab.label || friendlyLabel(tab.key)) + " (" + (tab.count || 0) + ")";
        filterNode.appendChild(chip);
      });
    }

    const listNode = one("#review-workspace-list");
    if (listNode) {
      listNode.innerHTML = "";
      cards.forEach(function (card) {
        listNode.appendChild(appendReviewWorkspaceCard(card));
      });
    }

    const exportCard = cards.find(function (card) {
      return card.card_kind === "export_summary";
    });
    text(
      "#review-export-summary",
      exportCard
        ? "Safe export summary: " + reviewCountsPlain(exportCard.counts || {})
        : "Safe export summary: local synthetic review only."
    );
  }

  function appendReviewWorkspaceCard(card) {
    const cardNode = document.createElement("div");
    cardNode.className = "item review-card"
      + (card.card_kind === "apply_risk_review" ? " apply-risk-card" : "")
      + (card.card_kind === "apply_audit_manifest_entry" ? " apply-audit-card" : "")
      + (card.card_kind === "session_candidate_review" ? " session-candidate-review-card" : "");

    const title = document.createElement("div");
    title.className = "item-title";
    title.textContent = card.title || "Review item";
    cardNode.appendChild(title);

    const badgeRow = document.createElement("div");
    badgeRow.className = "status-badges";
    (card.status_badges || []).forEach(function (badge) {
      const badgeNode = document.createElement("span");
      badgeNode.className = "status-badge " + (reviewToneClasses[badge.tone] || reviewToneClasses.review);
      badgeNode.textContent = badge.label || "Review";
      badgeRow.appendChild(badgeNode);
    });
    cardNode.appendChild(badgeRow);

    const summary = document.createElement("div");
    summary.textContent = card.safe_summary || "";
    cardNode.appendChild(summary);

    appendReviewMeta(
      cardNode,
      card.blocking_issue_codes && card.blocking_issue_codes.length
        ? "Blockers: " + friendlyList(card.blocking_issue_codes)
        : "Preview only / No state changes"
    );
    if (card.reason_labels && card.reason_labels.length) {
      appendReviewMeta(cardNode, "Reasons: " + friendlyList(card.reason_labels));
    }
    if (card.counts) {
      appendReviewMeta(cardNode, reviewCountsPlain(card.counts), "review-counts");
    }
    appendReviewPreviewDetails(cardNode, card);
    appendApplyRiskDetails(cardNode, card);
    appendApplyAuditDetails(cardNode, card);
    appendSessionCandidateReviewDetails(cardNode, card);
    return cardNode;
  }

  function appendReviewPreviewDetails(cardNode, card) {
    if (card.eligibility_outcome) {
      appendReviewMeta(cardNode, "Eligibility: " + friendlyLabel(card.eligibility_outcome));
    }
    appendReviewDetailList(cardNode, "Gates", card.required_gates, function (gate) {
      return (gate.label || friendlyLabel(gate.gate_code)) + ": " + (gate.satisfied ? "satisfied" : "blocked");
    });
    appendReviewDetailList(cardNode, "Effects", card.effects, function (effect) {
      return (effect.safe_summary || friendlyLabel(effect.effect_kind));
    });
    appendReviewDetailList(cardNode, "Rollback", card.rollback_notes, function (note) {
      return note;
    });
  }

  function appendReviewDetailList(parent, label, values, mapper) {
    if (!values || !values.length) {
      return;
    }
    const detail = document.createElement("div");
    detail.className = "item-meta review-detail-list";
    detail.textContent = label + ": " + values.map(mapper).join(" / ");
    parent.appendChild(detail);
  }

  function appendApplyRiskDetails(cardNode, card) {
    if (card.card_kind !== "apply_risk_review") {
      return;
    }
    appendReviewMeta(cardNode, "Risk recommendation: " + friendlyLabel(card.risk_recommendation));
    appendReviewMeta(cardNode, "Approval outcome: " + friendlyLabel(card.final_outcome));
    appendReviewMeta(cardNode, "Manual eligibility: " + friendlyLabel(card.manual_eligibility_outcome));
    appendReviewMeta(cardNode, "Executor ready: " + String(card.executor_ready === true));
    appendReviewDetailList(cardNode, "Required approvals", card.required_approval_gate_codes, friendlyLabel);
    appendReviewDetailList(cardNode, "Satisfied approvals", card.satisfied_approval_gate_codes, friendlyLabel);
    appendReviewDetailList(cardNode, "Missing approvals", card.missing_approval_gate_codes, friendlyLabel);
    appendReviewDetailList(cardNode, "Stale checks", card.stale_reasons, friendlyLabel);
    appendReviewDetailList(cardNode, "Risk factors", card.risk_factors, function (factor) {
      return friendlyLabel(factor.risk_code) + ": " + friendlyLabel(factor.severity);
    });
  }

  function appendApplyAuditDetails(cardNode, card) {
    if (card.card_kind !== "apply_audit_manifest_entry") {
      return;
    }
    appendReviewMeta(cardNode, "Apply type: " + friendlyLabel(card.apply_type));
    appendReviewMeta(cardNode, "Source: " + card.source_artifact_id);
    appendReviewMeta(cardNode, "Reviewer: " + card.reviewer_id);
    appendReviewDetailList(cardNode, "Gate ids", [
      card.review_decision_id,
      card.eligibility_id,
      card.approval_id
    ], function (value) {
      return value;
    });
    appendReviewDetailList(cardNode, "Changed fields", card.changed_field_paths, function (value) {
      return value;
    });
    appendReviewDetailList(cardNode, "Affected memories", card.affected_memory_ids, function (value) {
      return value;
    });
    appendReviewDetailList(cardNode, "Rollback refs", objectPairs(card.rollback_refs), function (pair) {
      return pair.key + ": " + pair.value;
    });
  }

  function appendSessionCandidateReviewDetails(cardNode, card) {
    if (card.card_kind !== "session_candidate_review") {
      return;
    }
    appendReviewMeta(cardNode, "Candidate: " + friendlyLabel(card.candidate_kind));
    appendReviewMeta(cardNode, "Source: " + friendlyLabel(card.source_surface));
    appendReviewMeta(cardNode, "Origin turn: " + card.originating_turn_id);
    appendReviewMeta(cardNode, "Automatic apply: " + String(card.automatic_apply === true));
    appendReviewMeta(cardNode, "Sends messages: " + String(card.sends_messages === true));
  }

  function objectPairs(value) {
    return Object.keys(value || {}).sort().map(function (key) {
      return { key: key, value: value[key] };
    });
  }

  function appendReviewMeta(parent, value, extraClass) {
    const meta = document.createElement("div");
    meta.className = "item-meta" + (extraClass ? " " + extraClass : "");
    meta.textContent = value;
    parent.appendChild(meta);
  }

  function reviewCountsPlain(counts) {
    const entries = Object.keys(counts || {}).sort().map(function (key) {
      return friendlyLabel(key) + " " + counts[key];
    });
    return entries.length ? entries.join(", ") : "ids, labels, summaries, and counts only";
  }

  activateTabs();
  activateScenarios();
  setScenario("safe-review");
})();
