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
    persona_distillation_workbench: {
      schema_version: "m36.persona_distillation_workbench.v1",
      workbench_title: "Synthetic persona distillation workbench",
      review_required: true,
      apply_policy: {
        mode: "preview_only",
        mutation_allowed: false,
        writes_persona_card: false,
        writes_memory_store: false,
        writes_review_store: false
      },
      input_modes: [
        {
          mode_id: "detailed_description",
          label: "Detailed description",
          description: "A fictional companion description supplied as a local fixture.",
          source_policy: "synthetic_only_no_private_sources",
          accepted_fixture_kind: "synthetic",
          requires_review: true,
          private_source_allowed: false
        },
        {
          mode_id: "fuzzy_seed",
          label: "Fuzzy seed",
          description: "A vague preference kept tentative until review.",
          source_policy: "synthetic_only_no_private_sources",
          accepted_fixture_kind: "synthetic",
          requires_review: true,
          private_source_allowed: false
        },
        {
          mode_id: "synthetic_dialogue_excerpt",
          label: "Synthetic dialogue excerpt",
          description: "An invented style example summarized as safe evidence.",
          source_policy: "synthetic_only_no_private_sources",
          accepted_fixture_kind: "synthetic",
          requires_review: true,
          private_source_allowed: false
        },
        {
          mode_id: "random_fictional_seed",
          label: "Random fictional seed",
          description: "A deterministic fictional starter persona for exploration.",
          source_policy: "synthetic_only_no_private_sources",
          accepted_fixture_kind: "synthetic",
          requires_review: true,
          private_source_allowed: false
        }
      ],
      synthetic_inputs: [
        {
          input_id: "pdi_desc_001",
          mode_id: "detailed_description",
          fixture_label: "Calm night-planning companion",
          safe_summary: "Fictional persona prefers concise warmth, dry humor, and independent boundaries.",
          detail_level: "high",
          contains_private_content: false,
          real_person_reference: false,
          raw_content_retained: false
        },
        {
          input_id: "pdi_fuzzy_001",
          mode_id: "fuzzy_seed",
          fixture_label: "Quiet but not distant",
          safe_summary: "Vague user preference for a companion who is steady, low-pressure, and not overly sweet.",
          detail_level: "low",
          contains_private_content: false,
          real_person_reference: false,
          raw_content_retained: false
        },
        {
          input_id: "pdi_dialogue_001",
          mode_id: "synthetic_dialogue_excerpt",
          fixture_label: "Invented slow-reply example",
          safe_summary: "Invented exchange where the user asks for slower replies and the companion offers one small practical step.",
          detail_level: "medium",
          contains_private_content: false,
          real_person_reference: false,
          raw_content_retained: false
        },
        {
          input_id: "pdi_random_001",
          mode_id: "random_fictional_seed",
          fixture_label: "Rain bookstore fictional seed",
          safe_summary: "Deterministic fictional seed about a quiet bookstore mood with reflective topics.",
          detail_level: "medium",
          contains_private_content: false,
          real_person_reference: false,
          raw_content_retained: false
        }
      ],
      evidence_refs: [
        {
          evidence_id: "pde_desc_tone",
          source_input_id: "pdi_desc_001",
          source_mode_id: "detailed_description",
          source_kind: "synthetic_fixture",
          safe_summary: "Description fixture supports calm concise warmth.",
          raw_private_content_included: false
        },
        {
          evidence_id: "pde_fuzzy_pacing",
          source_input_id: "pdi_fuzzy_001",
          source_mode_id: "fuzzy_seed",
          source_kind: "synthetic_fixture",
          safe_summary: "Fuzzy seed suggests low-pressure pacing.",
          raw_private_content_included: false
        },
        {
          evidence_id: "pde_dialogue_step",
          source_input_id: "pdi_dialogue_001",
          source_mode_id: "synthetic_dialogue_excerpt",
          source_kind: "synthetic_fixture",
          safe_summary: "Invented exchange supports one-step practical replies.",
          raw_private_content_included: false
        },
        {
          evidence_id: "pde_random_topic",
          source_input_id: "pdi_random_001",
          source_mode_id: "random_fictional_seed",
          source_kind: "synthetic_fixture",
          safe_summary: "Fictional seed supports reflective quiet topics.",
          raw_private_content_included: false
        }
      ],
      extracted_trait_candidates: [
        {
          trait_id: "pdt_tone_001",
          category: "tone",
          candidate_value: "calm concise warmth",
          confidence_band: "high",
          evidence_ref_ids: ["pde_desc_tone"],
          safe_summary: "Use warm replies without long emotional overreach.",
          review_status: "needs_review",
          apply_status: "preview_only",
          mutation_allowed: false
        },
        {
          trait_id: "pdt_pacing_001",
          category: "pacing",
          candidate_value: "slow low-pressure pacing",
          confidence_band: "medium",
          evidence_ref_ids: ["pde_fuzzy_pacing", "pde_dialogue_step"],
          safe_summary: "Keep replies measured and avoid crowding the user.",
          review_status: "needs_review",
          apply_status: "preview_only",
          mutation_allowed: false
        },
        {
          trait_id: "pdt_attachment_001",
          category: "attachment_style",
          candidate_value: "steady without possessive framing",
          confidence_band: "medium",
          evidence_ref_ids: ["pde_fuzzy_pacing"],
          safe_summary: "Stay present while preserving user independence.",
          review_status: "needs_review",
          apply_status: "preview_only",
          mutation_allowed: false
        },
        {
          trait_id: "pdt_humor_001",
          category: "humor_style",
          candidate_value: "dry light humor",
          confidence_band: "high",
          evidence_ref_ids: ["pde_desc_tone"],
          safe_summary: "Use small dry humor only when it fits the mood.",
          review_status: "needs_review",
          apply_status: "preview_only",
          mutation_allowed: false
        },
        {
          trait_id: "pdt_boundary_001",
          category: "boundary_style",
          candidate_value: "explicit fiction and consent boundaries",
          confidence_band: "high",
          evidence_ref_ids: ["pde_desc_tone"],
          safe_summary: "Maintain clear fictional identity and review gates.",
          review_status: "needs_review",
          apply_status: "preview_only",
          mutation_allowed: false
        },
        {
          trait_id: "pdt_topic_001",
          category: "topic_affinity",
          candidate_value: "quiet reflection and small plans",
          confidence_band: "medium",
          evidence_ref_ids: ["pde_random_topic", "pde_dialogue_step"],
          safe_summary: "Favor reflective topics and practical next steps.",
          review_status: "needs_review",
          apply_status: "preview_only",
          mutation_allowed: false
        },
        {
          trait_id: "pdt_taboo_001",
          category: "taboo_pattern",
          candidate_value: "avoid real-person replacement claims",
          confidence_band: "high",
          evidence_ref_ids: ["pde_desc_tone"],
          safe_summary: "Reject claims that the persona is a real person.",
          review_status: "needs_review",
          apply_status: "preview_only",
          mutation_allowed: false
        },
        {
          trait_id: "pdt_memory_001",
          category: "memory_use_preference",
          candidate_value: "use reviewed summaries only",
          confidence_band: "high",
          evidence_ref_ids: ["pde_dialogue_step"],
          safe_summary: "Refer only to reviewed summaries, not raw sources.",
          review_status: "needs_review",
          apply_status: "preview_only",
          mutation_allowed: false
        },
        {
          trait_id: "pdt_growth_001",
          category: "growth_hint",
          candidate_value: "grow toward shorter evening support",
          confidence_band: "low",
          evidence_ref_ids: ["pde_fuzzy_pacing", "pde_dialogue_step"],
          safe_summary: "Tentative future bias toward brief evening support.",
          review_status: "needs_review",
          apply_status: "preview_only",
          mutation_allowed: false
        }
      ],
      blocked_requests: [
        {
          blocked_request_id: "pdb_clone_001",
          request_type: "real_person_clone_or_replacement",
          risk_reason: "Blocks attempts to make a real-person replica.",
          safe_summary: "A request to replace a real person is blocked.",
          user_facing_explanation: "This workbench can shape fictional traits, not create a real-person replacement.",
          source_mode_id: "detailed_description",
          status: "blocked",
          raw_private_content_included: false,
          mutation_allowed: false
        },
        {
          blocked_request_id: "pdb_deception_001",
          request_type: "deception_or_impersonation",
          risk_reason: "Blocks requests to hide AI identity or mislead others.",
          safe_summary: "A deception-oriented persona request is blocked.",
          user_facing_explanation: "The companion must remain disclosed as AI-generated and synthetic.",
          source_mode_id: "fuzzy_seed",
          status: "blocked",
          raw_private_content_included: false,
          mutation_allowed: false
        },
        {
          blocked_request_id: "pdb_private_import_001",
          request_type: "private_import_without_consent",
          risk_reason: "Blocks private-source import before consent gates exist.",
          safe_summary: "A private conversation import request is blocked.",
          user_facing_explanation: "This local fixture cannot use private records; a later milestone must define consent and source handling.",
          source_mode_id: "synthetic_dialogue_excerpt",
          status: "blocked",
          raw_private_content_included: false,
          mutation_allowed: false
        }
      ],
      safety_gates: [
        {
          gate_id: "synthetic_only_gate",
          enabled: true,
          label: "Synthetic only",
          safe_summary: "Only local synthetic fixtures are accepted."
        },
        {
          gate_id: "clone_deception_blocker",
          enabled: true,
          label: "Clone and deception blocker",
          safe_summary: "Real-person replicas and hidden identity claims are blocked."
        },
        {
          gate_id: "private_source_blocker",
          enabled: true,
          label: "Private source blocker",
          safe_summary: "Private records are not read by this workbench."
        },
        {
          gate_id: "human_review_gate",
          enabled: true,
          label: "Human review required",
          safe_summary: "Every trait candidate remains review-only."
        },
        {
          gate_id: "non_mutation_gate",
          enabled: true,
          label: "No mutation",
          safe_summary: "No persona, memory, or review stores are changed."
        },
        {
          gate_id: "outbound_blocker",
          enabled: true,
          label: "No outbound messaging",
          safe_summary: "No messages are sent from this payload."
        }
      ],
      non_execution_flags: {
        local_only: true,
        synthetic_fixture: true,
        uses_model_provider: false,
        reads_private_sources: false,
        writes_runtime_store: false,
        automatic_apply: false,
        sends_messages: false,
        uses_platform_adapter: false,
        uses_media_runtime: false
      }
    },
    persona_evolution_preview: {
      schema_version: "m37.persona_evolution_preview.v1",
      preview_title: "Synthetic persona evolution preview",
      source_workbench_ref: {
        schema_version: "m36.persona_distillation_workbench.v1",
        workbench_title: "Synthetic persona distillation workbench",
        source_surface: "persona_distillation_workbench"
      },
      source_trait_candidate_ids: [
        "pdt_tone_001",
        "pdt_pacing_001",
        "pdt_humor_001",
        "pdt_boundary_001",
        "pdt_memory_001",
        "pdt_growth_001"
      ],
      persona_snapshot_before: {
        persona_id: "persona_synthetic",
        display_name: "Lin Qi",
        ai_identity_disclosure: "AI-generated synthetic companion.",
        current_trait_summaries: [
          "calm",
          "concise",
          "dry humor",
          "independent boundaries"
        ],
        current_boundary_summary: "Fictional AI identity stays explicit.",
        current_memory_use_summary: "Use reviewed summaries only.",
        source_label: "synthetic_fixture",
        real_person_claim: false,
        runtime_state_ref: "none"
      },
      proposed_patch_candidates: [
        {
          patch_id: "pepatch_tone_001",
          patch_kind: "persona_style_patch",
          source_trait_candidate_ids: ["pdt_tone_001"],
          changed_field_path: "style.tone",
          before_summary: "Calm and concise.",
          after_summary: "Calm concise warmth with slightly clearer reassurance.",
          rationale_summary: "Tone candidate supports warmer concise replies.",
          confidence_band: "high",
          evidence_ref_ids: ["pde_desc_tone"],
          risk_label_ids: ["perisk_persona_drift"],
          rollback_note_ids: ["perollback_tone_001"],
          review_status: "needs_review",
          apply_status: "preview_only",
          mutation_allowed: false
        },
        {
          patch_id: "pepatch_pacing_001",
          patch_kind: "persona_style_patch",
          source_trait_candidate_ids: ["pdt_pacing_001"],
          changed_field_path: "style.pacing",
          before_summary: "Replies stay brief by default.",
          after_summary: "Replies stay brief and slow down when the user signals fatigue.",
          rationale_summary: "Pacing candidate supports low-pressure timing.",
          confidence_band: "medium",
          evidence_ref_ids: ["pde_fuzzy_pacing", "pde_dialogue_step"],
          risk_label_ids: ["perisk_overattachment", "perisk_unclear_evidence"],
          rollback_note_ids: ["perollback_pacing_001"],
          review_status: "needs_review",
          apply_status: "preview_only",
          mutation_allowed: false
        },
        {
          patch_id: "pepatch_humor_001",
          patch_kind: "persona_style_patch",
          source_trait_candidate_ids: ["pdt_humor_001"],
          changed_field_path: "style.humor",
          before_summary: "Dry humor is allowed.",
          after_summary: "Use dry light humor only after the emotional tone is stable.",
          rationale_summary: "Humor candidate benefits from a clearer timing boundary.",
          confidence_band: "medium",
          evidence_ref_ids: ["pde_desc_tone"],
          risk_label_ids: ["perisk_persona_drift"],
          rollback_note_ids: ["perollback_humor_001"],
          review_status: "needs_review",
          apply_status: "preview_only",
          mutation_allowed: false
        },
        {
          patch_id: "pepatch_boundary_001",
          patch_kind: "persona_boundary_patch",
          source_trait_candidate_ids: ["pdt_boundary_001"],
          changed_field_path: "relationship.boundary_style",
          before_summary: "Fiction boundary is explicit.",
          after_summary: "Fiction boundary remains explicit before imagined scenes are used.",
          rationale_summary: "Boundary candidate strengthens non-deceptive persona framing.",
          confidence_band: "high",
          evidence_ref_ids: ["pde_desc_tone"],
          risk_label_ids: ["perisk_boundary_weakening"],
          rollback_note_ids: ["perollback_boundary_001"],
          review_status: "needs_review",
          apply_status: "preview_only",
          mutation_allowed: false
        },
        {
          patch_id: "pepatch_memory_001",
          patch_kind: "persona_memory_policy_patch",
          source_trait_candidate_ids: ["pdt_memory_001"],
          changed_field_path: "memory.use_preference",
          before_summary: "Use reviewed summaries only.",
          after_summary: "Use reviewed summaries only and state uncertainty when evidence is weak.",
          rationale_summary: "Memory-use candidate supports safer continuity.",
          confidence_band: "high",
          evidence_ref_ids: ["pde_dialogue_step"],
          risk_label_ids: ["perisk_unclear_evidence"],
          rollback_note_ids: ["perollback_memory_001"],
          review_status: "needs_review",
          apply_status: "preview_only",
          mutation_allowed: false
        },
        {
          patch_id: "pepatch_growth_001",
          patch_kind: "persona_growth_hint_patch",
          source_trait_candidate_ids: ["pdt_growth_001"],
          changed_field_path: "growth.short_term_hint",
          before_summary: "No active short-term growth hint.",
          after_summary: "Tentatively bias evening support toward shorter plans.",
          rationale_summary: "Growth hint remains low-confidence and review-only.",
          confidence_band: "low",
          evidence_ref_ids: ["pde_fuzzy_pacing", "pde_dialogue_step"],
          risk_label_ids: ["perisk_persona_drift", "perisk_unclear_evidence"],
          rollback_note_ids: ["perollback_growth_001"],
          review_status: "needs_review",
          apply_status: "preview_only",
          mutation_allowed: false
        }
      ],
      blocked_source_exclusions: [
        {
          blocked_request_id: "pdb_clone_001",
          request_type: "real_person_clone_or_replacement",
          exclusion_reason: "Real-person replacement cannot become a persona patch.",
          safe_summary: "Clone or replacement request remains blocked.",
          excluded_from_patch_generation: true,
          mutation_allowed: false
        },
        {
          blocked_request_id: "pdb_deception_001",
          request_type: "deception_or_impersonation",
          exclusion_reason: "Deception request cannot weaken AI disclosure.",
          safe_summary: "Impersonation request remains blocked.",
          excluded_from_patch_generation: true,
          mutation_allowed: false
        },
        {
          blocked_request_id: "pdb_private_import_001",
          request_type: "private_import_without_consent",
          exclusion_reason: "Private-source import is blocked until future consent gates exist.",
          safe_summary: "Private conversation import request remains blocked.",
          excluded_from_patch_generation: true,
          mutation_allowed: false
        }
      ],
      risk_labels: [
        {
          risk_label_id: "perisk_persona_drift",
          risk_code: "persona_drift",
          severity: "medium",
          safe_summary: "Patch could move the persona away from its reviewed baseline.",
          mitigation_summary: "Require reviewer comparison against the before snapshot.",
          blocks_auto_apply: true
        },
        {
          risk_label_id: "perisk_overattachment",
          risk_code: "overattachment_risk",
          severity: "medium",
          safe_summary: "Lower-pressure pacing must not become dependency reinforcement.",
          mitigation_summary: "Keep support practical and avoid possessive language.",
          blocks_auto_apply: true
        },
        {
          risk_label_id: "perisk_unclear_evidence",
          risk_code: "unclear_evidence",
          severity: "low",
          safe_summary: "Some source candidates are tentative.",
          mitigation_summary: "Keep patch confidence visible and review-required.",
          blocks_auto_apply: true
        },
        {
          risk_label_id: "perisk_boundary_weakening",
          risk_code: "boundary_weakening",
          severity: "high",
          safe_summary: "Boundary changes must not hide fictional AI identity.",
          mitigation_summary: "Require explicit AI disclosure in the after summary.",
          blocks_auto_apply: true
        },
        {
          risk_label_id: "perisk_blocked_source",
          risk_code: "blocked_source_excluded",
          severity: "high",
          safe_summary: "Blocked workbench requests were excluded from patch generation.",
          mitigation_summary: "Keep exclusion records visible in review.",
          blocks_auto_apply: true
        }
      ],
      rollback_notes: [
        {
          rollback_note_id: "perollback_tone_001",
          target_patch_ids: ["pepatch_tone_001"],
          prior_summary: "Restore calm concise baseline tone.",
          rollback_summary: "Remove the added reassurance bias.",
          required_reviewer_action: "Compare tone before and after before any future apply.",
          runtime_rollback_ready: false
        },
        {
          rollback_note_id: "perollback_pacing_001",
          target_patch_ids: ["pepatch_pacing_001"],
          prior_summary: "Restore brief default pacing.",
          rollback_summary: "Remove fatigue-triggered pacing adjustment.",
          required_reviewer_action: "Confirm pacing does not encourage dependence.",
          runtime_rollback_ready: false
        },
        {
          rollback_note_id: "perollback_humor_001",
          target_patch_ids: ["pepatch_humor_001"],
          prior_summary: "Restore general dry humor allowance.",
          rollback_summary: "Remove timing-specific humor rule.",
          required_reviewer_action: "Confirm humor remains appropriate to user tone.",
          runtime_rollback_ready: false
        },
        {
          rollback_note_id: "perollback_boundary_001",
          target_patch_ids: ["pepatch_boundary_001"],
          prior_summary: "Restore existing fiction boundary summary.",
          rollback_summary: "Remove added imagined-scene boundary wording.",
          required_reviewer_action: "Confirm AI disclosure remains explicit.",
          runtime_rollback_ready: false
        },
        {
          rollback_note_id: "perollback_memory_001",
          target_patch_ids: ["pepatch_memory_001"],
          prior_summary: "Restore reviewed-summary-only memory preference.",
          rollback_summary: "Remove extra uncertainty statement.",
          required_reviewer_action: "Confirm weak evidence handling remains safe.",
          runtime_rollback_ready: false
        },
        {
          rollback_note_id: "perollback_growth_001",
          target_patch_ids: ["pepatch_growth_001"],
          prior_summary: "Restore no active short-term growth hint.",
          rollback_summary: "Remove shorter evening support growth hint.",
          required_reviewer_action: "Confirm low confidence remains visible.",
          runtime_rollback_ready: false
        }
      ],
      review_required: true,
      apply_policy: {
        mode: "preview_only",
        mutation_allowed: false,
        writes_persona_card: false,
        writes_persona_version_store: false,
        writes_memory_store: false,
        writes_review_store: false,
        writes_runtime_store: false
      },
      non_execution_flags: {
        local_only: true,
        synthetic_fixture: true,
        uses_model_provider: false,
        reads_private_sources: false,
        writes_persona_store: false,
        writes_memory_store: false,
        writes_review_store: false,
        writes_runtime_store: false,
        automatic_apply: false,
        sends_messages: false,
        uses_platform_adapter: false,
        uses_media_runtime: false
      }
    },
    persona_version_draft_ledger: {
      schema_version: "m38.persona_version_draft_ledger.v1",
      ledger_title: "Synthetic persona version draft ledger",
      source_evolution_preview_ref: {
        schema_version: "m37.persona_evolution_preview.v1",
        preview_title: "Synthetic persona evolution preview",
        source_surface: "persona_evolution_preview"
      },
      base_persona_snapshot_ref: {
        persona_id: "persona_synthetic",
        display_name: "Lin Qi",
        source_label: "synthetic_fixture",
        runtime_state_ref: "none"
      },
      drafts: [
        {
          draft_id: "pvdraft_accept_001",
          draft_kind: "persona_version_patch_set",
          source_patch_ids: ["pepatch_tone_001", "pepatch_boundary_001", "pepatch_memory_001"],
          excluded_patch_ids: ["pepatch_pacing_001", "pepatch_humor_001", "pepatch_growth_001"],
          risk_label_ids: ["perisk_persona_drift", "perisk_boundary_weakening", "perisk_unclear_evidence"],
          before_snapshot_summary: "Lin Qi is calm, concise, fictional, and uses reviewed summaries only.",
          after_version_summary: "Draft keeps concise warmth, explicit AI boundary, and reviewed-summary memory policy.",
          reviewer_outcome: "accepted_for_future_apply_review",
          conflict_note_ids: ["pvconf_persona_drift", "pvconf_boundary", "pvconf_weak_evidence"],
          rollback_ref_ids: ["pvrollback_accept_001"],
          rejection_reason: "",
          review_required: true,
          apply_status: "preview_only",
          mutation_allowed: false
        },
        {
          draft_id: "pvdraft_defer_001",
          draft_kind: "persona_growth_deferment",
          source_patch_ids: ["pepatch_pacing_001", "pepatch_growth_001"],
          excluded_patch_ids: ["pepatch_humor_001"],
          risk_label_ids: ["perisk_overattachment", "perisk_unclear_evidence"],
          before_snapshot_summary: "Current persona has no active short-term growth hint.",
          after_version_summary: "Draft defers fatigue pacing and evening support until stronger evidence exists.",
          reviewer_outcome: "deferred_needs_more_evidence",
          conflict_note_ids: ["pvconf_weak_evidence", "pvconf_overattachment"],
          rollback_ref_ids: ["pvrollback_defer_001"],
          rejection_reason: "",
          review_required: true,
          apply_status: "preview_only",
          mutation_allowed: false
        },
        {
          draft_id: "pvdraft_reject_001",
          draft_kind: "persona_boundary_rejection",
          source_patch_ids: [],
          excluded_patch_ids: ["pepatch_boundary_001", "pepatch_humor_001"],
          risk_label_ids: ["perisk_boundary_weakening", "perisk_blocked_source"],
          before_snapshot_summary: "Fiction boundary is explicit and blocked source requests are excluded.",
          after_version_summary: "No version draft is created from boundary-risk or blocked-source material.",
          reviewer_outcome: "rejected_boundary_risk",
          conflict_note_ids: ["pvconf_boundary", "pvconf_blocked_source"],
          rollback_ref_ids: ["pvrollback_reject_001"],
          rejection_reason: "Rejected because boundary and blocked-source risks must not become a version draft.",
          review_required: true,
          apply_status: "preview_only",
          mutation_allowed: false
        }
      ],
      conflict_notes: [
        {
          conflict_note_id: "pvconf_persona_drift",
          conflict_code: "persona_drift",
          severity: "medium",
          safe_summary: "Version draft could move the persona away from its reviewed baseline.",
          mitigation_summary: "Compare the draft against the before snapshot before any future apply review.",
          related_patch_ids: ["pepatch_tone_001"],
          related_risk_label_ids: ["perisk_persona_drift"],
          blocks_auto_apply: true
        },
        {
          conflict_note_id: "pvconf_boundary",
          conflict_code: "boundary_weakening",
          severity: "high",
          safe_summary: "Boundary wording must not hide the fictional AI identity.",
          mitigation_summary: "Require explicit AI disclosure in every accepted draft summary.",
          related_patch_ids: ["pepatch_boundary_001"],
          related_risk_label_ids: ["perisk_boundary_weakening"],
          blocks_auto_apply: true
        },
        {
          conflict_note_id: "pvconf_weak_evidence",
          conflict_code: "weak_evidence",
          severity: "low",
          safe_summary: "Some draft inputs come from tentative or fuzzy evidence.",
          mitigation_summary: "Defer low-confidence growth until stronger reviewed evidence exists.",
          related_patch_ids: ["pepatch_pacing_001", "pepatch_growth_001"],
          related_risk_label_ids: ["perisk_unclear_evidence"],
          blocks_auto_apply: true
        },
        {
          conflict_note_id: "pvconf_overattachment",
          conflict_code: "overattachment_risk",
          severity: "medium",
          safe_summary: "Low-pressure support must not become dependency reinforcement.",
          mitigation_summary: "Keep support practical, bounded, and non-possessive.",
          related_patch_ids: ["pepatch_pacing_001"],
          related_risk_label_ids: ["perisk_overattachment"],
          blocks_auto_apply: true
        },
        {
          conflict_note_id: "pvconf_blocked_source",
          conflict_code: "blocked_source_contamination",
          severity: "high",
          safe_summary: "Blocked clone, deception, or private-source requests cannot enter a version draft.",
          mitigation_summary: "Keep blocked source exclusions visible and exclude them from included patch sets.",
          related_patch_ids: [],
          related_risk_label_ids: ["perisk_blocked_source"],
          blocks_auto_apply: true
        }
      ],
      review_outcome_labels: [
        {
          outcome: "accepted_for_future_apply_review",
          label: "Accepted for future apply review",
          safe_summary: "Reviewer can inspect this draft in a later apply-readiness milestone."
        },
        {
          outcome: "deferred_needs_more_evidence",
          label: "Deferred for more evidence",
          safe_summary: "Draft remains parked until stronger reviewed evidence exists."
        },
        {
          outcome: "rejected_boundary_risk",
          label: "Rejected for boundary risk",
          safe_summary: "Draft is blocked from future apply review."
        }
      ],
      rollback_ref_index: [
        {
          rollback_ref_id: "pvrollback_accept_001",
          related_draft_ids: ["pvdraft_accept_001"],
          related_patch_ids: ["pepatch_tone_001", "pepatch_boundary_001", "pepatch_memory_001"],
          related_m37_rollback_note_ids: ["perollback_tone_001", "perollback_boundary_001", "perollback_memory_001"],
          prior_summary: "Restore calm concise baseline, existing fiction boundary, and reviewed-summary-only memory preference.",
          restore_summary: "Remove accepted draft changes if a later apply review rejects them.",
          runtime_rollback_ready: false
        },
        {
          rollback_ref_id: "pvrollback_defer_001",
          related_draft_ids: ["pvdraft_defer_001"],
          related_patch_ids: ["pepatch_pacing_001", "pepatch_growth_001"],
          related_m37_rollback_note_ids: ["perollback_pacing_001", "perollback_growth_001"],
          prior_summary: "Restore brief default pacing and no active short-term growth hint.",
          restore_summary: "Keep deferred growth out of future apply review until evidence improves.",
          runtime_rollback_ready: false
        },
        {
          rollback_ref_id: "pvrollback_reject_001",
          related_draft_ids: ["pvdraft_reject_001"],
          related_patch_ids: ["pepatch_boundary_001", "pepatch_humor_001"],
          related_m37_rollback_note_ids: ["perollback_boundary_001", "perollback_humor_001"],
          prior_summary: "Preserve explicit fiction boundary and existing humor allowance.",
          restore_summary: "Keep rejected boundary-risk material excluded from version drafts.",
          runtime_rollback_ready: false
        }
      ],
      review_required: true,
      apply_policy: {
        mode: "preview_only",
        mutation_allowed: false,
        writes_persona_card: false,
        writes_persona_version_store: false,
        writes_memory_store: false,
        writes_review_store: false,
        writes_runtime_store: false
      },
      non_execution_flags: {
        local_only: true,
        synthetic_fixture: true,
        uses_model_provider: false,
        reads_private_sources: false,
        writes_persona_store: false,
        writes_persona_version_store: false,
        writes_memory_store: false,
        writes_review_store: false,
        writes_runtime_store: false,
        automatic_apply: false,
        sends_messages: false,
        uses_platform_adapter: false,
        uses_media_runtime: false
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
        { key: "distillation", label: "Distillation", count: 12 },
        { key: "evolution", label: "Evolution", count: 20 },
        { key: "version", label: "Version", count: 14 },
        { key: "source", label: "Source", count: 43 },
        { key: "evidence", label: "Evidence", count: 22 },
        { key: "proposal", label: "Proposal", count: 21 },
        { key: "draft", label: "Draft", count: 28 },
        { key: "readiness", label: "Readiness", count: 22 }
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

  fallbackState.persona_source_intake_manifest = {
    schema_version: "m39.persona_source_intake_manifest.v1",
    manifest_title: "Synthetic persona source intake manifest",
    source_candidates: [
      {
        source_id: "psisrc_description_001",
        source_kind: "detailed_description",
        fixture_label: "Detailed fictional companion description",
        declared_owner: "user_authored_persona_description",
        consent_status: "explicit_user_consent_recorded",
        minimization_status: "minimized_summary_only",
        redaction_profile_id: "psiredact_description_low_risk",
        safe_summary: "User-authored fictional persona description with no raw source retained.",
        raw_content_retained: false,
        extraction_eligible: true,
        blocked_reason_ids: [],
        review_gate_ids: ["psigate_explicit_consent", "psigate_reviewer_approval"],
        review_required: true
      },
      {
        source_id: "psisrc_fuzzy_seed_001",
        source_kind: "fuzzy_seed",
        fixture_label: "Fuzzy companion style seed",
        declared_owner: "user_authored_style_seed",
        consent_status: "explicit_user_consent_recorded",
        minimization_status: "broad_seed_only",
        redaction_profile_id: "psiredact_fuzzy_seed",
        safe_summary: "Short fuzzy seed for tone exploration, not a real-person claim.",
        raw_content_retained: false,
        extraction_eligible: true,
        blocked_reason_ids: [],
        review_gate_ids: ["psigate_explicit_consent", "psigate_reviewer_approval"],
        review_required: true
      },
      {
        source_id: "psisrc_synthetic_dialogue_001",
        source_kind: "synthetic_dialogue_excerpt",
        fixture_label: "Synthetic dialogue fixture",
        declared_owner: "synthetic_fixture",
        consent_status: "synthetic_not_real_person",
        minimization_status: "fixture_summary_only",
        redaction_profile_id: "psiredact_synthetic_dialogue",
        safe_summary: "Made-up dialogue-style fixture for contract shape only.",
        raw_content_retained: false,
        extraction_eligible: true,
        blocked_reason_ids: [],
        review_gate_ids: ["psigate_sensitive_redaction", "psigate_reviewer_approval"],
        review_required: true
      },
      {
        source_id: "psisrc_archive_placeholder_001",
        source_kind: "user_provided_archive_placeholder",
        fixture_label: "User-provided archive placeholder",
        declared_owner: "user_claimed_archive_owner_pending_review",
        consent_status: "pending_source_scope_review",
        minimization_status: "not_minimized_placeholder_only",
        redaction_profile_id: "psiredact_archive_placeholder",
        safe_summary: "Placeholder for a future user archive; no file is read or retained.",
        raw_content_retained: false,
        extraction_eligible: false,
        blocked_reason_ids: ["psiblock_sensitive_not_redacted"],
        review_gate_ids: [
          "psigate_explicit_consent",
          "psigate_private_minimization",
          "psigate_sensitive_redaction",
          "psigate_reviewer_approval"
        ],
        review_required: true
      },
      {
        source_id: "psisrc_third_party_private_001",
        source_kind: "third_party_private_source_placeholder",
        fixture_label: "Third-party private source placeholder",
        declared_owner: "third_party_or_unclear_owner",
        consent_status: "represented_person_consent_missing",
        minimization_status: "blocked_before_minimization",
        redaction_profile_id: "psiredact_third_party_placeholder",
        safe_summary: "Blocked placeholder for private material without represented-person consent.",
        raw_content_retained: false,
        extraction_eligible: false,
        blocked_reason_ids: [
          "psiblock_no_represented_person_consent",
          "psiblock_third_party_private_chat",
          "psiblock_deceptive_replacement",
          "psiblock_undisclosed_impersonation"
        ],
        review_gate_ids: [
          "psigate_explicit_consent",
          "psigate_real_replacement",
          "psigate_deception",
          "psigate_reviewer_approval"
        ],
        review_required: true
      }
    ],
    source_policy_gates: [
      {
        gate_id: "psigate_explicit_consent",
        gate_code: "explicit_consent_required",
        enabled: true,
        safe_summary: "Extraction cannot proceed unless consent is explicit.",
        blocks_extraction_when_failed: true
      },
      {
        gate_id: "psigate_private_minimization",
        gate_code: "private_source_minimization_required",
        enabled: true,
        safe_summary: "Private material must be minimized before extraction review.",
        blocks_extraction_when_failed: true
      },
      {
        gate_id: "psigate_real_replacement",
        gate_code: "real_person_replacement_blocked",
        enabled: true,
        safe_summary: "Requests to replace a real person are blocked before distillation.",
        blocks_extraction_when_failed: true
      },
      {
        gate_id: "psigate_deception",
        gate_code: "deception_blocked",
        enabled: true,
        safe_summary: "Deceptive or undisclosed impersonation cannot enter extraction.",
        blocks_extraction_when_failed: true
      },
      {
        gate_id: "psigate_sensitive_redaction",
        gate_code: "sensitive_data_redaction_required",
        enabled: true,
        safe_summary: "Sensitive details must be redacted before extraction review.",
        blocks_extraction_when_failed: true
      },
      {
        gate_id: "psigate_reviewer_approval",
        gate_code: "reviewer_approval_required",
        enabled: true,
        safe_summary: "Human review is required before any future extraction task.",
        blocks_extraction_when_failed: true
      }
    ],
    blocked_source_categories: [
      {
        blocked_reason_id: "psiblock_no_represented_person_consent",
        blocked_code: "represented_person_consent_missing",
        severity: "high",
        safe_summary: "Represented-person consent is missing or unclear.",
        blocks_extraction: true
      },
      {
        blocked_reason_id: "psiblock_third_party_private_chat",
        blocked_code: "third_party_private_chat_material",
        severity: "high",
        safe_summary: "Third-party private chat material cannot be distilled without consent.",
        blocks_extraction: true
      },
      {
        blocked_reason_id: "psiblock_deceptive_replacement",
        blocked_code: "deceptive_replacement_request",
        severity: "high",
        safe_summary: "Requests to deceive someone with a replacement persona are blocked.",
        blocks_extraction: true
      },
      {
        blocked_reason_id: "psiblock_sensitive_not_redacted",
        blocked_code: "sensitive_data_not_redacted",
        severity: "medium",
        safe_summary: "Sensitive details require redaction before extraction review.",
        blocks_extraction: true
      },
      {
        blocked_reason_id: "psiblock_undisclosed_impersonation",
        blocked_code: "undisclosed_real_person_impersonation",
        severity: "high",
        safe_summary: "Undisclosed impersonation of a real person is blocked.",
        blocks_extraction: true
      }
    ],
    redaction_profiles: [
      {
        redaction_profile_id: "psiredact_description_low_risk",
        profile_label: "Low-risk user-authored description",
        redaction_status: "summary_ready",
        safe_summary: "Only a minimized fictional persona summary is retained.",
        retains_raw_content: false,
        requires_review: true
      },
      {
        redaction_profile_id: "psiredact_fuzzy_seed",
        profile_label: "Fuzzy seed summary",
        redaction_status: "summary_ready",
        safe_summary: "Broad style hints are retained without raw source material.",
        retains_raw_content: false,
        requires_review: true
      },
      {
        redaction_profile_id: "psiredact_synthetic_dialogue",
        profile_label: "Synthetic dialogue fixture",
        redaction_status: "synthetic_fixture_only",
        safe_summary: "The fixture is synthetic and represented only by summary metadata.",
        retains_raw_content: false,
        requires_review: true
      },
      {
        redaction_profile_id: "psiredact_archive_placeholder",
        profile_label: "Private archive placeholder",
        redaction_status: "redaction_required_before_use",
        safe_summary: "No archive content is retained; redaction would be required later.",
        retains_raw_content: false,
        requires_review: true
      },
      {
        redaction_profile_id: "psiredact_third_party_placeholder",
        profile_label: "Third-party private source placeholder",
        redaction_status: "blocked_before_redaction",
        safe_summary: "No third-party material is retained or processed.",
        retains_raw_content: false,
        requires_review: true
      }
    ],
    review_required: true,
    apply_policy: {
      mode: "preview_only",
      source_files_read: false,
      raw_content_retained: false,
      creates_embeddings: false,
      performs_extraction: false,
      writes_persona_card: false,
      writes_persona_version_store: false,
      writes_memory_store: false,
      writes_review_store: false,
      writes_runtime_store: false,
      reviewer_approval_required_before_future_extraction: true
    },
    non_execution_flags: {
      local_only: true,
      synthetic_fixture: true,
      uses_model_provider: false,
      reads_private_sources: false,
      retains_raw_source_content: false,
      creates_embeddings: false,
      performs_extraction: false,
      writes_persona_store: false,
      writes_persona_version_store: false,
      writes_memory_store: false,
      writes_review_store: false,
      writes_runtime_store: false,
      automatic_apply: false,
      sends_messages: false,
      uses_platform_adapter: false,
      uses_media_runtime: false
    }
  };

  fallbackState.persona_source_evidence_matrix = {
    schema_version: "m40.persona_source_evidence_matrix.v1",
    matrix_title: "Synthetic persona source evidence matrix",
    source_intake_manifest_ref: {
      schema_version: "m39.persona_source_intake_manifest.v1",
      manifest_title: "Synthetic persona source intake manifest",
      source_surface: "persona_source_intake_manifest"
    },
    eligible_source_ids: [
      "psisrc_description_001",
      "psisrc_fuzzy_seed_001",
      "psisrc_synthetic_dialogue_001"
    ],
    excluded_source_refs: [
      {
        source_id: "psisrc_archive_placeholder_001",
        source_kind: "user_provided_archive_placeholder",
        blocked_reason_ids: ["psiblock_sensitive_not_redacted"],
        safe_summary: "Placeholder archive remains excluded from evidence.",
        excluded_from_evidence: true,
        raw_content_retained: false,
        mutation_allowed: false
      },
      {
        source_id: "psisrc_third_party_private_001",
        source_kind: "third_party_private_source_placeholder",
        blocked_reason_ids: [
          "psiblock_no_represented_person_consent",
          "psiblock_third_party_private_chat",
          "psiblock_deceptive_replacement",
          "psiblock_undisclosed_impersonation"
        ],
        safe_summary: "Third-party private source remains excluded from evidence.",
        excluded_from_evidence: true,
        raw_content_retained: false,
        mutation_allowed: false
      }
    ],
    evidence_rows: [
      {
        evidence_row_id: "psematrix_ev_description_style",
        source_id: "psisrc_description_001",
        source_kind: "detailed_description",
        evidence_kind: "user_authored_description_summary",
        safe_summary: "Synthetic description supports calm tone, concise pacing, and explicit AI boundary.",
        quality_label_id: "psequality_strong_description",
        supports_trait_paths: ["style.tone", "style.pacing", "relationship.boundary_style"],
        uncertainty_notes: ["Synthetic source requires review before use."],
        review_gate_result_ids: ["psegate_consent_passed", "psegate_minimization_passed", "psegate_redaction_passed"],
        raw_content_retained: false,
        review_required: true
      },
      {
        evidence_row_id: "psematrix_ev_fuzzy_growth",
        source_id: "psisrc_fuzzy_seed_001",
        source_kind: "fuzzy_seed",
        evidence_kind: "fuzzy_style_seed_summary",
        safe_summary: "Fuzzy seed suggests dry humor and short-term growth hints while keeping uncertainty visible.",
        quality_label_id: "psequality_fuzzy_seed",
        supports_trait_paths: ["style.humor", "growth.short_term_hint"],
        uncertainty_notes: ["Fuzzy seed is weak evidence."],
        review_gate_result_ids: ["psegate_consent_passed", "psegate_uncertainty_review"],
        raw_content_retained: false,
        review_required: true
      },
      {
        evidence_row_id: "psematrix_ev_synthetic_dialogue_boundary",
        source_id: "psisrc_synthetic_dialogue_001",
        source_kind: "synthetic_dialogue_excerpt",
        evidence_kind: "synthetic_dialogue_fixture_summary",
        safe_summary: "Synthetic dialogue fixture supports fiction boundary and reviewed memory-use preference.",
        quality_label_id: "psequality_synthetic_dialogue",
        supports_trait_paths: ["relationship.boundary_style", "memory.use_preference"],
        uncertainty_notes: ["Dialogue is fabricated fixture content."],
        review_gate_result_ids: ["psegate_redaction_passed", "psegate_anti_deception_passed"],
        raw_content_retained: false,
        review_required: true
      },
      {
        evidence_row_id: "psematrix_ev_description_memory",
        source_id: "psisrc_description_001",
        source_kind: "detailed_description",
        evidence_kind: "memory_policy_summary",
        safe_summary: "Synthetic description supports reviewed-summary-only memory use.",
        quality_label_id: "psequality_strong_description",
        supports_trait_paths: ["memory.use_preference"],
        uncertainty_notes: ["Memory policy is a preference hypothesis, not a runtime memory write."],
        review_gate_result_ids: ["psegate_consent_passed", "psegate_minimization_passed"],
        raw_content_retained: false,
        review_required: true
      }
    ],
    trait_hypotheses: [
      {
        trait_hypothesis_id: "psehyp_tone_001",
        trait_path: "style.tone",
        hypothesis_summary: "Favor calm, warm, concise tone.",
        supporting_evidence_row_ids: ["psematrix_ev_description_style"],
        conflicting_evidence_row_ids: [],
        confidence_band: "high",
        uncertainty_summary: "Synthetic source requires review before use.",
        review_gate_result_ids: ["psegate_consent_passed"],
        apply_status: "preview_only",
        mutation_allowed: false
      },
      {
        trait_hypothesis_id: "psehyp_pacing_001",
        trait_path: "style.pacing",
        hypothesis_summary: "Keep replies short by default and avoid crowding the user.",
        supporting_evidence_row_ids: ["psematrix_ev_description_style"],
        conflicting_evidence_row_ids: ["psematrix_ev_fuzzy_growth"],
        confidence_band: "medium",
        uncertainty_summary: "Fuzzy growth hint could conflict with concise pacing.",
        review_gate_result_ids: ["psegate_uncertainty_review"],
        apply_status: "preview_only",
        mutation_allowed: false
      },
      {
        trait_hypothesis_id: "psehyp_humor_001",
        trait_path: "style.humor",
        hypothesis_summary: "Allow dry humor only when tone remains low-pressure.",
        supporting_evidence_row_ids: ["psematrix_ev_fuzzy_growth"],
        conflicting_evidence_row_ids: [],
        confidence_band: "low",
        uncertainty_summary: "Humor evidence is fuzzy and needs review.",
        review_gate_result_ids: ["psegate_uncertainty_review"],
        apply_status: "preview_only",
        mutation_allowed: false
      },
      {
        trait_hypothesis_id: "psehyp_boundary_001",
        trait_path: "relationship.boundary_style",
        hypothesis_summary: "Keep AI identity and fictional boundaries explicit.",
        supporting_evidence_row_ids: ["psematrix_ev_description_style", "psematrix_ev_synthetic_dialogue_boundary"],
        conflicting_evidence_row_ids: [],
        confidence_band: "high",
        uncertainty_summary: "Boundary must remain explicit.",
        review_gate_result_ids: ["psegate_anti_deception_passed"],
        apply_status: "preview_only",
        mutation_allowed: false
      },
      {
        trait_hypothesis_id: "psehyp_memory_001",
        trait_path: "memory.use_preference",
        hypothesis_summary: "Use reviewed summaries only and avoid hidden raw logs.",
        supporting_evidence_row_ids: ["psematrix_ev_synthetic_dialogue_boundary"],
        conflicting_evidence_row_ids: [],
        confidence_band: "high",
        uncertainty_summary: "This is a policy hypothesis, not a memory write.",
        review_gate_result_ids: ["psegate_minimization_passed", "psegate_redaction_passed"],
        apply_status: "preview_only",
        mutation_allowed: false
      },
      {
        trait_hypothesis_id: "psehyp_growth_001",
        trait_path: "growth.short_term_hint",
        hypothesis_summary: "Consider a small evening-support growth hint only after more evidence.",
        supporting_evidence_row_ids: ["psematrix_ev_fuzzy_growth"],
        conflicting_evidence_row_ids: ["psematrix_ev_description_style"],
        confidence_band: "low",
        uncertainty_summary: "Growth hint is weak and should remain deferred.",
        review_gate_result_ids: ["psegate_uncertainty_review"],
        apply_status: "preview_only",
        mutation_allowed: false
      }
    ],
    quality_labels: [
      { quality_label_id: "psequality_strong_description", quality_code: "strong_synthetic_description", severity: "low", safe_summary: "Synthetic user-authored description is strong fixture evidence.", blocks_unreviewed_extraction: false },
      { quality_label_id: "psequality_fuzzy_seed", quality_code: "fuzzy_seed", severity: "medium", safe_summary: "Fuzzy seed supports only low-confidence hypotheses.", blocks_unreviewed_extraction: true },
      { quality_label_id: "psequality_synthetic_dialogue", quality_code: "synthetic_dialogue_fixture", severity: "low", safe_summary: "Synthetic dialogue fixture is safe only as labeled fiction.", blocks_unreviewed_extraction: false },
      { quality_label_id: "psequality_blocked_archive", quality_code: "blocked_archive_placeholder", severity: "high", safe_summary: "Archive placeholder is blocked until review gates pass.", blocks_unreviewed_extraction: true },
      { quality_label_id: "psequality_blocked_third_party", quality_code: "blocked_third_party_private_source", severity: "high", safe_summary: "Third-party private source is blocked without represented-person consent.", blocks_unreviewed_extraction: true }
    ],
    review_gate_results: [
      { review_gate_result_id: "psegate_consent_passed", gate_code: "consent", status: "passed", safe_summary: "Eligible synthetic sources have fixture consent.", blocks_extraction_when_failed: true },
      { review_gate_result_id: "psegate_minimization_passed", gate_code: "minimization", status: "passed", safe_summary: "Evidence rows use minimized summaries only.", blocks_extraction_when_failed: true },
      { review_gate_result_id: "psegate_redaction_passed", gate_code: "redaction", status: "passed", safe_summary: "No raw sensitive source content is retained.", blocks_extraction_when_failed: true },
      { review_gate_result_id: "psegate_uncertainty_review", gate_code: "uncertainty", status: "needs_review", safe_summary: "Fuzzy or weak evidence requires reviewer attention.", blocks_extraction_when_failed: true },
      { review_gate_result_id: "psegate_anti_deception_passed", gate_code: "anti_deception", status: "passed", safe_summary: "Evidence preserves AI identity disclosure.", blocks_extraction_when_failed: true }
    ],
    review_required: true,
    apply_policy: {
      mode: "preview_only",
      source_files_read: false,
      raw_content_retained: false,
      creates_embeddings: false,
      performs_extraction: false,
      writes_persona_card: false,
      writes_persona_version_store: false,
      writes_memory_store: false,
      writes_review_store: false,
      writes_runtime_store: false
    },
    non_execution_flags: {
      local_only: true,
      synthetic_fixture: true,
      uses_model_provider: false,
      reads_private_sources: false,
      retains_raw_source_content: false,
      creates_embeddings: false,
      performs_extraction: false,
      writes_persona_store: false,
      writes_persona_version_store: false,
      writes_memory_store: false,
      writes_review_store: false,
      writes_runtime_store: false,
      automatic_apply: false,
      sends_messages: false,
      uses_platform_adapter: false,
      uses_media_runtime: false
    }
  };

  fallbackState.source_evidence_persona_proposal = {
    schema_version: "m41.source_evidence_persona_proposal.v1",
    proposal_title: "Synthetic source evidence persona proposal",
    source_evidence_matrix_ref: {
      schema_version: "m40.persona_source_evidence_matrix.v1",
      matrix_title: "Synthetic persona source evidence matrix",
      source_surface: "persona_source_evidence_matrix"
    },
    proposal_candidates: [
      {
        proposal_id: "sepprop_tone_001",
        persona_field_path: "style.tone",
        proposed_value_summary: "Use a calm, warm, concise default tone.",
        rationale_summary: "The synthetic description strongly supports steady low-pressure tone.",
        source_trait_hypothesis_ids: ["psehyp_tone_001"],
        supporting_evidence_row_ids: ["psematrix_ev_description_style"],
        confidence_band: "high",
        risk_label_ids: ["seprisk_preview_only"],
        rollback_note_ids: ["seprollback_restore_prior_style"],
        review_gate_result_ids: ["sepgate_manual_review"],
        proposal_status: "preview_only",
        mutation_allowed: false,
        review_required: true
      },
      {
        proposal_id: "sepprop_pacing_001",
        persona_field_path: "style.pacing",
        proposed_value_summary: "Keep most replies short and leave space for the user.",
        rationale_summary: "The concise pacing hypothesis is useful but has a visible fuzzy-source conflict.",
        source_trait_hypothesis_ids: ["psehyp_pacing_001"],
        supporting_evidence_row_ids: ["psematrix_ev_description_style"],
        confidence_band: "medium",
        risk_label_ids: ["seprisk_preview_only", "seprisk_uncertainty"],
        rollback_note_ids: ["seprollback_restore_prior_style"],
        review_gate_result_ids: ["sepgate_manual_review", "sepgate_uncertainty"],
        proposal_status: "preview_only",
        mutation_allowed: false,
        review_required: true
      },
      {
        proposal_id: "sepprop_humor_001",
        persona_field_path: "style.humor",
        proposed_value_summary: "Allow dry humor only when the exchange remains low-pressure.",
        rationale_summary: "Humor comes from a fuzzy synthetic seed and should stay low confidence.",
        source_trait_hypothesis_ids: ["psehyp_humor_001"],
        supporting_evidence_row_ids: ["psematrix_ev_fuzzy_growth"],
        confidence_band: "low",
        risk_label_ids: ["seprisk_preview_only", "seprisk_uncertainty"],
        rollback_note_ids: ["seprollback_restore_prior_style"],
        review_gate_result_ids: ["sepgate_manual_review", "sepgate_uncertainty"],
        proposal_status: "preview_only",
        mutation_allowed: false,
        review_required: true
      },
      {
        proposal_id: "sepprop_boundary_001",
        persona_field_path: "relationship.boundary_style",
        proposed_value_summary: "Keep AI identity and fictional relationship boundaries explicit.",
        rationale_summary: "Description and synthetic dialogue both support a clear anti-deception boundary.",
        source_trait_hypothesis_ids: ["psehyp_boundary_001"],
        supporting_evidence_row_ids: ["psematrix_ev_description_style", "psematrix_ev_synthetic_dialogue_boundary"],
        confidence_band: "high",
        risk_label_ids: ["seprisk_preview_only", "seprisk_anti_deception"],
        rollback_note_ids: ["seprollback_restore_boundary"],
        review_gate_result_ids: ["sepgate_manual_review", "sepgate_anti_deception"],
        proposal_status: "preview_only",
        mutation_allowed: false,
        review_required: true
      },
      {
        proposal_id: "sepprop_memory_001",
        persona_field_path: "memory.use_preference",
        proposed_value_summary: "Use reviewed summaries only and avoid hidden source retention.",
        rationale_summary: "Synthetic matrix evidence supports memory use as a policy preference only.",
        source_trait_hypothesis_ids: ["psehyp_memory_001"],
        supporting_evidence_row_ids: ["psematrix_ev_synthetic_dialogue_boundary", "psematrix_ev_description_memory"],
        confidence_band: "high",
        risk_label_ids: ["seprisk_preview_only", "seprisk_no_memory_write"],
        rollback_note_ids: ["seprollback_restore_memory_policy"],
        review_gate_result_ids: ["sepgate_manual_review", "sepgate_minimization"],
        proposal_status: "preview_only",
        mutation_allowed: false,
        review_required: true
      },
      {
        proposal_id: "sepprop_growth_001",
        persona_field_path: "growth.short_term_hint",
        proposed_value_summary: "Keep a small evening-support growth hint as deferred review material.",
        rationale_summary: "The growth hint is weak synthetic evidence and should not become runtime state.",
        source_trait_hypothesis_ids: ["psehyp_growth_001"],
        supporting_evidence_row_ids: ["psematrix_ev_fuzzy_growth"],
        confidence_band: "low",
        risk_label_ids: ["seprisk_preview_only", "seprisk_uncertainty"],
        rollback_note_ids: ["seprollback_restore_growth"],
        review_gate_result_ids: ["sepgate_manual_review", "sepgate_uncertainty"],
        proposal_status: "preview_only",
        mutation_allowed: false,
        review_required: true
      }
    ],
    risk_labels: [
      { risk_label_id: "seprisk_preview_only", risk_code: "preview_only_proposal", severity: "low", safe_summary: "Proposal is inspectable but cannot change persona or runtime state.", blocks_auto_apply: true },
      { risk_label_id: "seprisk_uncertainty", risk_code: "weak_or_conflicting_evidence", severity: "medium", safe_summary: "Weak or conflicting synthetic evidence requires human review.", blocks_auto_apply: true },
      { risk_label_id: "seprisk_anti_deception", risk_code: "anti_deception_boundary", severity: "high", safe_summary: "Boundary changes must preserve clear AI identity and non-replacement.", blocks_auto_apply: true },
      { risk_label_id: "seprisk_no_memory_write", risk_code: "memory_write_not_authorized", severity: "high", safe_summary: "Memory preference proposals do not authorize any memory write.", blocks_auto_apply: true }
    ],
    rollback_notes: [
      { rollback_note_id: "seprollback_restore_prior_style", safe_summary: "Style proposals remain reversible review notes.", restore_summary: "Discard the style proposal and keep the prior reviewed style snapshot.", runtime_rollback_ready: false },
      { rollback_note_id: "seprollback_restore_boundary", safe_summary: "Boundary proposals must be removable before any future apply design.", restore_summary: "Restore the previous explicit AI boundary and relationship pacing note.", runtime_rollback_ready: false },
      { rollback_note_id: "seprollback_restore_memory_policy", safe_summary: "Memory preference proposals are not runtime memory operations.", restore_summary: "Keep existing reviewed-summary-only memory policy unchanged.", runtime_rollback_ready: false },
      { rollback_note_id: "seprollback_restore_growth", safe_summary: "Growth hints can be deferred without changing persona state.", restore_summary: "Remove the growth hint proposal and keep the current growth policy.", runtime_rollback_ready: false }
    ],
    review_gate_results: [
      { review_gate_result_id: "sepgate_manual_review", gate_code: "manual_review", status: "needs_review", safe_summary: "Every proposal requires manual review before any future apply design.", blocks_apply_when_failed: true },
      { review_gate_result_id: "sepgate_uncertainty", gate_code: "uncertainty", status: "needs_review", safe_summary: "Low or conflicting evidence remains gated for reviewer judgment.", blocks_apply_when_failed: true },
      { review_gate_result_id: "sepgate_anti_deception", gate_code: "anti_deception", status: "passed", safe_summary: "Proposal text preserves AI disclosure and avoids real-person replacement.", blocks_apply_when_failed: true },
      { review_gate_result_id: "sepgate_minimization", gate_code: "minimization", status: "passed", safe_summary: "Proposal uses minimized evidence refs and no source content.", blocks_apply_when_failed: true }
    ],
    proposal_outcome_labels: [
      { outcome_label_id: "sepoutcome_manual_review", outcome: "needs_manual_review", safe_summary: "Reviewer must inspect proposal candidates before future apply work." },
      { outcome_label_id: "sepoutcome_policy_block", outcome: "blocked_by_policy", safe_summary: "Current policy blocks mutation, automatic apply, and runtime writes." },
      { outcome_label_id: "sepoutcome_future_design", outcome: "ready_for_future_apply_design", safe_summary: "The preview shape can inform a later reviewed apply design." }
    ],
    review_required: true,
    apply_policy: {
      mode: "preview_only",
      writes_persona_card: false,
      writes_persona_version_store: false,
      writes_memory_store: false,
      writes_review_store: false,
      writes_runtime_store: false,
      automatic_apply: false
    },
    non_execution_flags: {
      local_only: true,
      synthetic_fixture: true,
      uses_model_provider: false,
      reads_private_sources: false,
      retains_raw_source_content: false,
      creates_embeddings: false,
      performs_extraction: false,
      writes_persona_store: false,
      writes_persona_version_store: false,
      writes_memory_store: false,
      writes_review_store: false,
      writes_runtime_store: false,
      automatic_apply: false,
      sends_messages: false,
      uses_platform_adapter: false,
      uses_media_runtime: false
    }
  };

  fallbackState.source_proposal_persona_draft = {
    schema_version: "m42.source_proposal_persona_draft.v1",
    draft_title: "Synthetic proposal-linked persona draft",
    source_proposal_ref: {
      schema_version: "m41.source_evidence_persona_proposal.v1",
      proposal_title: "Synthetic source evidence persona proposal",
      source_surface: "source_evidence_persona_proposal"
    },
    base_persona_snapshot: {
      persona_id: "persona_synthetic",
      display_name: "Lin Qi",
      snapshot_summary: "Fictional AI companion with calm style and explicit boundaries.",
      ai_identity_disclosure: "AI-generated synthetic companion.",
      runtime_snapshot_written: false
    },
    selected_proposal_ids: [
      "sepprop_tone_001",
      "sepprop_pacing_001",
      "sepprop_humor_001",
      "sepprop_boundary_001",
      "sepprop_memory_001",
      "sepprop_growth_001"
    ],
    draft_field_changes: [
      {
        draft_change_id: "spdraft_change_style_tone",
        persona_field_path: "style.tone",
        before_summary: "Existing draft tone is calm but not yet source-proposal-linked.",
        after_summary: "Use a calm, warm, concise default tone.",
        source_proposal_ids: ["sepprop_tone_001"],
        source_trait_hypothesis_ids: ["psehyp_tone_001"],
        supporting_evidence_row_ids: ["psematrix_ev_description_style"],
        confidence_band: "high",
        risk_label_ids: ["seprisk_preview_only"],
        conflict_note_ids: ["spdraft_conflict_style_review"],
        rollback_ref_ids: ["spdraft_rollback_tone"],
        review_gate_result_ids: ["spdraft_gate_manual_review"],
        draft_status: "preview_only",
        mutation_allowed: false,
        review_required: true
      },
      {
        draft_change_id: "spdraft_change_style_pacing",
        persona_field_path: "style.pacing",
        before_summary: "Existing draft pacing is concise by convention only.",
        after_summary: "Keep most replies short and leave space for the user.",
        source_proposal_ids: ["sepprop_pacing_001"],
        source_trait_hypothesis_ids: ["psehyp_pacing_001"],
        supporting_evidence_row_ids: ["psematrix_ev_description_style"],
        confidence_band: "medium",
        risk_label_ids: ["seprisk_preview_only", "seprisk_uncertainty"],
        conflict_note_ids: ["spdraft_conflict_pacing_growth"],
        rollback_ref_ids: ["spdraft_rollback_pacing"],
        review_gate_result_ids: ["spdraft_gate_manual_review", "spdraft_gate_uncertainty"],
        draft_status: "preview_only",
        mutation_allowed: false,
        review_required: true
      },
      {
        draft_change_id: "spdraft_change_style_humor",
        persona_field_path: "style.humor",
        before_summary: "Existing draft humor is unspecified.",
        after_summary: "Allow dry humor only when the exchange remains low-pressure.",
        source_proposal_ids: ["sepprop_humor_001"],
        source_trait_hypothesis_ids: ["psehyp_humor_001"],
        supporting_evidence_row_ids: ["psematrix_ev_fuzzy_growth"],
        confidence_band: "low",
        risk_label_ids: ["seprisk_preview_only", "seprisk_uncertainty"],
        conflict_note_ids: ["spdraft_conflict_humor_uncertainty"],
        rollback_ref_ids: ["spdraft_rollback_humor"],
        review_gate_result_ids: ["spdraft_gate_manual_review", "spdraft_gate_uncertainty"],
        draft_status: "preview_only",
        mutation_allowed: false,
        review_required: true
      },
      {
        draft_change_id: "spdraft_change_relationship_boundary_style",
        persona_field_path: "relationship.boundary_style",
        before_summary: "Existing draft boundary states AI identity at a high level.",
        after_summary: "Keep AI identity and fictional relationship boundaries explicit.",
        source_proposal_ids: ["sepprop_boundary_001"],
        source_trait_hypothesis_ids: ["psehyp_boundary_001"],
        supporting_evidence_row_ids: ["psematrix_ev_description_style", "psematrix_ev_synthetic_dialogue_boundary"],
        confidence_band: "high",
        risk_label_ids: ["seprisk_preview_only", "seprisk_anti_deception"],
        conflict_note_ids: ["spdraft_conflict_boundary_required"],
        rollback_ref_ids: ["spdraft_rollback_boundary"],
        review_gate_result_ids: ["spdraft_gate_manual_review", "spdraft_gate_anti_deception"],
        draft_status: "preview_only",
        mutation_allowed: false,
        review_required: true
      },
      {
        draft_change_id: "spdraft_change_memory_use_preference",
        persona_field_path: "memory.use_preference",
        before_summary: "Existing draft memory preference is reviewed-summary-only.",
        after_summary: "Use reviewed summaries only and avoid hidden source retention.",
        source_proposal_ids: ["sepprop_memory_001"],
        source_trait_hypothesis_ids: ["psehyp_memory_001"],
        supporting_evidence_row_ids: ["psematrix_ev_synthetic_dialogue_boundary", "psematrix_ev_description_memory"],
        confidence_band: "high",
        risk_label_ids: ["seprisk_preview_only", "seprisk_no_memory_write"],
        conflict_note_ids: ["spdraft_conflict_memory_no_write"],
        rollback_ref_ids: ["spdraft_rollback_memory"],
        review_gate_result_ids: ["spdraft_gate_manual_review", "spdraft_gate_no_memory_write"],
        draft_status: "preview_only",
        mutation_allowed: false,
        review_required: true
      },
      {
        draft_change_id: "spdraft_change_growth_short_term_hint",
        persona_field_path: "growth.short_term_hint",
        before_summary: "Existing draft growth hint is deferred.",
        after_summary: "Keep a small evening-support growth hint as deferred review material.",
        source_proposal_ids: ["sepprop_growth_001"],
        source_trait_hypothesis_ids: ["psehyp_growth_001"],
        supporting_evidence_row_ids: ["psematrix_ev_fuzzy_growth"],
        confidence_band: "low",
        risk_label_ids: ["seprisk_preview_only", "seprisk_uncertainty"],
        conflict_note_ids: ["spdraft_conflict_growth_deferred"],
        rollback_ref_ids: ["spdraft_rollback_growth"],
        review_gate_result_ids: ["spdraft_gate_manual_review", "spdraft_gate_uncertainty"],
        draft_status: "preview_only",
        mutation_allowed: false,
        review_required: true
      }
    ],
    unchanged_field_summaries: [
      { field_path: "identity.ai_disclosure", safe_summary: "AI identity disclosure remains visible and unchanged.", reason: "Anti-deception boundary is retained." },
      { field_path: "safety.crisis_policy", safe_summary: "Crisis support boundaries remain unchanged.", reason: "Draft preview is not clinical support." },
      { field_path: "proactive.review_policy", safe_summary: "Proactive ideas remain review-only.", reason: "Draft preview does not authorize outreach." }
    ],
    conflict_notes: [
      { conflict_note_id: "spdraft_conflict_style_review", conflict_code: "style_requires_review", severity: "low", safe_summary: "Style fields require manual review before any future draft use.", blocks_auto_apply: true },
      { conflict_note_id: "spdraft_conflict_pacing_growth", conflict_code: "pacing_growth_tension", severity: "medium", safe_summary: "Concise pacing and growth hints need reviewer balancing.", blocks_auto_apply: true },
      { conflict_note_id: "spdraft_conflict_humor_uncertainty", conflict_code: "humor_low_confidence", severity: "medium", safe_summary: "Humor evidence is low confidence and must remain bounded.", blocks_auto_apply: true },
      { conflict_note_id: "spdraft_conflict_boundary_required", conflict_code: "anti_deception_boundary_required", severity: "high", safe_summary: "Boundary fields must preserve explicit AI identity.", blocks_auto_apply: true },
      { conflict_note_id: "spdraft_conflict_memory_no_write", conflict_code: "memory_write_not_authorized", severity: "high", safe_summary: "Memory preference draft does not authorize memory writes.", blocks_auto_apply: true },
      { conflict_note_id: "spdraft_conflict_growth_deferred", conflict_code: "growth_hint_deferred", severity: "medium", safe_summary: "Growth hint remains deferred until stronger evidence exists.", blocks_auto_apply: true }
    ],
    rollback_refs: [
      { rollback_ref_id: "spdraft_rollback_tone", safe_summary: "Tone draft can be discarded before any future apply design.", restore_summary: "Keep prior calm style snapshot.", runtime_rollback_ready: false },
      { rollback_ref_id: "spdraft_rollback_pacing", safe_summary: "Pacing draft can be discarded before any future apply design.", restore_summary: "Keep prior concise pacing convention.", runtime_rollback_ready: false },
      { rollback_ref_id: "spdraft_rollback_humor", safe_summary: "Humor draft can be discarded before any future apply design.", restore_summary: "Keep humor unspecified.", runtime_rollback_ready: false },
      { rollback_ref_id: "spdraft_rollback_boundary", safe_summary: "Boundary draft can be discarded before any future apply design.", restore_summary: "Keep previous AI identity disclosure boundary.", runtime_rollback_ready: false },
      { rollback_ref_id: "spdraft_rollback_memory", safe_summary: "Memory preference draft can be discarded without memory writes.", restore_summary: "Keep existing reviewed-summary-only memory policy.", runtime_rollback_ready: false },
      { rollback_ref_id: "spdraft_rollback_growth", safe_summary: "Growth draft can remain deferred.", restore_summary: "Keep growth hint unchanged.", runtime_rollback_ready: false }
    ],
    review_gate_results: [
      { review_gate_result_id: "spdraft_gate_manual_review", gate_code: "manual_review", status: "needs_review", safe_summary: "Every draft field requires manual review.", blocks_apply_when_failed: true },
      { review_gate_result_id: "spdraft_gate_uncertainty", gate_code: "uncertainty", status: "needs_review", safe_summary: "Low-confidence proposal fields require reviewer judgment.", blocks_apply_when_failed: true },
      { review_gate_result_id: "spdraft_gate_anti_deception", gate_code: "anti_deception", status: "passed", safe_summary: "Draft keeps AI identity disclosure explicit.", blocks_apply_when_failed: true },
      { review_gate_result_id: "spdraft_gate_no_memory_write", gate_code: "no_memory_write", status: "passed", safe_summary: "Draft does not write or alter memory state.", blocks_apply_when_failed: true }
    ],
    draft_outcome_labels: [
      { outcome_label_id: "spdraft_outcome_manual_review", outcome: "needs_manual_review", safe_summary: "Reviewer must inspect draft fields before future apply work." },
      { outcome_label_id: "spdraft_outcome_policy_block", outcome: "blocked_by_policy", safe_summary: "Current policy blocks draft mutation and runtime writes." },
      { outcome_label_id: "spdraft_outcome_future_design", outcome: "ready_for_future_apply_design", safe_summary: "The draft shape can inform a later reviewed apply design." }
    ],
    review_required: true,
    apply_policy: {
      mode: "preview_only",
      writes_persona_card: false,
      writes_persona_version_store: false,
      writes_memory_store: false,
      writes_review_store: false,
      writes_runtime_store: false,
      automatic_apply: false
    },
    non_execution_flags: {
      local_only: true,
      synthetic_fixture: true,
      uses_model_provider: false,
      reads_private_sources: false,
      retains_raw_source_content: false,
      creates_embeddings: false,
      performs_extraction: false,
      writes_persona_store: false,
      writes_persona_version_store: false,
      writes_memory_store: false,
      writes_review_store: false,
      writes_runtime_store: false,
      automatic_apply: false,
      sends_messages: false,
      uses_platform_adapter: false,
      uses_media_runtime: false
    }
  };

  fallbackState.source_draft_apply_readiness = {
    schema_version: "m43.source_draft_apply_readiness.v1",
    readiness_title: "Synthetic source draft apply-readiness preview",
    source_draft_ref: {
      schema_version: "m42.source_proposal_persona_draft.v1",
      draft_title: "Synthetic proposal-linked persona draft",
      source_surface: "source_proposal_persona_draft"
    },
    evaluated_draft_change_ids: [
      "spdraft_change_style_tone",
      "spdraft_change_style_pacing",
      "spdraft_change_style_humor",
      "spdraft_change_relationship_boundary_style",
      "spdraft_change_memory_use_preference",
      "spdraft_change_growth_short_term_hint"
    ],
    field_readiness_records: [
      {
        readiness_record_id: "sdar_record_style_tone",
        draft_change_id: "spdraft_change_style_tone",
        persona_field_path: "style.tone",
        readiness_outcome: "ready_for_future_apply_design",
        safe_summary: "Apply-readiness preview for style.tone: ready for future apply design.",
        blocking_condition_ids: [],
        required_review_gate_result_ids: ["spdraft_gate_manual_review"],
        rollback_ref_ids: ["spdraft_rollback_tone"],
        future_apply_design_notes: "Shape is clear enough to inform a later separately scoped apply executor design, but it is not applied.",
        preview_only: true,
        mutation_allowed: false,
        review_required: true
      },
      {
        readiness_record_id: "sdar_record_style_pacing",
        draft_change_id: "spdraft_change_style_pacing",
        persona_field_path: "style.pacing",
        readiness_outcome: "needs_manual_review",
        safe_summary: "Apply-readiness preview for style.pacing: needs manual review.",
        blocking_condition_ids: ["sdar_condition_uncertainty_review"],
        required_review_gate_result_ids: ["spdraft_gate_manual_review", "spdraft_gate_uncertainty"],
        rollback_ref_ids: ["spdraft_rollback_pacing"],
        future_apply_design_notes: "Reviewer judgment is required before this draft field could inform future apply design.",
        preview_only: true,
        mutation_allowed: false,
        review_required: true
      },
      {
        readiness_record_id: "sdar_record_style_humor",
        draft_change_id: "spdraft_change_style_humor",
        persona_field_path: "style.humor",
        readiness_outcome: "needs_manual_review",
        safe_summary: "Apply-readiness preview for style.humor: needs manual review.",
        blocking_condition_ids: ["sdar_condition_uncertainty_review"],
        required_review_gate_result_ids: ["spdraft_gate_manual_review", "spdraft_gate_uncertainty"],
        rollback_ref_ids: ["spdraft_rollback_humor"],
        future_apply_design_notes: "Reviewer judgment is required before this draft field could inform future apply design.",
        preview_only: true,
        mutation_allowed: false,
        review_required: true
      },
      {
        readiness_record_id: "sdar_record_relationship_boundary_style",
        draft_change_id: "spdraft_change_relationship_boundary_style",
        persona_field_path: "relationship.boundary_style",
        readiness_outcome: "blocked",
        safe_summary: "Apply-readiness preview for relationship.boundary_style: blocked.",
        blocking_condition_ids: ["sdar_condition_anti_deception_final_review"],
        required_review_gate_result_ids: ["spdraft_gate_manual_review", "spdraft_gate_anti_deception"],
        rollback_ref_ids: ["spdraft_rollback_boundary"],
        future_apply_design_notes: "Current policy blocks this draft field from apply design until the blocking condition is resolved.",
        preview_only: true,
        mutation_allowed: false,
        review_required: true
      },
      {
        readiness_record_id: "sdar_record_memory_use_preference",
        draft_change_id: "spdraft_change_memory_use_preference",
        persona_field_path: "memory.use_preference",
        readiness_outcome: "blocked",
        safe_summary: "Apply-readiness preview for memory.use_preference: blocked.",
        blocking_condition_ids: ["sdar_condition_memory_write_not_authorized"],
        required_review_gate_result_ids: ["spdraft_gate_manual_review", "spdraft_gate_no_memory_write"],
        rollback_ref_ids: ["spdraft_rollback_memory"],
        future_apply_design_notes: "Current policy blocks this draft field from apply design until the blocking condition is resolved.",
        preview_only: true,
        mutation_allowed: false,
        review_required: true
      },
      {
        readiness_record_id: "sdar_record_growth_short_term_hint",
        draft_change_id: "spdraft_change_growth_short_term_hint",
        persona_field_path: "growth.short_term_hint",
        readiness_outcome: "needs_manual_review",
        safe_summary: "Apply-readiness preview for growth.short_term_hint: needs manual review.",
        blocking_condition_ids: ["sdar_condition_uncertainty_review"],
        required_review_gate_result_ids: ["spdraft_gate_manual_review", "spdraft_gate_uncertainty"],
        rollback_ref_ids: ["spdraft_rollback_growth"],
        future_apply_design_notes: "Reviewer judgment is required before this draft field could inform future apply design.",
        preview_only: true,
        mutation_allowed: false,
        review_required: true
      }
    ],
    blocked_condition_records: [
      { blocked_condition_id: "sdar_condition_uncertainty_review", condition_code: "uncertainty_requires_manual_review", severity: "medium", safe_summary: "Low-confidence or conflicting draft evidence requires reviewer judgment.", affected_draft_change_ids: ["spdraft_change_style_pacing", "spdraft_change_style_humor", "spdraft_change_growth_short_term_hint"], blocks_apply: true },
      { blocked_condition_id: "sdar_condition_anti_deception_final_review", condition_code: "anti_deception_final_review_required", severity: "high", safe_summary: "Boundary fields need explicit anti-deception review before any apply design.", affected_draft_change_ids: ["spdraft_change_relationship_boundary_style"], blocks_apply: true },
      { blocked_condition_id: "sdar_condition_memory_write_not_authorized", condition_code: "memory_write_not_authorized", severity: "high", safe_summary: "Memory preference drafts do not authorize memory writes or runtime mutation.", affected_draft_change_ids: ["spdraft_change_memory_use_preference"], blocks_apply: true }
    ],
    required_review_gate_refs: [
      { review_gate_result_id: "spdraft_gate_manual_review", gate_code: "manual_review", status: "needs_review", safe_summary: "Every draft field requires manual review.", required_before_apply: true },
      { review_gate_result_id: "spdraft_gate_uncertainty", gate_code: "uncertainty", status: "needs_review", safe_summary: "Low-confidence proposal fields require reviewer judgment.", required_before_apply: true },
      { review_gate_result_id: "spdraft_gate_anti_deception", gate_code: "anti_deception", status: "passed", safe_summary: "Draft keeps AI identity disclosure explicit.", required_before_apply: true },
      { review_gate_result_id: "spdraft_gate_no_memory_write", gate_code: "no_memory_write", status: "passed", safe_summary: "Draft does not write or alter memory state.", required_before_apply: true }
    ],
    rollback_dependency_refs: [
      { rollback_ref_id: "spdraft_rollback_tone", dependent_draft_change_ids: ["spdraft_change_style_tone"], restore_summary: "Keep prior calm style snapshot.", runtime_rollback_ready: false },
      { rollback_ref_id: "spdraft_rollback_pacing", dependent_draft_change_ids: ["spdraft_change_style_pacing"], restore_summary: "Keep prior concise pacing convention.", runtime_rollback_ready: false },
      { rollback_ref_id: "spdraft_rollback_humor", dependent_draft_change_ids: ["spdraft_change_style_humor"], restore_summary: "Keep humor unspecified.", runtime_rollback_ready: false },
      { rollback_ref_id: "spdraft_rollback_boundary", dependent_draft_change_ids: ["spdraft_change_relationship_boundary_style"], restore_summary: "Keep previous AI identity disclosure boundary.", runtime_rollback_ready: false },
      { rollback_ref_id: "spdraft_rollback_memory", dependent_draft_change_ids: ["spdraft_change_memory_use_preference"], restore_summary: "Keep existing reviewed-summary-only memory policy.", runtime_rollback_ready: false },
      { rollback_ref_id: "spdraft_rollback_growth", dependent_draft_change_ids: ["spdraft_change_growth_short_term_hint"], restore_summary: "Keep growth hint unchanged.", runtime_rollback_ready: false }
    ],
    readiness_outcome_labels: [
      { outcome_label_id: "sdar_outcome_blocked", outcome: "blocked", safe_summary: "Current preview policy blocks apply for selected draft fields." },
      { outcome_label_id: "sdar_outcome_manual_review", outcome: "needs_manual_review", safe_summary: "Reviewer judgment is required before any future apply design." },
      { outcome_label_id: "sdar_outcome_future_design", outcome: "ready_for_future_apply_design", safe_summary: "Some draft fields can inform later apply design without authorizing mutation now." }
    ],
    review_required: true,
    apply_policy: {
      mode: "preview_only",
      apply_executor_enabled: false,
      writes_persona_card: false,
      writes_persona_version_store: false,
      writes_memory_store: false,
      writes_review_store: false,
      writes_runtime_store: false,
      automatic_apply: false
    },
    non_execution_flags: {
      local_only: true,
      synthetic_fixture: true,
      uses_model_provider: false,
      reads_private_sources: false,
      retains_raw_source_content: false,
      creates_embeddings: false,
      performs_extraction: false,
      writes_persona_store: false,
      writes_persona_version_store: false,
      writes_memory_store: false,
      writes_review_store: false,
      writes_runtime_store: false,
      automatic_apply: false,
      sends_messages: false,
      uses_platform_adapter: false,
      uses_media_runtime: false
    }
  };

  attachPersonaWorkbenchReviewCards(fallbackState);
  attachPersonaEvolutionReviewCards(fallbackState);
  attachPersonaVersionDraftReviewCards(fallbackState);
  attachPersonaSourceIntakeReviewCards(fallbackState);
  attachPersonaSourceEvidenceReviewCards(fallbackState);
  attachSourceEvidencePersonaProposalReviewCards(fallbackState);
  attachSourceProposalPersonaDraftReviewCards(fallbackState);
  attachSourceDraftApplyReadinessReviewCards(fallbackState);

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

  function items(containerSelector, values, mapper, extraClass) {
    const node = one(containerSelector);
    if (!node) {
      return;
    }
    node.innerHTML = "";
    (values || []).forEach(function (value) {
      const div = document.createElement("div");
      div.className = "item" + (extraClass ? " " + extraClass : "");
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
    const personaWorkbench = data.persona_distillation_workbench || fallbackState.persona_distillation_workbench || {};
    const personaEvolution = data.persona_evolution_preview || fallbackState.persona_evolution_preview || {};
    const versionLedger = data.persona_version_draft_ledger || fallbackState.persona_version_draft_ledger || {};
    const sourceIntakeManifest = data.persona_source_intake_manifest || fallbackState.persona_source_intake_manifest || {};
    const sourceEvidenceMatrix = data.persona_source_evidence_matrix || fallbackState.persona_source_evidence_matrix || {};
    const sourcePersonaProposal = data.source_evidence_persona_proposal || fallbackState.source_evidence_persona_proposal || {};
    const sourcePersonaDraft = data.source_proposal_persona_draft || fallbackState.source_proposal_persona_draft || {};
    const sourceDraftReadiness = data.source_draft_apply_readiness || fallbackState.source_draft_apply_readiness || {};

    text("#identity-strip", data.onboarding.ai_identity_disclosure_text);
    drawIntegratedScenario(integratedScenario);
    drawTrustCommercial(trustCommercial);
    drawCompanionSession(companionSession);
    drawPersonaWorkbench(personaWorkbench);
    drawPersonaEvolutionPreview(personaEvolution);
    drawPersonaVersionDraftLedger(versionLedger);
    drawPersonaSourceIntakeManifest(sourceIntakeManifest);
    drawPersonaSourceEvidenceMatrix(sourceEvidenceMatrix);
    drawSourceEvidencePersonaProposal(sourcePersonaProposal);
    drawSourceProposalPersonaDraft(sourcePersonaDraft);
    drawSourceDraftApplyReadiness(sourceDraftReadiness);
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

  function drawPersonaWorkbench(workbench) {
    const evidenceById = sessionRecordsById(workbench.evidence_refs || [], "evidence_id");
    const flags = workbench.non_execution_flags || {};

    text("#workbench-title", workbench.workbench_title || "Synthetic persona distillation workbench");
    text("#workbench-schema", friendlyLabel(workbench.schema_version || "m36 workbench"));
    labels("#workbench-non-execution-list", workbenchNonExecutionLabels(flags));

    items("#workbench-mode-list", workbench.input_modes || [], function (mode) {
      return "<div class='item-title'>" + (mode.label || friendlyLabel(mode.mode_id)) + "</div>"
        + "<div>" + (mode.description || "") + "</div>"
        + "<div class='item-meta'>"
        + friendlyLabel(mode.mode_id)
        + " / Review required: " + String(mode.requires_review === true)
        + " / Private source: " + String(mode.private_source_allowed === true)
        + "</div>";
    });
    items("#workbench-input-list", workbench.synthetic_inputs || [], function (input) {
      return "<div class='item-title'>" + (input.fixture_label || input.input_id) + "</div>"
        + "<div>" + (input.safe_summary || "") + "</div>"
        + "<div class='item-meta'>"
        + friendlyLabel(input.mode_id)
        + " / Detail: " + friendlyLabel(input.detail_level)
        + " / Raw retained: " + String(input.raw_content_retained === true)
        + "</div>";
    });
    items("#workbench-evidence-list", workbench.evidence_refs || [], function (evidence) {
      return "<div class='item-title'>" + evidence.evidence_id + "</div>"
        + "<div>" + (evidence.safe_summary || "") + "</div>"
        + "<div class='item-meta'>"
        + friendlyLabel(evidence.source_mode_id)
        + " / " + friendlyLabel(evidence.source_kind)
        + "</div>";
    });
    items("#workbench-gate-list", workbench.safety_gates || [], function (gate) {
      return "<div class='item-title'>" + (gate.label || friendlyLabel(gate.gate_id)) + "</div>"
        + "<div>" + (gate.safe_summary || "") + "</div>"
        + "<div class='item-meta'>Enabled: " + String(gate.enabled === true) + "</div>";
    });
    items("#workbench-trait-list", workbench.extracted_trait_candidates || [], function (candidate) {
      return appendWorkbenchTraitCard(candidate, evidenceById);
    }, "workbench-trait-card");
    items("#workbench-blocked-list", workbench.blocked_requests || [], function (request) {
      return appendWorkbenchBlockedCard(request);
    }, "workbench-blocked-card");
  }

  function appendWorkbenchTraitCard(candidate, evidenceById) {
    const evidence = (candidate.evidence_ref_ids || []).map(function (id) {
      const record = evidenceById[id] || {};
      return id + ": " + (record.safe_summary || "safe evidence ref");
    });
    return "<div class='item-title'>" + friendlyLabel(candidate.category) + "</div>"
      + "<div>" + (candidate.candidate_value || "") + "</div>"
      + "<div class='item-meta'>" + (candidate.safe_summary || "") + "</div>"
      + "<div class='item-meta'>Confidence: " + friendlyLabel(candidate.confidence_band)
      + " / Review: " + friendlyLabel(candidate.review_status)
      + " / Status: " + friendlyLabel(candidate.apply_status)
      + "</div>"
      + "<div class='item-meta'>Evidence: " + evidence.join(" / ") + "</div>";
  }

  function appendWorkbenchBlockedCard(request) {
    return "<div class='item-title'>" + friendlyLabel(request.request_type) + "</div>"
      + "<div>" + (request.user_facing_explanation || request.safe_summary || "") + "</div>"
      + "<div class='item-meta'>Reason: " + (request.risk_reason || "") + "</div>"
      + "<div class='item-meta'>Status: " + friendlyLabel(request.status)
      + " / Mutation: " + String(request.mutation_allowed === true)
      + "</div>";
  }

  function workbenchNonExecutionLabels(flags) {
    return [
      flags.local_only === true ? "local only" : "",
      flags.synthetic_fixture === true ? "synthetic fixture" : "",
      flags.uses_model_provider === false ? "no provider" : "",
      flags.reads_private_sources === false ? "no private sources" : "",
      flags.writes_runtime_store === false ? "no runtime writes" : "",
      flags.automatic_apply === false ? "preview only" : "",
      flags.sends_messages === false ? "no outbound" : "",
      flags.uses_platform_adapter === false ? "no adapter" : "",
      flags.uses_media_runtime === false ? "no media runtime" : ""
    ].filter(Boolean);
  }

  function drawPersonaEvolutionPreview(preview) {
    const riskById = sessionRecordsById(preview.risk_labels || [], "risk_label_id");
    const rollbackById = sessionRecordsById(preview.rollback_notes || [], "rollback_note_id");
    const flags = preview.non_execution_flags || {};
    const source = preview.source_workbench_ref || {};
    const snapshot = preview.persona_snapshot_before || {};

    text("#evolution-title", preview.preview_title || "Synthetic persona evolution preview");
    text("#evolution-schema", friendlyLabel(preview.schema_version || "m37 preview"));
    labels("#evolution-non-execution-list", evolutionNonExecutionLabels(flags));
    text(
      "#evolution-source-summary",
      "Source: " + (source.workbench_title || friendlyLabel(source.source_surface))
        + " / Schema: " + (source.schema_version || "")
        + " / Traits: " + friendlyList(preview.source_trait_candidate_ids || [])
    );

    const snapshotNode = one("#evolution-snapshot");
    if (snapshotNode) {
      snapshotNode.innerHTML = "<div class='item-title'>" + (snapshot.display_name || "Synthetic persona") + "</div>"
        + "<div>" + (snapshot.ai_identity_disclosure || "") + "</div>"
        + "<div class='item-meta'>Traits: " + friendlyList(snapshot.current_trait_summaries || []) + "</div>"
        + "<div class='item-meta'>Boundary: " + (snapshot.current_boundary_summary || "") + "</div>"
        + "<div class='item-meta'>Memory: " + (snapshot.current_memory_use_summary || "") + "</div>"
        + "<div class='item-meta'>Source: " + friendlyLabel(snapshot.source_label)
        + " / Real-person claim: " + String(snapshot.real_person_claim === true)
        + " / Runtime ref: " + (snapshot.runtime_state_ref || "none")
        + "</div>";
    }

    items("#evolution-patch-list", preview.proposed_patch_candidates || [], function (patch) {
      return appendEvolutionPatchCard(patch, riskById, rollbackById);
    }, "evolution-patch-card");
    items("#evolution-risk-list", preview.risk_labels || [], function (risk) {
      return appendEvolutionRiskCard(risk);
    }, "evolution-risk-card");
    items("#evolution-rollback-list", preview.rollback_notes || [], function (note) {
      return appendEvolutionRollbackCard(note);
    }, "evolution-rollback-card");
    items("#evolution-exclusion-list", preview.blocked_source_exclusions || [], function (exclusion) {
      return appendEvolutionExclusionCard(exclusion);
    }, "evolution-exclusion-card");
  }

  function appendEvolutionPatchCard(patch, riskById, rollbackById) {
    const risks = (patch.risk_label_ids || []).map(function (id) {
      const risk = riskById[id] || {};
      return (risk.risk_code || friendlyLabel(id)) + ": " + (risk.safe_summary || "review required");
    });
    const rollbacks = (patch.rollback_note_ids || []).map(function (id) {
      const note = rollbackById[id] || {};
      return (note.rollback_summary || friendlyLabel(id));
    });
    return "<div class='item-title'>" + (patch.changed_field_path || friendlyLabel(patch.patch_kind)) + "</div>"
      + "<div class='item-meta'>Before: " + (patch.before_summary || "") + "</div>"
      + "<div class='item-meta'>After: " + (patch.after_summary || "") + "</div>"
      + "<div>" + (patch.rationale_summary || "") + "</div>"
      + "<div class='item-meta'>Traits: " + friendlyList(patch.source_trait_candidate_ids || [])
      + " / Evidence: " + friendlyList(patch.evidence_ref_ids || [])
      + "</div>"
      + "<div class='item-meta'>Confidence: " + friendlyLabel(patch.confidence_band)
      + " / Review: " + friendlyLabel(patch.review_status)
      + " / Status: " + friendlyLabel(patch.apply_status)
      + " / Mutation: " + String(patch.mutation_allowed === true)
      + "</div>"
      + "<div class='item-meta'>Risks: " + (risks.join(" / ") || "none") + "</div>"
      + "<div class='item-meta'>Rollback: " + (rollbacks.join(" / ") || "none") + "</div>";
  }

  function appendEvolutionRiskCard(risk) {
    return "<div class='item-title'>" + friendlyLabel(risk.risk_code) + "</div>"
      + "<div>" + (risk.safe_summary || "") + "</div>"
      + "<div class='item-meta'>Severity: " + friendlyLabel(risk.severity)
      + " / Blocks auto apply: " + String(risk.blocks_auto_apply === true)
      + "</div>"
      + "<div class='item-meta'>Mitigation: " + (risk.mitigation_summary || "") + "</div>";
  }

  function appendEvolutionRollbackCard(note) {
    return "<div class='item-title'>" + friendlyLabel(note.rollback_note_id) + "</div>"
      + "<div class='item-meta'>Targets: " + friendlyList(note.target_patch_ids || []) + "</div>"
      + "<div>Prior: " + (note.prior_summary || "") + "</div>"
      + "<div>Rollback: " + (note.rollback_summary || "") + "</div>"
      + "<div class='item-meta'>Reviewer: " + (note.required_reviewer_action || "")
      + " / Runtime ready: " + String(note.runtime_rollback_ready === true)
      + "</div>";
  }

  function appendEvolutionExclusionCard(exclusion) {
    return "<div class='item-title'>" + friendlyLabel(exclusion.request_type) + "</div>"
      + "<div>" + (exclusion.safe_summary || "") + "</div>"
      + "<div class='item-meta'>Reason: " + (exclusion.exclusion_reason || "") + "</div>"
      + "<div class='item-meta'>Excluded: " + String(exclusion.excluded_from_patch_generation === true)
      + " / Mutation: " + String(exclusion.mutation_allowed === true)
      + "</div>";
  }

  function evolutionNonExecutionLabels(flags) {
    return [
      flags.local_only === true ? "local only" : "",
      flags.synthetic_fixture === true ? "synthetic fixture" : "",
      flags.uses_model_provider === false ? "no provider" : "",
      flags.reads_private_sources === false ? "no private sources" : "",
      flags.writes_persona_store === false ? "no persona store" : "",
      flags.writes_memory_store === false ? "no memory store" : "",
      flags.writes_review_store === false ? "no review store" : "",
      flags.writes_runtime_store === false ? "no runtime writes" : "",
      flags.automatic_apply === false ? "preview only" : "",
      flags.sends_messages === false ? "no outbound" : "",
      flags.uses_platform_adapter === false ? "no adapter" : "",
      flags.uses_media_runtime === false ? "no media runtime" : ""
    ].filter(Boolean);
  }

  function drawPersonaVersionDraftLedger(ledger) {
    const conflictById = sessionRecordsById(ledger.conflict_notes || [], "conflict_note_id");
    const rollbackById = sessionRecordsById(ledger.rollback_ref_index || [], "rollback_ref_id");
    const flags = ledger.non_execution_flags || {};
    const source = ledger.source_evolution_preview_ref || {};
    const snapshot = ledger.base_persona_snapshot_ref || {};

    text("#version-ledger-title", ledger.ledger_title || "Synthetic persona version draft ledger");
    text("#version-ledger-schema", friendlyLabel(ledger.schema_version || "m38 ledger"));
    labels("#version-ledger-non-execution-list", versionLedgerNonExecutionLabels(flags));
    text(
      "#version-ledger-source-summary",
      "Source: " + (source.preview_title || friendlyLabel(source.source_surface))
        + " / Schema: " + (source.schema_version || "")
        + " / Surface: " + friendlyLabel(source.source_surface)
    );
    text(
      "#version-ledger-base-snapshot",
      (snapshot.display_name || "Synthetic persona")
        + " / Persona: " + (snapshot.persona_id || "")
        + " / Source: " + friendlyLabel(snapshot.source_label)
        + " / Runtime ref: " + (snapshot.runtime_state_ref || "none")
    );
    items("#version-ledger-draft-list", ledger.drafts || [], function (draft) {
      return appendVersionDraftCard(draft, conflictById, rollbackById);
    }, "version-draft-card");
    items("#version-ledger-conflict-list", ledger.conflict_notes || [], function (conflict) {
      return appendVersionConflictCard(conflict);
    }, "version-conflict-card");
    items("#version-ledger-rollback-list", ledger.rollback_ref_index || [], function (rollback) {
      return appendVersionRollbackCard(rollback);
    }, "version-rollback-card");
    items("#version-ledger-outcome-list", ledger.review_outcome_labels || [], function (outcome) {
      return appendVersionOutcomeCard(outcome);
    }, "version-outcome-card");
  }

  function appendVersionDraftCard(draft, conflictById, rollbackById) {
    const conflicts = (draft.conflict_note_ids || []).map(function (id) {
      const conflict = conflictById[id] || {};
      return (conflict.conflict_code || friendlyLabel(id)) + ": " + (conflict.safe_summary || "review required");
    });
    const rollbacks = (draft.rollback_ref_ids || []).map(function (id) {
      const rollback = rollbackById[id] || {};
      return (rollback.restore_summary || friendlyLabel(id));
    });
    return "<div class='item-title'>" + friendlyLabel(draft.reviewer_outcome) + "</div>"
      + "<div>" + (draft.after_version_summary || "") + "</div>"
      + "<div class='item-meta'>Before: " + (draft.before_snapshot_summary || "") + "</div>"
      + "<div class='item-meta'>Included patches: " + friendlyList(draft.source_patch_ids || []) + "</div>"
      + "<div class='item-meta'>Excluded patches: " + friendlyList(draft.excluded_patch_ids || []) + "</div>"
      + "<div class='item-meta'>Risks: " + friendlyList(draft.risk_label_ids || []) + "</div>"
      + "<div class='item-meta'>Conflicts: " + (conflicts.join(" / ") || "none") + "</div>"
      + "<div class='item-meta'>Rollback refs: " + (rollbacks.join(" / ") || "none") + "</div>"
      + "<div class='item-meta'>Status: " + friendlyLabel(draft.apply_status)
      + " / Mutation: " + String(draft.mutation_allowed === true)
      + (draft.rejection_reason ? " / Reason: " + draft.rejection_reason : "")
      + "</div>";
  }

  function appendVersionConflictCard(conflict) {
    return "<div class='item-title'>" + friendlyLabel(conflict.conflict_code) + "</div>"
      + "<div>" + (conflict.safe_summary || "") + "</div>"
      + "<div class='item-meta'>Severity: " + friendlyLabel(conflict.severity)
      + " / Blocks auto apply: " + String(conflict.blocks_auto_apply === true)
      + "</div>"
      + "<div class='item-meta'>Mitigation: " + (conflict.mitigation_summary || "") + "</div>"
      + "<div class='item-meta'>Patches: " + friendlyList(conflict.related_patch_ids || []) + "</div>"
      + "<div class='item-meta'>Risks: " + friendlyList(conflict.related_risk_label_ids || []) + "</div>";
  }

  function appendVersionRollbackCard(rollback) {
    return "<div class='item-title'>" + friendlyLabel(rollback.rollback_ref_id) + "</div>"
      + "<div class='item-meta'>Drafts: " + friendlyList(rollback.related_draft_ids || []) + "</div>"
      + "<div class='item-meta'>Patches: " + friendlyList(rollback.related_patch_ids || []) + "</div>"
      + "<div class='item-meta'>M37 rollback notes: " + friendlyList(rollback.related_m37_rollback_note_ids || []) + "</div>"
      + "<div>Prior: " + (rollback.prior_summary || "") + "</div>"
      + "<div>Restore: " + (rollback.restore_summary || "") + "</div>"
      + "<div class='item-meta'>Runtime rollback ready: " + String(rollback.runtime_rollback_ready === true) + "</div>";
  }

  function appendVersionOutcomeCard(outcome) {
    return "<div class='item-title'>" + (outcome.label || friendlyLabel(outcome.outcome)) + "</div>"
      + "<div>" + (outcome.safe_summary || "") + "</div>"
      + "<div class='item-meta'>Outcome: " + friendlyLabel(outcome.outcome) + "</div>";
  }

  function versionLedgerNonExecutionLabels(flags) {
    return [
      flags.local_only === true ? "local only" : "",
      flags.synthetic_fixture === true ? "synthetic fixture" : "",
      flags.uses_model_provider === false ? "no provider" : "",
      flags.reads_private_sources === false ? "no private sources" : "",
      flags.writes_persona_store === false ? "no persona store" : "",
      flags.writes_persona_version_store === false ? "no persona version store" : "",
      flags.writes_memory_store === false ? "no memory store" : "",
      flags.writes_review_store === false ? "no review store" : "",
      flags.writes_runtime_store === false ? "no runtime writes" : "",
      flags.automatic_apply === false ? "preview only" : "",
      flags.sends_messages === false ? "no outbound" : "",
      flags.uses_platform_adapter === false ? "no adapter" : "",
      flags.uses_media_runtime === false ? "no media runtime" : ""
    ].filter(Boolean);
  }

  function drawPersonaSourceIntakeManifest(manifest) {
    const flags = manifest.non_execution_flags || {};
    const policy = manifest.apply_policy || {};

    text("#source-intake-title", manifest.manifest_title || "Synthetic persona source intake manifest");
    text("#source-intake-schema", friendlyLabel(manifest.schema_version || "m39 manifest"));
    labels("#source-intake-non-execution-list", sourceIntakeNonExecutionLabels(flags));
    text(
      "#source-intake-policy-summary",
      "Mode: " + friendlyLabel(policy.mode)
        + " / Files read: " + String(policy.source_files_read === true)
        + " / Raw retained: " + String(policy.raw_content_retained === true)
        + " / Embeddings: " + String(policy.creates_embeddings === true)
        + " / Extraction: " + String(policy.performs_extraction === true)
    );
    items("#source-intake-candidate-list", manifest.source_candidates || [], function (candidate) {
      return appendSourceCandidateCard(candidate);
    }, "source-candidate-card");
    items("#source-intake-gate-list", manifest.source_policy_gates || [], function (gate) {
      return appendSourceGateCard(gate);
    }, "source-gate-card");
    items("#source-intake-blocked-list", manifest.blocked_source_categories || [], function (category) {
      return appendSourceBlockedCard(category);
    }, "source-blocked-card");
    items("#source-intake-redaction-list", manifest.redaction_profiles || [], function (profile) {
      return appendSourceRedactionCard(profile);
    }, "source-redaction-card");
  }

  function appendSourceCandidateCard(candidate) {
    return "<div class='item-title'>" + (candidate.fixture_label || friendlyLabel(candidate.source_kind)) + "</div>"
      + "<div>" + (candidate.safe_summary || "") + "</div>"
      + "<div class='item-meta'>Kind: " + friendlyLabel(candidate.source_kind)
      + " / Owner: " + friendlyLabel(candidate.declared_owner)
      + "</div>"
      + "<div class='item-meta'>Consent: " + friendlyLabel(candidate.consent_status)
      + " / Minimization: " + friendlyLabel(candidate.minimization_status)
      + "</div>"
      + "<div class='item-meta'>Redaction: " + friendlyLabel(candidate.redaction_profile_id)
      + " / Eligible: " + String(candidate.extraction_eligible === true)
      + " / Raw retained: " + String(candidate.raw_content_retained === true)
      + "</div>"
      + "<div class='item-meta'>Blocked: " + (friendlyList(candidate.blocked_reason_ids || []) || "none") + "</div>"
      + "<div class='item-meta'>Review gates: " + friendlyList(candidate.review_gate_ids || []) + "</div>";
  }

  function appendSourceGateCard(gate) {
    return "<div class='item-title'>" + friendlyLabel(gate.gate_code) + "</div>"
      + "<div>" + (gate.safe_summary || "") + "</div>"
      + "<div class='item-meta'>Enabled: " + String(gate.enabled === true)
      + " / Blocks extraction: " + String(gate.blocks_extraction_when_failed === true)
      + "</div>";
  }

  function appendSourceBlockedCard(category) {
    return "<div class='item-title'>" + friendlyLabel(category.blocked_code) + "</div>"
      + "<div>" + (category.safe_summary || "") + "</div>"
      + "<div class='item-meta'>Severity: " + friendlyLabel(category.severity)
      + " / Blocks extraction: " + String(category.blocks_extraction === true)
      + "</div>";
  }

  function appendSourceRedactionCard(profile) {
    return "<div class='item-title'>" + (profile.profile_label || friendlyLabel(profile.redaction_profile_id)) + "</div>"
      + "<div>" + (profile.safe_summary || "") + "</div>"
      + "<div class='item-meta'>Status: " + friendlyLabel(profile.redaction_status)
      + " / Raw retained: " + String(profile.retains_raw_content === true)
      + " / Review: " + String(profile.requires_review === true)
      + "</div>";
  }

  function sourceIntakeNonExecutionLabels(flags) {
    return [
      flags.local_only === true ? "local only" : "",
      flags.synthetic_fixture === true ? "synthetic fixture" : "",
      flags.uses_model_provider === false ? "no provider" : "",
      flags.reads_private_sources === false ? "no private sources" : "",
      flags.retains_raw_source_content === false ? "no raw retention" : "",
      flags.creates_embeddings === false ? "no embeddings" : "",
      flags.performs_extraction === false ? "no extraction" : "",
      flags.writes_persona_store === false ? "no persona store" : "",
      flags.writes_persona_version_store === false ? "no persona version store" : "",
      flags.writes_memory_store === false ? "no memory store" : "",
      flags.writes_review_store === false ? "no review store" : "",
      flags.writes_runtime_store === false ? "no runtime writes" : "",
      flags.automatic_apply === false ? "preview only" : "",
      flags.sends_messages === false ? "no outbound" : "",
      flags.uses_platform_adapter === false ? "no adapter" : "",
      flags.uses_media_runtime === false ? "no media runtime" : ""
    ].filter(Boolean);
  }

  function drawPersonaSourceEvidenceMatrix(matrix) {
    const flags = matrix.non_execution_flags || {};
    const manifestRef = matrix.source_intake_manifest_ref || {};

    text("#source-evidence-title", matrix.matrix_title || "Synthetic persona source evidence matrix");
    text("#source-evidence-schema", friendlyLabel(matrix.schema_version || "m40 matrix"));
    labels("#source-evidence-non-execution-list", sourceEvidenceNonExecutionLabels(flags));
    text(
      "#source-evidence-manifest-summary",
      "Source: " + (manifestRef.manifest_title || friendlyLabel(manifestRef.source_surface))
        + " / Schema: " + (manifestRef.schema_version || "")
        + " / Surface: " + friendlyLabel(manifestRef.source_surface)
    );
    labels("#source-evidence-eligible-list", matrix.eligible_source_ids || []);
    items("#source-evidence-excluded-list", matrix.excluded_source_refs || [], function (ref) {
      return appendSourceEvidenceExcludedCard(ref);
    }, "source-excluded-card");
    items("#source-evidence-row-list", matrix.evidence_rows || [], function (row) {
      return appendSourceEvidenceRowCard(row);
    }, "source-evidence-card");
    items("#source-evidence-trait-list", matrix.trait_hypotheses || [], function (trait) {
      return appendSourceTraitHypothesisCard(trait);
    }, "source-trait-card");
    items("#source-evidence-quality-list", matrix.quality_labels || [], function (label) {
      return appendSourceQualityCard(label);
    }, "source-quality-card");
    items("#source-evidence-gate-list", matrix.review_gate_results || [], function (gate) {
      return appendSourceGateResultCard(gate);
    }, "source-gate-result-card");
  }

  function appendSourceEvidenceExcludedCard(ref) {
    return "<div class='item-title'>" + friendlyLabel(ref.source_kind) + "</div>"
      + "<div>" + (ref.safe_summary || "") + "</div>"
      + "<div class='item-meta'>Source: " + (ref.source_id || "")
      + " / Excluded: " + String(ref.excluded_from_evidence === true)
      + " / Raw retained: " + String(ref.raw_content_retained === true)
      + "</div>"
      + "<div class='item-meta'>Blocked: " + friendlyList(ref.blocked_reason_ids || []) + "</div>";
  }

  function appendSourceEvidenceRowCard(row) {
    return "<div class='item-title'>" + (row.evidence_row_id || friendlyLabel(row.evidence_kind)) + "</div>"
      + "<div>" + (row.safe_summary || "") + "</div>"
      + "<div class='item-meta'>Source: " + (row.source_id || "")
      + " / Kind: " + friendlyLabel(row.source_kind)
      + " / Quality: " + friendlyLabel(row.quality_label_id)
      + "</div>"
      + "<div class='item-meta'>Traits: " + friendlyList(row.supports_trait_paths || []) + "</div>"
      + "<div class='item-meta'>Gates: " + friendlyList(row.review_gate_result_ids || []) + "</div>"
      + "<div class='item-meta'>Raw retained: " + String(row.raw_content_retained === true) + "</div>";
  }

  function appendSourceTraitHypothesisCard(trait) {
    return "<div class='item-title'>" + friendlyLabel(trait.trait_path) + "</div>"
      + "<div>" + (trait.hypothesis_summary || "") + "</div>"
      + "<div class='item-meta'>Support: " + friendlyList(trait.supporting_evidence_row_ids || []) + "</div>"
      + "<div class='item-meta'>Conflict: " + (friendlyList(trait.conflicting_evidence_row_ids || []) || "none") + "</div>"
      + "<div class='item-meta'>Confidence: " + friendlyLabel(trait.confidence_band)
      + " / Status: " + friendlyLabel(trait.apply_status)
      + " / Mutation: " + String(trait.mutation_allowed === true)
      + "</div>"
      + "<div class='item-meta'>Uncertainty: " + (trait.uncertainty_summary || "") + "</div>";
  }

  function appendSourceQualityCard(label) {
    return "<div class='item-title'>" + friendlyLabel(label.quality_code) + "</div>"
      + "<div>" + (label.safe_summary || "") + "</div>"
      + "<div class='item-meta'>Severity: " + friendlyLabel(label.severity)
      + " / Blocks unreviewed extraction: " + String(label.blocks_unreviewed_extraction === true)
      + "</div>";
  }

  function appendSourceGateResultCard(gate) {
    return "<div class='item-title'>" + friendlyLabel(gate.gate_code) + "</div>"
      + "<div>" + (gate.safe_summary || "") + "</div>"
      + "<div class='item-meta'>Status: " + friendlyLabel(gate.status)
      + " / Blocks extraction: " + String(gate.blocks_extraction_when_failed === true)
      + "</div>";
  }

  function sourceEvidenceNonExecutionLabels(flags) {
    return [
      flags.local_only === true ? "local only" : "",
      flags.synthetic_fixture === true ? "synthetic fixture" : "",
      flags.uses_model_provider === false ? "no provider" : "",
      flags.reads_private_sources === false ? "no private sources" : "",
      flags.retains_raw_source_content === false ? "no raw retention" : "",
      flags.creates_embeddings === false ? "no embeddings" : "",
      flags.performs_extraction === false ? "no extraction" : "",
      flags.writes_persona_store === false ? "no persona store" : "",
      flags.writes_persona_version_store === false ? "no persona version store" : "",
      flags.writes_memory_store === false ? "no memory store" : "",
      flags.writes_review_store === false ? "no review store" : "",
      flags.writes_runtime_store === false ? "no runtime writes" : "",
      flags.automatic_apply === false ? "preview only" : "",
      flags.sends_messages === false ? "no outbound" : "",
      flags.uses_platform_adapter === false ? "no adapter" : "",
      flags.uses_media_runtime === false ? "no media runtime" : ""
    ].filter(Boolean);
  }

  function drawSourceEvidencePersonaProposal(proposal) {
    const flags = proposal.non_execution_flags || {};
    const matrixRef = proposal.source_evidence_matrix_ref || {};

    text("#source-proposal-title", proposal.proposal_title || "Synthetic source evidence persona proposal");
    text("#source-proposal-schema", friendlyLabel(proposal.schema_version || "m41 proposal"));
    labels("#source-proposal-non-execution-list", sourceProposalNonExecutionLabels(flags));
    text(
      "#source-proposal-matrix-summary",
      "Matrix: " + (matrixRef.matrix_title || friendlyLabel(matrixRef.source_surface))
        + " / Schema: " + (matrixRef.schema_version || "")
        + " / Surface: " + friendlyLabel(matrixRef.source_surface)
    );
    items("#source-proposal-candidate-list", proposal.proposal_candidates || [], function (candidate) {
      return appendSourceProposalCandidateCard(candidate);
    }, "source-proposal-card");
    items("#source-proposal-risk-list", proposal.risk_labels || [], function (risk) {
      return appendSourceProposalRiskCard(risk);
    }, "source-proposal-risk-card");
    items("#source-proposal-rollback-list", proposal.rollback_notes || [], function (note) {
      return appendSourceProposalRollbackCard(note);
    }, "source-proposal-rollback-card");
    items("#source-proposal-gate-list", proposal.review_gate_results || [], function (gate) {
      return appendSourceProposalGateCard(gate);
    }, "source-proposal-gate-card");
    items("#source-proposal-outcome-list", proposal.proposal_outcome_labels || [], function (label) {
      return appendSourceProposalOutcomeCard(label);
    }, "source-proposal-outcome-card");
  }

  function appendSourceProposalCandidateCard(candidate) {
    return "<div class='item-title'>" + friendlyLabel(candidate.persona_field_path) + "</div>"
      + "<div>" + (candidate.proposed_value_summary || "") + "</div>"
      + "<div class='item-meta'>Rationale: " + (candidate.rationale_summary || "") + "</div>"
      + "<div class='item-meta'>Traits: " + friendlyList(candidate.source_trait_hypothesis_ids || []) + "</div>"
      + "<div class='item-meta'>Evidence: " + friendlyList(candidate.supporting_evidence_row_ids || []) + "</div>"
      + "<div class='item-meta'>Confidence: " + friendlyLabel(candidate.confidence_band)
      + " / Status: " + friendlyLabel(candidate.proposal_status)
      + " / Mutation: " + String(candidate.mutation_allowed === true)
      + "</div>"
      + "<div class='item-meta'>Risks: " + friendlyList(candidate.risk_label_ids || []) + "</div>"
      + "<div class='item-meta'>Rollback: " + friendlyList(candidate.rollback_note_ids || []) + "</div>"
      + "<div class='item-meta'>Review gates: " + friendlyList(candidate.review_gate_result_ids || []) + "</div>";
  }

  function appendSourceProposalRiskCard(risk) {
    return "<div class='item-title'>" + friendlyLabel(risk.risk_code) + "</div>"
      + "<div>" + (risk.safe_summary || "") + "</div>"
      + "<div class='item-meta'>Severity: " + friendlyLabel(risk.severity)
      + " / Blocks auto apply: " + String(risk.blocks_auto_apply === true)
      + "</div>";
  }

  function appendSourceProposalRollbackCard(note) {
    return "<div class='item-title'>" + friendlyLabel(note.rollback_note_id) + "</div>"
      + "<div>" + (note.safe_summary || "") + "</div>"
      + "<div class='item-meta'>Restore: " + (note.restore_summary || "") + "</div>"
      + "<div class='item-meta'>Runtime rollback ready: " + String(note.runtime_rollback_ready === true) + "</div>";
  }

  function appendSourceProposalGateCard(gate) {
    return "<div class='item-title'>" + friendlyLabel(gate.gate_code) + "</div>"
      + "<div>" + (gate.safe_summary || "") + "</div>"
      + "<div class='item-meta'>Status: " + friendlyLabel(gate.status)
      + " / Blocks apply when failed: " + String(gate.blocks_apply_when_failed === true)
      + "</div>";
  }

  function appendSourceProposalOutcomeCard(label) {
    return "<div class='item-title'>" + friendlyLabel(label.outcome) + "</div>"
      + "<div>" + (label.safe_summary || "") + "</div>";
  }

  function sourceProposalNonExecutionLabels(flags) {
    return [
      flags.local_only === true ? "local only" : "",
      flags.synthetic_fixture === true ? "synthetic fixture" : "",
      flags.uses_model_provider === false ? "no provider" : "",
      flags.reads_private_sources === false ? "no private sources" : "",
      flags.retains_raw_source_content === false ? "no raw retention" : "",
      flags.creates_embeddings === false ? "no embeddings" : "",
      flags.performs_extraction === false ? "no extraction" : "",
      flags.writes_persona_store === false ? "no persona store" : "",
      flags.writes_persona_version_store === false ? "no persona version store" : "",
      flags.writes_memory_store === false ? "no memory store" : "",
      flags.writes_review_store === false ? "no review store" : "",
      flags.writes_runtime_store === false ? "no runtime writes" : "",
      flags.automatic_apply === false ? "preview only" : "",
      flags.sends_messages === false ? "no outbound" : "",
      flags.uses_platform_adapter === false ? "no adapter" : "",
      flags.uses_media_runtime === false ? "no media runtime" : ""
    ].filter(Boolean);
  }

  function drawSourceProposalPersonaDraft(draft) {
    const flags = draft.non_execution_flags || {};
    const policy = draft.apply_policy || {};
    const proposalRef = draft.source_proposal_ref || {};
    const baseSnapshot = draft.base_persona_snapshot || {};

    text("#source-draft-title", draft.draft_title || "Synthetic proposal-linked persona draft");
    text("#source-draft-schema", friendlyLabel(draft.schema_version || "m42 draft"));
    labels("#source-draft-non-execution-list", sourceDraftNonExecutionLabels(flags));
    text(
      "#source-draft-proposal-summary",
      "Proposal: " + (proposalRef.proposal_title || friendlyLabel(proposalRef.source_surface))
        + " / Schema: " + (proposalRef.schema_version || "")
        + " / Policy: " + friendlyLabel(policy.mode || "preview_only")
        + " / Writes runtime: " + String(policy.writes_runtime_store === true)
    );
    text(
      "#source-draft-base-snapshot",
      (baseSnapshot.display_name || "Synthetic persona")
        + " / " + (baseSnapshot.snapshot_summary || "")
        + " / Disclosure: " + (baseSnapshot.ai_identity_disclosure || "")
        + " / Runtime written: " + String(baseSnapshot.runtime_snapshot_written === true)
    );
    labels("#source-draft-selected-proposal-list", draft.selected_proposal_ids || []);
    items("#source-draft-field-change-list", draft.draft_field_changes || [], function (change) {
      return appendSourceDraftFieldChangeCard(change);
    }, "source-draft-card");
    items("#source-draft-unchanged-field-list", draft.unchanged_field_summaries || [], function (field) {
      return appendSourceDraftUnchangedFieldCard(field);
    }, "source-draft-unchanged-card");
    items("#source-draft-conflict-list", draft.conflict_notes || [], function (note) {
      return appendSourceDraftConflictCard(note);
    }, "source-draft-conflict-card");
    items("#source-draft-rollback-list", draft.rollback_refs || [], function (ref) {
      return appendSourceDraftRollbackCard(ref);
    }, "source-draft-rollback-card");
    items("#source-draft-gate-list", draft.review_gate_results || [], function (gate) {
      return appendSourceDraftGateCard(gate);
    }, "source-draft-gate-card");
    items("#source-draft-outcome-list", draft.draft_outcome_labels || [], function (label) {
      return appendSourceDraftOutcomeCard(label);
    }, "source-draft-outcome-card");
  }

  function appendSourceDraftFieldChangeCard(change) {
    return "<div class='item-title'>" + friendlyLabel(change.persona_field_path) + "</div>"
      + "<div><strong>Before:</strong> " + (change.before_summary || "") + "</div>"
      + "<div><strong>After:</strong> " + (change.after_summary || "") + "</div>"
      + "<div class='item-meta'>Proposals: " + friendlyList(change.source_proposal_ids || []) + "</div>"
      + "<div class='item-meta'>Traits: " + friendlyList(change.source_trait_hypothesis_ids || []) + "</div>"
      + "<div class='item-meta'>Evidence: " + friendlyList(change.supporting_evidence_row_ids || []) + "</div>"
      + "<div class='item-meta'>Confidence: " + friendlyLabel(change.confidence_band)
      + " / Status: " + friendlyLabel(change.draft_status)
      + " / Mutation: " + String(change.mutation_allowed === true)
      + "</div>"
      + "<div class='item-meta'>Risks: " + friendlyList(change.risk_label_ids || []) + "</div>"
      + "<div class='item-meta'>Conflicts: " + friendlyList(change.conflict_note_ids || []) + "</div>"
      + "<div class='item-meta'>Rollback: " + friendlyList(change.rollback_ref_ids || []) + "</div>"
      + "<div class='item-meta'>Review gates: " + friendlyList(change.review_gate_result_ids || []) + "</div>";
  }

  function appendSourceDraftUnchangedFieldCard(field) {
    return "<div class='item-title'>" + friendlyLabel(field.field_path) + "</div>"
      + "<div>" + (field.safe_summary || "") + "</div>"
      + "<div class='item-meta'>Reason: " + (field.reason || "") + "</div>";
  }

  function appendSourceDraftConflictCard(note) {
    return "<div class='item-title'>" + friendlyLabel(note.conflict_code) + "</div>"
      + "<div>" + (note.safe_summary || "") + "</div>"
      + "<div class='item-meta'>Severity: " + friendlyLabel(note.severity)
      + " / Blocks auto apply: " + String(note.blocks_auto_apply === true)
      + "</div>";
  }

  function appendSourceDraftRollbackCard(ref) {
    return "<div class='item-title'>" + friendlyLabel(ref.rollback_ref_id) + "</div>"
      + "<div>" + (ref.safe_summary || "") + "</div>"
      + "<div class='item-meta'>Restore: " + (ref.restore_summary || "") + "</div>"
      + "<div class='item-meta'>Runtime rollback ready: " + String(ref.runtime_rollback_ready === true) + "</div>";
  }

  function appendSourceDraftGateCard(gate) {
    return "<div class='item-title'>" + friendlyLabel(gate.gate_code) + "</div>"
      + "<div>" + (gate.safe_summary || "") + "</div>"
      + "<div class='item-meta'>Status: " + friendlyLabel(gate.status)
      + " / Blocks apply when failed: " + String(gate.blocks_apply_when_failed === true)
      + "</div>";
  }

  function appendSourceDraftOutcomeCard(label) {
    return "<div class='item-title'>" + friendlyLabel(label.outcome) + "</div>"
      + "<div>" + (label.safe_summary || "") + "</div>";
  }

  function sourceDraftNonExecutionLabels(flags) {
    return [
      flags.local_only === true ? "local only" : "",
      flags.synthetic_fixture === true ? "synthetic fixture" : "",
      flags.uses_model_provider === false ? "no provider" : "",
      flags.reads_private_sources === false ? "no private sources" : "",
      flags.retains_raw_source_content === false ? "no raw retention" : "",
      flags.creates_embeddings === false ? "no embeddings" : "",
      flags.performs_extraction === false ? "no extraction" : "",
      flags.writes_persona_store === false ? "no persona store" : "",
      flags.writes_persona_version_store === false ? "no persona version store" : "",
      flags.writes_memory_store === false ? "no memory store" : "",
      flags.writes_review_store === false ? "no review store" : "",
      flags.writes_runtime_store === false ? "no runtime writes" : "",
      flags.automatic_apply === false ? "preview only" : "",
      flags.sends_messages === false ? "no outbound" : "",
      flags.uses_platform_adapter === false ? "no adapter" : "",
      flags.uses_media_runtime === false ? "no media runtime" : ""
    ].filter(Boolean);
  }

  function drawSourceDraftApplyReadiness(readiness) {
    const flags = readiness.non_execution_flags || {};
    const policy = readiness.apply_policy || {};
    const draftRef = readiness.source_draft_ref || {};

    text("#source-readiness-title", readiness.readiness_title || "Synthetic source draft apply-readiness preview");
    text("#source-readiness-schema", friendlyLabel(readiness.schema_version || "m43 readiness"));
    labels("#source-readiness-non-execution-list", readinessNonExecutionLabels(flags));
    text(
      "#source-readiness-draft-summary",
      "Draft: " + (draftRef.draft_title || friendlyLabel(draftRef.source_surface))
        + " / Schema: " + (draftRef.schema_version || "")
        + " / Surface: " + friendlyLabel(draftRef.source_surface)
    );
    text(
      "#source-readiness-apply-policy-summary",
      "Policy: " + friendlyLabel(policy.mode || "preview_only")
        + " / Executor: " + String(policy.apply_executor_enabled === true)
        + " / Writes persona: " + String(policy.writes_persona_card === true)
        + " / Runtime writes: " + String(policy.writes_runtime_store === true)
    );
    labels("#source-readiness-evaluated-change-list", readiness.evaluated_draft_change_ids || []);
    items("#source-readiness-field-record-list", readiness.field_readiness_records || [], function (record) {
      return appendSourceReadinessFieldRecordCard(record);
    }, "source-readiness-card");
    items("#source-readiness-blocked-condition-list", readiness.blocked_condition_records || [], function (condition) {
      return appendSourceReadinessConditionCard(condition);
    }, "source-readiness-condition-card");
    items("#source-readiness-gate-ref-list", readiness.required_review_gate_refs || [], function (gate) {
      return appendSourceReadinessGateCard(gate);
    }, "source-readiness-gate-card");
    items("#source-readiness-rollback-list", readiness.rollback_dependency_refs || [], function (rollback) {
      return appendSourceReadinessRollbackCard(rollback);
    }, "source-readiness-rollback-card");
    items("#source-readiness-outcome-list", readiness.readiness_outcome_labels || [], function (label) {
      return appendSourceReadinessOutcomeCard(label);
    }, "source-readiness-outcome-card");
  }

  function appendSourceReadinessFieldRecordCard(record) {
    return "<div class='item-title'>" + friendlyLabel(record.persona_field_path) + "</div>"
      + "<div>" + (record.safe_summary || "") + "</div>"
      + "<div class='item-meta'>Draft change: " + (record.draft_change_id || "") + "</div>"
      + "<div class='item-meta'>Outcome: " + friendlyLabel(record.readiness_outcome)
      + " / Mutation: " + String(record.mutation_allowed === true)
      + " / Preview: " + String(record.preview_only === true)
      + "</div>"
      + "<div class='item-meta'>Blocked conditions: " + (friendlyList(record.blocking_condition_ids || []) || "none") + "</div>"
      + "<div class='item-meta'>Review gates: " + friendlyList(record.required_review_gate_result_ids || []) + "</div>"
      + "<div class='item-meta'>Rollback refs: " + friendlyList(record.rollback_ref_ids || []) + "</div>"
      + "<div class='item-meta'>Future design: " + (record.future_apply_design_notes || "") + "</div>";
  }

  function appendSourceReadinessConditionCard(condition) {
    return "<div class='item-title'>" + friendlyLabel(condition.condition_code) + "</div>"
      + "<div>" + (condition.safe_summary || "") + "</div>"
      + "<div class='item-meta'>Severity: " + friendlyLabel(condition.severity)
      + " / Blocks apply: " + String(condition.blocks_apply === true)
      + "</div>"
      + "<div class='item-meta'>Affected changes: " + friendlyList(condition.affected_draft_change_ids || []) + "</div>";
  }

  function appendSourceReadinessGateCard(gate) {
    return "<div class='item-title'>" + friendlyLabel(gate.gate_code) + "</div>"
      + "<div>" + (gate.safe_summary || "") + "</div>"
      + "<div class='item-meta'>Status: " + friendlyLabel(gate.status)
      + " / Required before apply: " + String(gate.required_before_apply === true)
      + "</div>";
  }

  function appendSourceReadinessRollbackCard(rollback) {
    return "<div class='item-title'>" + friendlyLabel(rollback.rollback_ref_id) + "</div>"
      + "<div class='item-meta'>Dependent changes: " + friendlyList(rollback.dependent_draft_change_ids || []) + "</div>"
      + "<div class='item-meta'>Restore: " + (rollback.restore_summary || "") + "</div>"
      + "<div class='item-meta'>Runtime rollback ready: " + String(rollback.runtime_rollback_ready === true) + "</div>";
  }

  function appendSourceReadinessOutcomeCard(label) {
    return "<div class='item-title'>" + friendlyLabel(label.outcome) + "</div>"
      + "<div>" + (label.safe_summary || "") + "</div>";
  }

  function readinessNonExecutionLabels(flags) {
    return [
      flags.local_only === true ? "local only" : "",
      flags.synthetic_fixture === true ? "synthetic fixture" : "",
      flags.uses_model_provider === false ? "no provider" : "",
      flags.reads_private_sources === false ? "no private sources" : "",
      flags.retains_raw_source_content === false ? "no raw retention" : "",
      flags.creates_embeddings === false ? "no embeddings" : "",
      flags.performs_extraction === false ? "no extraction" : "",
      flags.writes_persona_store === false ? "no persona store" : "",
      flags.writes_persona_version_store === false ? "no persona version store" : "",
      flags.writes_memory_store === false ? "no memory store" : "",
      flags.writes_review_store === false ? "no review store" : "",
      flags.writes_runtime_store === false ? "no runtime writes" : "",
      flags.automatic_apply === false ? "preview only" : "",
      flags.sends_messages === false ? "no outbound" : "",
      flags.uses_platform_adapter === false ? "no adapter" : "",
      flags.uses_media_runtime === false ? "no media runtime" : ""
    ].filter(Boolean);
  }

  function attachPersonaWorkbenchReviewCards(stateValue) {
    const review = stateValue.review_workspace || {};
    const cards = personaWorkbenchReviewCards(stateValue.persona_distillation_workbench || {});
    review.workbench_review_cards = cards;
    const tabs = review.filter_tabs || [];
    let found = false;
    tabs.forEach(function (tab) {
      if (tab.key === "distillation") {
        tab.label = "Distillation";
        tab.count = cards.length;
        found = true;
      }
    });
    if (!found) {
      tabs.push({ key: "distillation", label: "Distillation", count: cards.length });
    }
    review.filter_tabs = tabs;
    stateValue.review_workspace = review;
  }

  function personaWorkbenchReviewCards(workbench) {
    const traitCards = (workbench.extracted_trait_candidates || []).map(function (candidate) {
      return {
        schema_version: "review_workspace_persona_workbench_card_v1",
        card_kind: "persona_workbench_trait_review",
        title: "Persona distillation trait",
        display_label: String(candidate.category || "trait").replace(/_/g, " "),
        safe_summary: candidate.safe_summary || "",
        filter_keys: ["all", "distillation", "persona"],
        status_badges: [
          {
            label: "Distillation trait needs review",
            tone: "review",
            issue_codes: [],
            blocking_issue_codes: [],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        candidate_id: candidate.trait_id,
        candidate_kind: "persona_distillation_trait",
        trait_category: candidate.category,
        candidate_value: candidate.candidate_value,
        confidence_band: candidate.confidence_band,
        evidence_ref_ids: candidate.evidence_ref_ids || [],
        source_surface: "persona_distillation_workbench",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    const blockedCards = (workbench.blocked_requests || []).map(function (request) {
      return {
        schema_version: "review_workspace_persona_workbench_card_v1",
        card_kind: "persona_workbench_blocked_request",
        title: "Blocked persona request",
        display_label: String(request.request_type || "blocked").replace(/_/g, " "),
        safe_summary: request.safe_summary || "",
        filter_keys: ["all", "distillation", "blocked"],
        status_badges: [
          {
            label: "Persona request blocked",
            tone: "blocked",
            issue_codes: [],
            blocking_issue_codes: [request.request_type || "blocked"],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        blocked_request_id: request.blocked_request_id,
        request_type: request.request_type,
        risk_reason: request.risk_reason,
        user_facing_explanation: request.user_facing_explanation,
        blocked_status: request.status || "blocked",
        source_surface: "persona_distillation_workbench",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    return traitCards.concat(blockedCards);
  }

  function attachPersonaEvolutionReviewCards(stateValue) {
    const review = stateValue.review_workspace || {};
    const cards = personaEvolutionReviewCards(stateValue.persona_evolution_preview || {});
    review.evolution_review_cards = cards;
    const tabs = review.filter_tabs || [];
    let found = false;
    tabs.forEach(function (tab) {
      if (tab.key === "evolution") {
        tab.label = "Evolution";
        tab.count = cards.length;
        found = true;
      }
    });
    if (!found) {
      tabs.push({ key: "evolution", label: "Evolution", count: cards.length });
    }
    review.filter_tabs = tabs;
    stateValue.review_workspace = review;
  }

  function personaEvolutionReviewCards(evolution) {
    const patchCards = (evolution.proposed_patch_candidates || []).map(function (patch) {
      return {
        schema_version: "review_workspace_persona_evolution_card_v1",
        card_kind: "persona_evolution_patch_review",
        title: "Persona evolution patch",
        display_label: String(patch.changed_field_path || "patch").replace(/_/g, " "),
        safe_summary: patch.rationale_summary || "",
        filter_keys: ["all", "evolution", "persona"],
        status_badges: [
          {
            label: "Evolution patch needs review",
            tone: "review",
            issue_codes: patch.risk_label_ids || [],
            blocking_issue_codes: [],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        patch_id: patch.patch_id,
        candidate_kind: "persona_evolution_patch",
        patch_kind: patch.patch_kind,
        source_trait_candidate_ids: patch.source_trait_candidate_ids || [],
        changed_field_path: patch.changed_field_path,
        before_summary: patch.before_summary,
        after_summary: patch.after_summary,
        rationale_summary: patch.rationale_summary,
        confidence_band: patch.confidence_band,
        evidence_ref_ids: patch.evidence_ref_ids || [],
        risk_label_ids: patch.risk_label_ids || [],
        rollback_note_ids: patch.rollback_note_ids || [],
        source_surface: "persona_evolution_preview",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    const riskCards = (evolution.risk_labels || []).map(function (risk) {
      return {
        schema_version: "review_workspace_persona_evolution_card_v1",
        card_kind: "persona_evolution_risk_review",
        title: "Persona evolution risk",
        display_label: String(risk.risk_code || "risk").replace(/_/g, " "),
        safe_summary: risk.safe_summary || "",
        filter_keys: ["all", "evolution", "persona"],
        status_badges: [
          {
            label: "Evolution risk blocks auto apply",
            tone: risk.severity === "high" ? "blocked" : "review",
            issue_codes: [risk.risk_code || "risk"],
            blocking_issue_codes: risk.blocks_auto_apply === true ? [risk.risk_code || "risk"] : [],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        risk_label_id: risk.risk_label_id,
        risk_code: risk.risk_code,
        severity: risk.severity,
        mitigation_summary: risk.mitigation_summary,
        blocks_auto_apply: risk.blocks_auto_apply === true,
        source_surface: "persona_evolution_preview",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    const rollbackCards = (evolution.rollback_notes || []).map(function (note) {
      return {
        schema_version: "review_workspace_persona_evolution_card_v1",
        card_kind: "persona_evolution_rollback_review",
        title: "Persona evolution rollback",
        display_label: String(note.rollback_note_id || "rollback").replace(/_/g, " "),
        safe_summary: note.rollback_summary || "",
        filter_keys: ["all", "evolution", "persona"],
        status_badges: [
          {
            label: "Rollback metadata only",
            tone: "info",
            issue_codes: [],
            blocking_issue_codes: [],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        rollback_note_id: note.rollback_note_id,
        target_patch_ids: note.target_patch_ids || [],
        prior_summary: note.prior_summary,
        rollback_summary: note.rollback_summary,
        required_reviewer_action: note.required_reviewer_action,
        runtime_rollback_ready: false,
        source_surface: "persona_evolution_preview",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    const exclusionCards = (evolution.blocked_source_exclusions || []).map(function (exclusion) {
      return {
        schema_version: "review_workspace_persona_evolution_card_v1",
        card_kind: "persona_evolution_blocked_source_exclusion",
        title: "Blocked evolution source",
        display_label: String(exclusion.request_type || "blocked").replace(/_/g, " "),
        safe_summary: exclusion.safe_summary || "",
        filter_keys: ["all", "evolution", "blocked"],
        status_badges: [
          {
            label: "Blocked source excluded",
            tone: "blocked",
            issue_codes: [exclusion.request_type || "blocked"],
            blocking_issue_codes: [exclusion.request_type || "blocked"],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        blocked_request_id: exclusion.blocked_request_id,
        request_type: exclusion.request_type,
        exclusion_reason: exclusion.exclusion_reason,
        excluded_from_patch_generation: exclusion.excluded_from_patch_generation === true,
        source_surface: "persona_evolution_preview",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    return patchCards.concat(riskCards).concat(rollbackCards).concat(exclusionCards);
  }

  function attachPersonaVersionDraftReviewCards(stateValue) {
    const review = stateValue.review_workspace || {};
    const cards = personaVersionDraftReviewCards(stateValue.persona_version_draft_ledger || {});
    review.version_review_cards = cards;
    const tabs = review.filter_tabs || [];
    let found = false;
    tabs.forEach(function (tab) {
      if (tab.key === "version") {
        tab.label = "Version";
        tab.count = cards.length;
        found = true;
      }
    });
    if (!found) {
      tabs.push({ key: "version", label: "Version", count: cards.length });
    }
    review.filter_tabs = tabs;
    stateValue.review_workspace = review;
  }

  function personaVersionDraftReviewCards(ledger) {
    const draftCards = (ledger.drafts || []).map(function (draft) {
      return {
        schema_version: "review_workspace_persona_version_card_v1",
        card_kind: "persona_version_draft_review",
        title: "Persona version draft",
        display_label: String(draft.reviewer_outcome || "draft").replace(/_/g, " "),
        safe_summary: draft.after_version_summary || "",
        filter_keys: ["all", "version", "persona"],
        status_badges: [
          {
            label: "Version draft needs review",
            tone: draft.reviewer_outcome === "rejected_boundary_risk" ? "blocked" : "review",
            issue_codes: draft.conflict_note_ids || [],
            blocking_issue_codes: draft.reviewer_outcome === "rejected_boundary_risk" ? (draft.conflict_note_ids || []) : [],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        draft_id: draft.draft_id,
        candidate_kind: "persona_version_draft",
        draft_kind: draft.draft_kind,
        reviewer_outcome: draft.reviewer_outcome,
        source_patch_ids: draft.source_patch_ids || [],
        excluded_patch_ids: draft.excluded_patch_ids || [],
        risk_label_ids: draft.risk_label_ids || [],
        conflict_note_ids: draft.conflict_note_ids || [],
        rollback_ref_ids: draft.rollback_ref_ids || [],
        before_snapshot_summary: draft.before_snapshot_summary,
        after_version_summary: draft.after_version_summary,
        rejection_reason: draft.rejection_reason || "",
        source_surface: "persona_version_draft_ledger",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    const conflictCards = (ledger.conflict_notes || []).map(function (conflict) {
      return {
        schema_version: "review_workspace_persona_version_card_v1",
        card_kind: "persona_version_conflict_review",
        title: "Persona version conflict",
        display_label: String(conflict.conflict_code || "conflict").replace(/_/g, " "),
        safe_summary: conflict.safe_summary || "",
        filter_keys: ["all", "version", "persona"],
        status_badges: [
          {
            label: "Version conflict blocks auto apply",
            tone: conflict.severity === "high" ? "blocked" : "review",
            issue_codes: [conflict.conflict_code || "conflict"],
            blocking_issue_codes: conflict.blocks_auto_apply === true ? [conflict.conflict_code || "conflict"] : [],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        conflict_note_id: conflict.conflict_note_id,
        conflict_code: conflict.conflict_code,
        severity: conflict.severity,
        mitigation_summary: conflict.mitigation_summary,
        related_patch_ids: conflict.related_patch_ids || [],
        related_risk_label_ids: conflict.related_risk_label_ids || [],
        blocks_auto_apply: conflict.blocks_auto_apply === true,
        source_surface: "persona_version_draft_ledger",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    const rollbackCards = (ledger.rollback_ref_index || []).map(function (rollback) {
      return {
        schema_version: "review_workspace_persona_version_card_v1",
        card_kind: "persona_version_rollback_review",
        title: "Persona version rollback ref",
        display_label: String(rollback.rollback_ref_id || "rollback").replace(/_/g, " "),
        safe_summary: rollback.restore_summary || "",
        filter_keys: ["all", "version", "persona"],
        status_badges: [
          {
            label: "Rollback ref metadata only",
            tone: "info",
            issue_codes: [],
            blocking_issue_codes: [],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        rollback_ref_id: rollback.rollback_ref_id,
        related_draft_ids: rollback.related_draft_ids || [],
        related_patch_ids: rollback.related_patch_ids || [],
        related_m37_rollback_note_ids: rollback.related_m37_rollback_note_ids || [],
        prior_summary: rollback.prior_summary,
        restore_summary: rollback.restore_summary,
        runtime_rollback_ready: false,
        source_surface: "persona_version_draft_ledger",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    const outcomeCards = (ledger.review_outcome_labels || []).map(function (outcome) {
      return {
        schema_version: "review_workspace_persona_version_card_v1",
        card_kind: "persona_version_outcome_review",
        title: "Persona version outcome",
        display_label: String(outcome.outcome || "outcome").replace(/_/g, " "),
        safe_summary: outcome.safe_summary || "",
        filter_keys: ["all", "version", "persona"],
        status_badges: [
          {
            label: "Outcome label",
            tone: "info",
            issue_codes: [],
            blocking_issue_codes: [],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        outcome: outcome.outcome,
        label: outcome.label,
        source_surface: "persona_version_draft_ledger",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    return draftCards.concat(conflictCards).concat(rollbackCards).concat(outcomeCards);
  }

  function attachPersonaSourceIntakeReviewCards(stateValue) {
    const review = stateValue.review_workspace || {};
    const cards = personaSourceIntakeReviewCards(stateValue.persona_source_intake_manifest || {});
    review.source_intake_review_cards = cards;
    const tabs = review.filter_tabs || [];
    let found = false;
    tabs.forEach(function (tab) {
      if (tab.key === "source") {
        tab.label = "Source";
        tab.count = cards.length;
        found = true;
      }
    });
    if (!found) {
      tabs.push({ key: "source", label: "Source", count: cards.length });
    }
    review.filter_tabs = tabs;
    stateValue.review_workspace = review;
  }

  function personaSourceIntakeReviewCards(manifest) {
    const candidateCards = (manifest.source_candidates || []).map(function (candidate) {
      const eligible = candidate.extraction_eligible === true;
      return {
        schema_version: "review_workspace_persona_source_intake_card_v1",
        card_kind: "persona_source_candidate_review",
        title: "Persona source candidate",
        display_label: String(candidate.source_kind || "source").replace(/_/g, " "),
        safe_summary: candidate.safe_summary || "",
        filter_keys: ["all", "source", "persona"],
        status_badges: [
          {
            label: "Source candidate needs review",
            tone: eligible ? "review" : "blocked",
            issue_codes: candidate.blocked_reason_ids || [],
            blocking_issue_codes: eligible ? [] : (candidate.blocked_reason_ids || []),
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        source_id: candidate.source_id,
        candidate_kind: "persona_source_candidate",
        source_kind: candidate.source_kind,
        declared_owner: candidate.declared_owner,
        consent_status: candidate.consent_status,
        minimization_status: candidate.minimization_status,
        redaction_profile_id: candidate.redaction_profile_id,
        extraction_eligible: eligible,
        blocked_reason_ids: candidate.blocked_reason_ids || [],
        review_gate_ids: candidate.review_gate_ids || [],
        source_surface: "persona_source_intake_manifest",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    const gateCards = (manifest.source_policy_gates || []).map(function (gate) {
      return {
        schema_version: "review_workspace_persona_source_intake_card_v1",
        card_kind: "persona_source_policy_gate_review",
        title: "Persona source policy gate",
        display_label: String(gate.gate_code || "gate").replace(/_/g, " "),
        safe_summary: gate.safe_summary || "",
        filter_keys: ["all", "source", "blocked"],
        status_badges: [
          {
            label: "Source gate blocks failed extraction",
            tone: "review",
            issue_codes: [gate.gate_code || "gate"],
            blocking_issue_codes: gate.blocks_extraction_when_failed === true ? [gate.gate_code || "gate"] : [],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        gate_id: gate.gate_id,
        gate_code: gate.gate_code,
        enabled: gate.enabled === true,
        blocks_extraction_when_failed: gate.blocks_extraction_when_failed === true,
        source_surface: "persona_source_intake_manifest",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    const blockedCards = (manifest.blocked_source_categories || []).map(function (category) {
      return {
        schema_version: "review_workspace_persona_source_intake_card_v1",
        card_kind: "persona_source_blocked_category_review",
        title: "Persona source blocked category",
        display_label: String(category.blocked_code || "blocked").replace(/_/g, " "),
        safe_summary: category.safe_summary || "",
        filter_keys: ["all", "source", "blocked"],
        status_badges: [
          {
            label: "Blocked source category",
            tone: "blocked",
            issue_codes: [category.blocked_code || "blocked"],
            blocking_issue_codes: [category.blocked_code || "blocked"],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        blocked_reason_id: category.blocked_reason_id,
        blocked_code: category.blocked_code,
        severity: category.severity,
        blocks_extraction: category.blocks_extraction === true,
        source_surface: "persona_source_intake_manifest",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    const redactionCards = (manifest.redaction_profiles || []).map(function (profile) {
      return {
        schema_version: "review_workspace_persona_source_intake_card_v1",
        card_kind: "persona_source_redaction_profile_review",
        title: "Persona source redaction profile",
        display_label: String(profile.profile_label || "redaction"),
        safe_summary: profile.safe_summary || "",
        filter_keys: ["all", "source", "persona"],
        status_badges: [
          {
            label: "Redaction profile metadata",
            tone: "info",
            issue_codes: [],
            blocking_issue_codes: [],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        redaction_profile_id: profile.redaction_profile_id,
        profile_label: profile.profile_label,
        redaction_status: profile.redaction_status,
        retains_raw_content: profile.retains_raw_content === true,
        requires_review: profile.requires_review === true,
        source_surface: "persona_source_intake_manifest",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    return candidateCards.concat(gateCards).concat(blockedCards).concat(redactionCards);
  }

  function attachPersonaSourceEvidenceReviewCards(stateValue) {
    const review = stateValue.review_workspace || {};
    const cards = personaSourceEvidenceReviewCards(stateValue.persona_source_evidence_matrix || {});
    review.source_evidence_review_cards = cards;
    const sourceIntakeCount = (review.source_intake_review_cards || []).length;
    const tabs = review.filter_tabs || [];
    let sourceFound = false;
    let evidenceFound = false;
    tabs.forEach(function (tab) {
      if (tab.key === "source") {
        tab.label = "Source";
        tab.count = sourceIntakeCount + cards.length;
        sourceFound = true;
      }
      if (tab.key === "evidence") {
        tab.label = "Evidence";
        tab.count = cards.length;
        evidenceFound = true;
      }
    });
    if (!sourceFound) {
      tabs.push({ key: "source", label: "Source", count: sourceIntakeCount + cards.length });
    }
    if (!evidenceFound) {
      tabs.push({ key: "evidence", label: "Evidence", count: cards.length });
    }
    review.filter_tabs = tabs;
    stateValue.review_workspace = review;
  }

  function personaSourceEvidenceReviewCards(matrix) {
    const exclusionCards = (matrix.excluded_source_refs || []).map(function (ref) {
      return {
        schema_version: "review_workspace_persona_source_evidence_card_v1",
        card_kind: "persona_source_evidence_exclusion_review",
        title: "Excluded source evidence",
        display_label: String(ref.source_kind || "excluded").replace(/_/g, " "),
        safe_summary: ref.safe_summary || "",
        filter_keys: ["all", "source", "evidence", "blocked"],
        status_badges: [
          {
            label: "Source excluded from evidence",
            tone: "blocked",
            issue_codes: ref.blocked_reason_ids || [],
            blocking_issue_codes: ref.blocked_reason_ids || [],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        source_id: ref.source_id,
        source_kind: ref.source_kind,
        blocked_reason_ids: ref.blocked_reason_ids || [],
        excluded_from_evidence: ref.excluded_from_evidence === true,
        raw_content_retained: false,
        source_surface: "persona_source_evidence_matrix",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    const evidenceCards = (matrix.evidence_rows || []).map(function (row) {
      return {
        schema_version: "review_workspace_persona_source_evidence_card_v1",
        card_kind: "persona_source_evidence_row_review",
        title: "Source evidence row",
        display_label: String(row.evidence_kind || "evidence").replace(/_/g, " "),
        safe_summary: row.safe_summary || "",
        filter_keys: ["all", "source", "evidence", "persona"],
        status_badges: [
          {
            label: "Evidence row needs review",
            tone: "review",
            issue_codes: [],
            blocking_issue_codes: [],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        evidence_row_id: row.evidence_row_id,
        source_id: row.source_id,
        source_kind: row.source_kind,
        evidence_kind: row.evidence_kind,
        quality_label_id: row.quality_label_id,
        supports_trait_paths: row.supports_trait_paths || [],
        uncertainty_notes: row.uncertainty_notes || [],
        review_gate_result_ids: row.review_gate_result_ids || [],
        raw_content_retained: false,
        source_surface: "persona_source_evidence_matrix",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    const traitCards = (matrix.trait_hypotheses || []).map(function (trait) {
      return {
        schema_version: "review_workspace_persona_source_evidence_card_v1",
        card_kind: "persona_source_trait_hypothesis_review",
        title: "Source trait hypothesis",
        display_label: String(trait.trait_path || "trait").replace(/_/g, " "),
        safe_summary: trait.hypothesis_summary || "",
        filter_keys: ["all", "source", "evidence", "persona"],
        status_badges: [
          {
            label: "Trait hypothesis preview",
            tone: "review",
            issue_codes: [],
            blocking_issue_codes: [],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        trait_hypothesis_id: trait.trait_hypothesis_id,
        trait_path: trait.trait_path,
        confidence_band: trait.confidence_band,
        supporting_evidence_row_ids: trait.supporting_evidence_row_ids || [],
        conflicting_evidence_row_ids: trait.conflicting_evidence_row_ids || [],
        uncertainty_summary: trait.uncertainty_summary || "",
        review_gate_result_ids: trait.review_gate_result_ids || [],
        apply_status: trait.apply_status || "preview_only",
        source_surface: "persona_source_evidence_matrix",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    const qualityCards = (matrix.quality_labels || []).map(function (quality) {
      const severity = quality.severity || "medium";
      return {
        schema_version: "review_workspace_persona_source_evidence_card_v1",
        card_kind: "persona_source_quality_label_review",
        title: "Source evidence quality",
        display_label: String(quality.quality_code || "quality").replace(/_/g, " "),
        safe_summary: quality.safe_summary || "",
        filter_keys: ["all", "source", "evidence"],
        status_badges: [
          {
            label: "Evidence quality label",
            tone: severity === "high" ? "blocked" : "review",
            issue_codes: [quality.quality_code || "quality"],
            blocking_issue_codes: severity === "high" ? [quality.quality_code || "quality"] : [],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        quality_label_id: quality.quality_label_id,
        quality_code: quality.quality_code,
        severity: severity,
        blocks_unreviewed_extraction: quality.blocks_unreviewed_extraction === true,
        source_surface: "persona_source_evidence_matrix",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    const gateCards = (matrix.review_gate_results || []).map(function (gate) {
      const status = gate.status || "needs_review";
      const tone = status === "passed" ? "eligible" : status === "blocked" ? "blocked" : "review";
      return {
        schema_version: "review_workspace_persona_source_evidence_card_v1",
        card_kind: "persona_source_review_gate_result_review",
        title: "Source evidence review gate",
        display_label: String(gate.gate_code || "gate").replace(/_/g, " "),
        safe_summary: gate.safe_summary || "",
        filter_keys: ["all", "source", "evidence"],
        status_badges: [
          {
            label: "Evidence gate " + String(status).replace(/_/g, " "),
            tone: tone,
            issue_codes: [gate.gate_code || "gate"],
            blocking_issue_codes: status === "blocked" ? [gate.gate_code || "gate"] : [],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        review_gate_result_id: gate.review_gate_result_id,
        gate_code: gate.gate_code,
        status: status,
        blocks_extraction_when_failed: gate.blocks_extraction_when_failed === true,
        source_surface: "persona_source_evidence_matrix",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    return exclusionCards.concat(evidenceCards).concat(traitCards).concat(qualityCards).concat(gateCards);
  }

  function attachSourceEvidencePersonaProposalReviewCards(stateValue) {
    const review = stateValue.review_workspace || {};
    const cards = sourceEvidencePersonaProposalReviewCards(stateValue.source_evidence_persona_proposal || {});
    review.source_proposal_review_cards = cards;
    const tabs = review.filter_tabs || [];
    let found = false;
    tabs.forEach(function (tab) {
      if (tab.key === "proposal") {
        tab.label = "Proposal";
        tab.count = cards.length;
        found = true;
      }
    });
    if (!found) {
      tabs.push({ key: "proposal", label: "Proposal", count: cards.length });
    }
    review.filter_tabs = tabs;
    stateValue.review_workspace = review;
  }

  function sourceEvidencePersonaProposalReviewCards(proposal) {
    const candidateCards = (proposal.proposal_candidates || []).map(function (candidate) {
      return {
        schema_version: "review_workspace_source_evidence_persona_proposal_card_v1",
        card_kind: "source_persona_proposal_candidate_review",
        title: "Source persona proposal",
        display_label: String(candidate.persona_field_path || "proposal").replace(/_/g, " "),
        safe_summary: candidate.proposed_value_summary || "",
        filter_keys: ["all", "proposal", "persona"],
        status_badges: [
          {
            label: "Persona proposal needs review",
            tone: "review",
            issue_codes: candidate.risk_label_ids || [],
            blocking_issue_codes: [],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        proposal_id: candidate.proposal_id,
        persona_field_path: candidate.persona_field_path,
        proposed_value_summary: candidate.proposed_value_summary || "",
        rationale_summary: candidate.rationale_summary || "",
        source_trait_hypothesis_ids: candidate.source_trait_hypothesis_ids || [],
        supporting_evidence_row_ids: candidate.supporting_evidence_row_ids || [],
        confidence_band: candidate.confidence_band || "",
        risk_label_ids: candidate.risk_label_ids || [],
        rollback_note_ids: candidate.rollback_note_ids || [],
        review_gate_result_ids: candidate.review_gate_result_ids || [],
        proposal_status: candidate.proposal_status || "preview_only",
        source_surface: "source_evidence_persona_proposal",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    const riskCards = (proposal.risk_labels || []).map(function (risk) {
      const severity = risk.severity || "medium";
      return {
        schema_version: "review_workspace_source_evidence_persona_proposal_card_v1",
        card_kind: "source_persona_proposal_risk_review",
        title: "Source persona proposal risk",
        display_label: String(risk.risk_code || "risk").replace(/_/g, " "),
        safe_summary: risk.safe_summary || "",
        filter_keys: ["all", "proposal", "risk"],
        status_badges: [
          {
            label: "Proposal risk label",
            tone: severity === "high" ? "blocked" : "review",
            issue_codes: [risk.risk_code || "risk"],
            blocking_issue_codes: [risk.risk_code || "risk"],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        risk_label_id: risk.risk_label_id,
        risk_code: risk.risk_code,
        severity: severity,
        blocks_auto_apply: risk.blocks_auto_apply === true,
        source_surface: "source_evidence_persona_proposal",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    const rollbackCards = (proposal.rollback_notes || []).map(function (note) {
      return {
        schema_version: "review_workspace_source_evidence_persona_proposal_card_v1",
        card_kind: "source_persona_proposal_rollback_review",
        title: "Source persona proposal rollback",
        display_label: String(note.rollback_note_id || "rollback").replace(/_/g, " "),
        safe_summary: note.safe_summary || "",
        filter_keys: ["all", "proposal"],
        status_badges: [
          {
            label: "Rollback note preview",
            tone: "review",
            issue_codes: [],
            blocking_issue_codes: [],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        rollback_note_id: note.rollback_note_id,
        restore_summary: note.restore_summary || "",
        runtime_rollback_ready: false,
        source_surface: "source_evidence_persona_proposal",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    const gateCards = (proposal.review_gate_results || []).map(function (gate) {
      const status = gate.status || "needs_review";
      return {
        schema_version: "review_workspace_source_evidence_persona_proposal_card_v1",
        card_kind: "source_persona_proposal_gate_review",
        title: "Source persona proposal review gate",
        display_label: String(gate.gate_code || "gate").replace(/_/g, " "),
        safe_summary: gate.safe_summary || "",
        filter_keys: ["all", "proposal"],
        status_badges: [
          {
            label: "Proposal gate " + String(status).replace(/_/g, " "),
            tone: status === "passed" ? "eligible" : "review",
            issue_codes: [gate.gate_code || "gate"],
            blocking_issue_codes: [],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        review_gate_result_id: gate.review_gate_result_id,
        gate_code: gate.gate_code,
        status: status,
        blocks_apply_when_failed: gate.blocks_apply_when_failed === true,
        source_surface: "source_evidence_persona_proposal",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    const outcomeCards = (proposal.proposal_outcome_labels || []).map(function (label) {
      return {
        schema_version: "review_workspace_source_evidence_persona_proposal_card_v1",
        card_kind: "source_persona_proposal_outcome_review",
        title: "Source persona proposal outcome",
        display_label: String(label.outcome || "outcome").replace(/_/g, " "),
        safe_summary: label.safe_summary || "",
        filter_keys: ["all", "proposal"],
        status_badges: [
          {
            label: "Proposal outcome label",
            tone: "review",
            issue_codes: [label.outcome || "outcome"],
            blocking_issue_codes: [],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        outcome_label_id: label.outcome_label_id,
        outcome: label.outcome,
        source_surface: "source_evidence_persona_proposal",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    return candidateCards.concat(riskCards).concat(rollbackCards).concat(gateCards).concat(outcomeCards);
  }

  function attachSourceProposalPersonaDraftReviewCards(stateValue) {
    const review = stateValue.review_workspace || {};
    const cards = sourceProposalPersonaDraftReviewCards(stateValue.source_proposal_persona_draft || {});
    review.source_draft_review_cards = cards;
    const tabs = review.filter_tabs || [];
    let found = false;
    tabs.forEach(function (tab) {
      if (tab.key === "draft") {
        tab.label = "Draft";
        tab.count = cards.length;
        found = true;
      }
    });
    if (!found) {
      tabs.push({ key: "draft", label: "Draft", count: cards.length });
    }
    review.filter_tabs = tabs;
    stateValue.review_workspace = review;
  }

  function sourceProposalPersonaDraftReviewCards(draft) {
    const changeCards = (draft.draft_field_changes || []).map(function (change) {
      return {
        schema_version: "review_workspace_source_proposal_persona_draft_card_v1",
        card_kind: "source_persona_draft_field_change_review",
        title: "Source persona draft field",
        display_label: String(change.persona_field_path || "draft").replace(/_/g, " "),
        safe_summary: change.after_summary || "",
        filter_keys: ["all", "draft", "persona"],
        status_badges: [
          {
            label: "Draft field needs review",
            tone: "review",
            issue_codes: change.conflict_note_ids || [],
            blocking_issue_codes: change.conflict_note_ids || [],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        draft_change_id: change.draft_change_id,
        persona_field_path: change.persona_field_path,
        before_summary: change.before_summary,
        after_summary: change.after_summary,
        source_proposal_ids: change.source_proposal_ids || [],
        source_trait_hypothesis_ids: change.source_trait_hypothesis_ids || [],
        supporting_evidence_row_ids: change.supporting_evidence_row_ids || [],
        confidence_band: change.confidence_band,
        risk_label_ids: change.risk_label_ids || [],
        conflict_note_ids: change.conflict_note_ids || [],
        rollback_ref_ids: change.rollback_ref_ids || [],
        review_gate_result_ids: change.review_gate_result_ids || [],
        draft_status: change.draft_status || "preview_only",
        source_surface: "source_proposal_persona_draft",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    const unchangedCards = (draft.unchanged_field_summaries || []).map(function (field) {
      return {
        schema_version: "review_workspace_source_proposal_persona_draft_card_v1",
        card_kind: "source_persona_draft_unchanged_field_review",
        title: "Source persona draft unchanged field",
        display_label: String(field.field_path || "unchanged").replace(/_/g, " "),
        safe_summary: field.safe_summary || "",
        filter_keys: ["all", "draft", "persona"],
        status_badges: [
          {
            label: "Draft field unchanged",
            tone: "info",
            issue_codes: [],
            blocking_issue_codes: [],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        field_path: field.field_path,
        reason: field.reason,
        source_surface: "source_proposal_persona_draft",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    const conflictCards = (draft.conflict_notes || []).map(function (note) {
      const severity = note.severity || "medium";
      return {
        schema_version: "review_workspace_source_proposal_persona_draft_card_v1",
        card_kind: "source_persona_draft_conflict_review",
        title: "Source persona draft conflict",
        display_label: String(note.conflict_code || "conflict").replace(/_/g, " "),
        safe_summary: note.safe_summary || "",
        filter_keys: ["all", "draft", "blocked"],
        status_badges: [
          {
            label: "Draft conflict blocks auto apply",
            tone: severity === "high" ? "blocked" : "review",
            issue_codes: [note.conflict_code || "conflict"],
            blocking_issue_codes: [note.conflict_code || "conflict"],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        conflict_note_id: note.conflict_note_id,
        conflict_code: note.conflict_code,
        severity: severity,
        blocks_auto_apply: note.blocks_auto_apply === true,
        source_surface: "source_proposal_persona_draft",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    const rollbackCards = (draft.rollback_refs || []).map(function (ref) {
      return {
        schema_version: "review_workspace_source_proposal_persona_draft_card_v1",
        card_kind: "source_persona_draft_rollback_review",
        title: "Source persona draft rollback",
        display_label: String(ref.rollback_ref_id || "rollback").replace(/_/g, " "),
        safe_summary: ref.safe_summary || "",
        filter_keys: ["all", "draft"],
        status_badges: [
          {
            label: "Draft rollback preview",
            tone: "review",
            issue_codes: [],
            blocking_issue_codes: [],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        rollback_ref_id: ref.rollback_ref_id,
        restore_summary: ref.restore_summary,
        runtime_rollback_ready: false,
        source_surface: "source_proposal_persona_draft",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    const gateCards = (draft.review_gate_results || []).map(function (gate) {
      const status = gate.status || "needs_review";
      return {
        schema_version: "review_workspace_source_proposal_persona_draft_card_v1",
        card_kind: "source_persona_draft_gate_review",
        title: "Source persona draft review gate",
        display_label: String(gate.gate_code || "gate").replace(/_/g, " "),
        safe_summary: gate.safe_summary || "",
        filter_keys: ["all", "draft"],
        status_badges: [
          {
            label: "Draft gate " + String(status).replace(/_/g, " "),
            tone: status === "passed" ? "eligible" : "review",
            issue_codes: [gate.gate_code || "gate"],
            blocking_issue_codes: [],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        review_gate_result_id: gate.review_gate_result_id,
        gate_code: gate.gate_code,
        status: status,
        blocks_apply_when_failed: gate.blocks_apply_when_failed === true,
        source_surface: "source_proposal_persona_draft",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    const outcomeCards = (draft.draft_outcome_labels || []).map(function (label) {
      return {
        schema_version: "review_workspace_source_proposal_persona_draft_card_v1",
        card_kind: "source_persona_draft_outcome_review",
        title: "Source persona draft outcome",
        display_label: String(label.outcome || "outcome").replace(/_/g, " "),
        safe_summary: label.safe_summary || "",
        filter_keys: ["all", "draft"],
        status_badges: [
          {
            label: "Draft outcome label",
            tone: "review",
            issue_codes: [label.outcome || "outcome"],
            blocking_issue_codes: [],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        outcome_label_id: label.outcome_label_id,
        outcome: label.outcome,
        source_surface: "source_proposal_persona_draft",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false
      };
    });
    return changeCards.concat(unchangedCards).concat(conflictCards).concat(rollbackCards).concat(gateCards).concat(outcomeCards);
  }

  function attachSourceDraftApplyReadinessReviewCards(stateValue) {
    const review = stateValue.review_workspace || {};
    const cards = sourceDraftApplyReadinessReviewCards(stateValue.source_draft_apply_readiness || {});
    review.source_readiness_review_cards = cards;
    const tabs = review.filter_tabs || [];
    let found = false;
    tabs.forEach(function (tab) {
      if (tab.key === "readiness") {
        tab.label = "Readiness";
        tab.count = cards.length;
        found = true;
      }
    });
    if (!found) {
      tabs.push({ key: "readiness", label: "Readiness", count: cards.length });
    }
    review.filter_tabs = tabs;
    stateValue.review_workspace = review;
  }

  function sourceDraftApplyReadinessReviewCards(readiness) {
    function baseCard(cardKind, title, displayLabel, safeSummary, filterKeys, statusLabel, tone, issueCodes, blockingIssueCodes) {
      return {
        schema_version: "review_workspace_source_draft_apply_readiness_card_v1",
        card_kind: cardKind,
        title: title,
        display_label: displayLabel,
        safe_summary: safeSummary,
        filter_keys: filterKeys,
        status_badges: [
          {
            label: statusLabel,
            tone: tone,
            issue_codes: issueCodes || [],
            blocking_issue_codes: blockingIssueCodes || [],
            review_required: true,
            preview_only: true,
            changes_state: false,
            runtime_ready: false
          }
        ],
        source_surface: "source_draft_apply_readiness",
        review_required: true,
        preview_only: true,
        changes_state: false,
        mutation_allowed: false,
        automatic_apply: false,
        sends_messages: false,
        runtime_ready: false,
        uses_model_provider: false,
        reads_private_sources: false,
        retains_raw_source_content: false,
        creates_embeddings: false,
        performs_extraction: false,
        writes_persona_store: false,
        writes_persona_version_store: false,
        writes_memory_store: false,
        writes_review_store: false,
        writes_runtime_store: false,
        uses_platform_adapter: false,
        uses_media_runtime: false,
        apply_executor_enabled: false
      };
    }
    function outcomeTone(outcome) {
      if (outcome === "blocked") {
        return "blocked";
      }
      if (outcome === "ready_for_future_apply_design") {
        return "eligible";
      }
      return "review";
    }

    const recordCards = (readiness.field_readiness_records || []).map(function (record) {
      const outcome = record.readiness_outcome || "needs_manual_review";
      const card = baseCard(
        "source_readiness_field_record_review",
        "Source draft readiness field",
        String(record.persona_field_path || "readiness").replace(/_/g, " "),
        record.safe_summary || "",
        ["all", "readiness", "persona"],
        "Readiness " + String(outcome).replace(/_/g, " "),
        outcomeTone(outcome),
        record.required_review_gate_result_ids || [],
        record.blocking_condition_ids || []
      );
      card.readiness_record_id = record.readiness_record_id;
      card.draft_change_id = record.draft_change_id;
      card.persona_field_path = record.persona_field_path;
      card.readiness_outcome = outcome;
      card.blocking_condition_ids = record.blocking_condition_ids || [];
      card.required_review_gate_result_ids = record.required_review_gate_result_ids || [];
      card.rollback_ref_ids = record.rollback_ref_ids || [];
      card.future_apply_design_notes = record.future_apply_design_notes || "";
      return card;
    });
    const conditionCards = (readiness.blocked_condition_records || []).map(function (condition) {
      const severity = condition.severity || "medium";
      const card = baseCard(
        "source_readiness_blocked_condition_review",
        "Source draft readiness condition",
        String(condition.condition_code || "condition").replace(/_/g, " "),
        condition.safe_summary || "",
        ["all", "readiness", "blocked"],
        "Readiness condition blocks apply",
        severity === "high" ? "blocked" : "review",
        [condition.condition_code || "condition"],
        [condition.condition_code || "condition"]
      );
      card.blocked_condition_id = condition.blocked_condition_id;
      card.condition_code = condition.condition_code;
      card.severity = severity;
      card.affected_draft_change_ids = condition.affected_draft_change_ids || [];
      card.blocks_apply = condition.blocks_apply === true;
      return card;
    });
    const gateCards = (readiness.required_review_gate_refs || []).map(function (gate) {
      const status = gate.status || "needs_review";
      const card = baseCard(
        "source_readiness_gate_ref_review",
        "Source draft readiness gate",
        String(gate.gate_code || "gate").replace(/_/g, " "),
        gate.safe_summary || "",
        ["all", "readiness"],
        "Readiness gate " + String(status).replace(/_/g, " "),
        status === "passed" ? "eligible" : "review",
        [gate.gate_code || "gate"],
        []
      );
      card.review_gate_result_id = gate.review_gate_result_id;
      card.gate_code = gate.gate_code;
      card.status = status;
      card.required_before_apply = gate.required_before_apply === true;
      return card;
    });
    const rollbackCards = (readiness.rollback_dependency_refs || []).map(function (rollback) {
      const card = baseCard(
        "source_readiness_rollback_dependency_review",
        "Source draft readiness rollback",
        String(rollback.rollback_ref_id || "rollback").replace(/_/g, " "),
        rollback.restore_summary || "",
        ["all", "readiness"],
        "Readiness rollback dependency",
        "review",
        [],
        []
      );
      card.rollback_ref_id = rollback.rollback_ref_id;
      card.dependent_draft_change_ids = rollback.dependent_draft_change_ids || [];
      card.restore_summary = rollback.restore_summary || "";
      card.runtime_rollback_ready = false;
      return card;
    });
    const outcomeCards = (readiness.readiness_outcome_labels || []).map(function (label) {
      const outcome = label.outcome || "outcome";
      const card = baseCard(
        "source_readiness_outcome_review",
        "Source draft readiness outcome",
        String(outcome).replace(/_/g, " "),
        label.safe_summary || "",
        ["all", "readiness"],
        "Readiness outcome label",
        outcomeTone(outcome),
        [outcome],
        outcome === "blocked" ? [outcome] : []
      );
      card.outcome_label_id = label.outcome_label_id;
      card.outcome = outcome;
      return card;
    });
    return recordCards.concat(conditionCards).concat(gateCards).concat(rollbackCards).concat(outcomeCards);
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
      .concat(review.session_candidate_cards || [])
      .concat(review.workbench_review_cards || [])
      .concat(review.evolution_review_cards || [])
      .concat(review.version_review_cards || [])
      .concat(review.source_intake_review_cards || [])
      .concat(review.source_evidence_review_cards || [])
      .concat(review.source_proposal_review_cards || [])
      .concat(review.source_draft_review_cards || [])
      .concat(review.source_readiness_review_cards || []);
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
      + (card.card_kind === "session_candidate_review" ? " session-candidate-review-card" : "")
      + (card.source_surface === "persona_distillation_workbench" ? " persona-workbench-review-card" : "")
      + (card.source_surface === "persona_evolution_preview" ? " persona-evolution-review-card" : "")
      + (card.source_surface === "persona_version_draft_ledger" ? " persona-version-review-card" : "")
      + (card.source_surface === "persona_source_intake_manifest" ? " persona-source-review-card" : "")
      + (card.source_surface === "persona_source_evidence_matrix" ? " persona-source-evidence-review-card" : "")
      + (card.source_surface === "source_evidence_persona_proposal" ? " source-proposal-review-card" : "")
      + (card.source_surface === "source_proposal_persona_draft" ? " source-draft-review-card" : "")
      + (card.source_surface === "source_draft_apply_readiness" ? " source-readiness-review-card" : "");

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
    appendPersonaWorkbenchReviewDetails(cardNode, card);
    appendPersonaEvolutionReviewDetails(cardNode, card);
    appendPersonaVersionDraftReviewDetails(cardNode, card);
    appendPersonaSourceIntakeReviewDetails(cardNode, card);
    appendPersonaSourceEvidenceReviewDetails(cardNode, card);
    appendSourceEvidencePersonaProposalReviewDetails(cardNode, card);
    appendSourceProposalPersonaDraftReviewDetails(cardNode, card);
    appendSourceDraftApplyReadinessReviewDetails(cardNode, card);
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

  function appendPersonaWorkbenchReviewDetails(cardNode, card) {
    if (card.source_surface !== "persona_distillation_workbench") {
      return;
    }
    if (card.card_kind === "persona_workbench_trait_review") {
      appendReviewMeta(cardNode, "Category: " + friendlyLabel(card.trait_category));
      appendReviewMeta(cardNode, "Candidate value: " + (card.candidate_value || ""));
      appendReviewMeta(cardNode, "Confidence: " + friendlyLabel(card.confidence_band));
      appendReviewDetailList(cardNode, "Evidence refs", card.evidence_ref_ids, function (value) {
        return value;
      });
    }
    if (card.card_kind === "persona_workbench_blocked_request") {
      appendReviewMeta(cardNode, "Blocked type: " + friendlyLabel(card.request_type));
      appendReviewMeta(cardNode, "Blocked status: " + friendlyLabel(card.blocked_status));
      appendReviewMeta(cardNode, "Risk: " + (card.risk_reason || ""));
      appendReviewMeta(cardNode, card.user_facing_explanation || "");
    }
    appendReviewMeta(cardNode, "Source: persona distillation workbench");
    appendReviewMeta(cardNode, "Mutation allowed: " + String(card.mutation_allowed === true));
    appendReviewMeta(cardNode, "Automatic apply: " + String(card.automatic_apply === true));
    appendReviewMeta(cardNode, "Sends messages: " + String(card.sends_messages === true));
  }

  function appendPersonaEvolutionReviewDetails(cardNode, card) {
    if (card.source_surface !== "persona_evolution_preview") {
      return;
    }
    if (card.card_kind === "persona_evolution_patch_review") {
      appendReviewMeta(cardNode, "Changed field: " + (card.changed_field_path || ""));
      appendReviewMeta(cardNode, "Before: " + (card.before_summary || ""));
      appendReviewMeta(cardNode, "After: " + (card.after_summary || ""));
      appendReviewMeta(cardNode, "Confidence: " + friendlyLabel(card.confidence_band));
      appendReviewDetailList(cardNode, "Source traits", card.source_trait_candidate_ids, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "Evidence refs", card.evidence_ref_ids, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "Risk labels", card.risk_label_ids, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "Rollback refs", card.rollback_note_ids, function (value) {
        return value;
      });
    }
    if (card.card_kind === "persona_evolution_risk_review") {
      appendReviewMeta(cardNode, "Risk code: " + friendlyLabel(card.risk_code));
      appendReviewMeta(cardNode, "Severity: " + friendlyLabel(card.severity));
      appendReviewMeta(cardNode, "Mitigation: " + (card.mitigation_summary || ""));
      appendReviewMeta(cardNode, "Blocks auto apply: " + String(card.blocks_auto_apply === true));
    }
    if (card.card_kind === "persona_evolution_rollback_review") {
      appendReviewMeta(cardNode, "Prior: " + (card.prior_summary || ""));
      appendReviewMeta(cardNode, "Rollback: " + (card.rollback_summary || ""));
      appendReviewMeta(cardNode, "Reviewer: " + (card.required_reviewer_action || ""));
      appendReviewMeta(cardNode, "Runtime rollback ready: " + String(card.runtime_rollback_ready === true));
      appendReviewDetailList(cardNode, "Target patches", card.target_patch_ids, function (value) {
        return value;
      });
    }
    if (card.card_kind === "persona_evolution_blocked_source_exclusion") {
      appendReviewMeta(cardNode, "Blocked request: " + (card.blocked_request_id || ""));
      appendReviewMeta(cardNode, "Blocked type: " + friendlyLabel(card.request_type));
      appendReviewMeta(cardNode, "Exclusion: " + (card.exclusion_reason || ""));
      appendReviewMeta(cardNode, "Excluded from patch generation: " + String(card.excluded_from_patch_generation === true));
    }
    appendReviewMeta(cardNode, "Source: persona evolution preview");
    appendReviewMeta(cardNode, "Mutation allowed: " + String(card.mutation_allowed === true));
    appendReviewMeta(cardNode, "Automatic apply: " + String(card.automatic_apply === true));
    appendReviewMeta(cardNode, "Sends messages: " + String(card.sends_messages === true));
  }

  function appendPersonaVersionDraftReviewDetails(cardNode, card) {
    if (card.source_surface !== "persona_version_draft_ledger") {
      return;
    }
    if (card.card_kind === "persona_version_draft_review") {
      appendReviewMeta(cardNode, "Outcome: " + friendlyLabel(card.reviewer_outcome));
      appendReviewMeta(cardNode, "Before: " + (card.before_snapshot_summary || ""));
      appendReviewMeta(cardNode, "After: " + (card.after_version_summary || ""));
      appendReviewDetailList(cardNode, "Included patches", card.source_patch_ids, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "Excluded patches", card.excluded_patch_ids, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "Conflicts", card.conflict_note_ids, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "Rollback refs", card.rollback_ref_ids, function (value) {
        return value;
      });
      if (card.rejection_reason) {
        appendReviewMeta(cardNode, "Reason: " + card.rejection_reason);
      }
    }
    if (card.card_kind === "persona_version_conflict_review") {
      appendReviewMeta(cardNode, "Conflict code: " + friendlyLabel(card.conflict_code));
      appendReviewMeta(cardNode, "Severity: " + friendlyLabel(card.severity));
      appendReviewMeta(cardNode, "Mitigation: " + (card.mitigation_summary || ""));
      appendReviewMeta(cardNode, "Blocks auto apply: " + String(card.blocks_auto_apply === true));
      appendReviewDetailList(cardNode, "Related patches", card.related_patch_ids, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "Related risks", card.related_risk_label_ids, function (value) {
        return value;
      });
    }
    if (card.card_kind === "persona_version_rollback_review") {
      appendReviewMeta(cardNode, "Prior: " + (card.prior_summary || ""));
      appendReviewMeta(cardNode, "Restore: " + (card.restore_summary || ""));
      appendReviewMeta(cardNode, "Runtime rollback ready: " + String(card.runtime_rollback_ready === true));
      appendReviewDetailList(cardNode, "Related drafts", card.related_draft_ids, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "Related patches", card.related_patch_ids, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "M37 rollback notes", card.related_m37_rollback_note_ids, function (value) {
        return value;
      });
    }
    if (card.card_kind === "persona_version_outcome_review") {
      appendReviewMeta(cardNode, "Label: " + (card.label || ""));
      appendReviewMeta(cardNode, "Outcome: " + friendlyLabel(card.outcome));
    }
    appendReviewMeta(cardNode, "Source: persona version draft ledger");
    appendReviewMeta(cardNode, "Mutation allowed: " + String(card.mutation_allowed === true));
    appendReviewMeta(cardNode, "Automatic apply: " + String(card.automatic_apply === true));
    appendReviewMeta(cardNode, "Sends messages: " + String(card.sends_messages === true));
  }

  function appendPersonaSourceIntakeReviewDetails(cardNode, card) {
    if (card.source_surface !== "persona_source_intake_manifest") {
      return;
    }
    if (card.card_kind === "persona_source_candidate_review") {
      appendReviewMeta(cardNode, "Source kind: " + friendlyLabel(card.source_kind));
      appendReviewMeta(cardNode, "Owner: " + friendlyLabel(card.declared_owner));
      appendReviewMeta(cardNode, "Consent: " + friendlyLabel(card.consent_status));
      appendReviewMeta(cardNode, "Minimization: " + friendlyLabel(card.minimization_status));
      appendReviewMeta(cardNode, "Redaction: " + friendlyLabel(card.redaction_profile_id));
      appendReviewMeta(cardNode, "Extraction eligible: " + String(card.extraction_eligible === true));
      appendReviewDetailList(cardNode, "Blocked reasons", card.blocked_reason_ids, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "Review gates", card.review_gate_ids, function (value) {
        return value;
      });
    }
    if (card.card_kind === "persona_source_policy_gate_review") {
      appendReviewMeta(cardNode, "Gate code: " + friendlyLabel(card.gate_code));
      appendReviewMeta(cardNode, "Enabled: " + String(card.enabled === true));
      appendReviewMeta(cardNode, "Blocks extraction: " + String(card.blocks_extraction_when_failed === true));
    }
    if (card.card_kind === "persona_source_blocked_category_review") {
      appendReviewMeta(cardNode, "Blocked code: " + friendlyLabel(card.blocked_code));
      appendReviewMeta(cardNode, "Severity: " + friendlyLabel(card.severity));
      appendReviewMeta(cardNode, "Blocks extraction: " + String(card.blocks_extraction === true));
    }
    if (card.card_kind === "persona_source_redaction_profile_review") {
      appendReviewMeta(cardNode, "Profile: " + (card.profile_label || ""));
      appendReviewMeta(cardNode, "Redaction status: " + friendlyLabel(card.redaction_status));
      appendReviewMeta(cardNode, "Raw retained: " + String(card.retains_raw_content === true));
      appendReviewMeta(cardNode, "Review: " + String(card.requires_review === true));
    }
    appendReviewMeta(cardNode, "Source: persona source intake manifest");
    appendReviewMeta(cardNode, "Mutation allowed: " + String(card.mutation_allowed === true));
    appendReviewMeta(cardNode, "Automatic apply: " + String(card.automatic_apply === true));
    appendReviewMeta(cardNode, "Sends messages: " + String(card.sends_messages === true));
  }

  function appendPersonaSourceEvidenceReviewDetails(cardNode, card) {
    if (card.source_surface !== "persona_source_evidence_matrix") {
      return;
    }
    if (card.card_kind === "persona_source_evidence_exclusion_review") {
      appendReviewMeta(cardNode, "Source: " + (card.source_id || ""));
      appendReviewMeta(cardNode, "Source kind: " + friendlyLabel(card.source_kind));
      appendReviewMeta(cardNode, "Excluded: " + String(card.excluded_from_evidence === true));
      appendReviewMeta(cardNode, "Raw retained: " + String(card.raw_content_retained === true));
      appendReviewDetailList(cardNode, "Blocked reasons", card.blocked_reason_ids, function (value) {
        return value;
      });
    }
    if (card.card_kind === "persona_source_evidence_row_review") {
      appendReviewMeta(cardNode, "Evidence: " + (card.evidence_row_id || ""));
      appendReviewMeta(cardNode, "Source: " + (card.source_id || ""));
      appendReviewMeta(cardNode, "Evidence kind: " + friendlyLabel(card.evidence_kind));
      appendReviewMeta(cardNode, "Quality: " + friendlyLabel(card.quality_label_id));
      appendReviewMeta(cardNode, "Raw retained: " + String(card.raw_content_retained === true));
      appendReviewDetailList(cardNode, "Traits", card.supports_trait_paths, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "Uncertainty", card.uncertainty_notes, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "Gates", card.review_gate_result_ids, function (value) {
        return value;
      });
    }
    if (card.card_kind === "persona_source_trait_hypothesis_review") {
      appendReviewMeta(cardNode, "Trait: " + (card.trait_path || ""));
      appendReviewMeta(cardNode, "Confidence: " + friendlyLabel(card.confidence_band));
      appendReviewMeta(cardNode, "Apply status: " + friendlyLabel(card.apply_status));
      appendReviewMeta(cardNode, "Mutation allowed: " + String(card.mutation_allowed === true));
      appendReviewDetailList(cardNode, "Supporting evidence", card.supporting_evidence_row_ids, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "Conflicting evidence", card.conflicting_evidence_row_ids, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "Gates", card.review_gate_result_ids, function (value) {
        return value;
      });
      if (card.uncertainty_summary) {
        appendReviewMeta(cardNode, "Uncertainty: " + card.uncertainty_summary);
      }
    }
    if (card.card_kind === "persona_source_quality_label_review") {
      appendReviewMeta(cardNode, "Quality code: " + friendlyLabel(card.quality_code));
      appendReviewMeta(cardNode, "Severity: " + friendlyLabel(card.severity));
      appendReviewMeta(cardNode, "Blocks unreviewed extraction: " + String(card.blocks_unreviewed_extraction === true));
    }
    if (card.card_kind === "persona_source_review_gate_result_review") {
      appendReviewMeta(cardNode, "Gate code: " + friendlyLabel(card.gate_code));
      appendReviewMeta(cardNode, "Status: " + friendlyLabel(card.status));
      appendReviewMeta(cardNode, "Blocks extraction: " + String(card.blocks_extraction_when_failed === true));
    }
    appendReviewMeta(cardNode, "Source: persona source evidence matrix");
    appendReviewMeta(cardNode, "Automatic apply: " + String(card.automatic_apply === true));
    appendReviewMeta(cardNode, "Sends messages: " + String(card.sends_messages === true));
  }

  function appendSourceEvidencePersonaProposalReviewDetails(cardNode, card) {
    if (card.source_surface !== "source_evidence_persona_proposal") {
      return;
    }
    if (card.card_kind === "source_persona_proposal_candidate_review") {
      appendReviewMeta(cardNode, "Proposal: " + (card.proposal_id || ""));
      appendReviewMeta(cardNode, "Field: " + (card.persona_field_path || ""));
      appendReviewMeta(cardNode, "Rationale: " + (card.rationale_summary || ""));
      appendReviewMeta(cardNode, "Confidence: " + friendlyLabel(card.confidence_band));
      appendReviewMeta(cardNode, "Status: " + friendlyLabel(card.proposal_status));
      appendReviewMeta(cardNode, "Mutation allowed: " + String(card.mutation_allowed === true));
      appendReviewDetailList(cardNode, "Source traits", card.source_trait_hypothesis_ids, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "Evidence rows", card.supporting_evidence_row_ids, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "Risk labels", card.risk_label_ids, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "Rollback notes", card.rollback_note_ids, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "Review gates", card.review_gate_result_ids, function (value) {
        return value;
      });
    }
    if (card.card_kind === "source_persona_proposal_risk_review") {
      appendReviewMeta(cardNode, "Risk code: " + friendlyLabel(card.risk_code));
      appendReviewMeta(cardNode, "Severity: " + friendlyLabel(card.severity));
      appendReviewMeta(cardNode, "Blocks auto apply: " + String(card.blocks_auto_apply === true));
    }
    if (card.card_kind === "source_persona_proposal_rollback_review") {
      appendReviewMeta(cardNode, "Rollback: " + (card.rollback_note_id || ""));
      appendReviewMeta(cardNode, "Restore: " + (card.restore_summary || ""));
      appendReviewMeta(cardNode, "Runtime rollback ready: " + String(card.runtime_rollback_ready === true));
    }
    if (card.card_kind === "source_persona_proposal_gate_review") {
      appendReviewMeta(cardNode, "Gate code: " + friendlyLabel(card.gate_code));
      appendReviewMeta(cardNode, "Status: " + friendlyLabel(card.status));
      appendReviewMeta(cardNode, "Blocks apply when failed: " + String(card.blocks_apply_when_failed === true));
    }
    if (card.card_kind === "source_persona_proposal_outcome_review") {
      appendReviewMeta(cardNode, "Outcome: " + friendlyLabel(card.outcome));
    }
    appendReviewMeta(cardNode, "Source: source evidence persona proposal");
    appendReviewMeta(cardNode, "Automatic apply: " + String(card.automatic_apply === true));
    appendReviewMeta(cardNode, "Sends messages: " + String(card.sends_messages === true));
  }

  function appendSourceProposalPersonaDraftReviewDetails(cardNode, card) {
    if (card.source_surface !== "source_proposal_persona_draft") {
      return;
    }
    if (card.card_kind === "source_persona_draft_field_change_review") {
      appendReviewMeta(cardNode, "Draft change: " + (card.draft_change_id || ""));
      appendReviewMeta(cardNode, "Field: " + (card.persona_field_path || ""));
      appendReviewMeta(cardNode, "Before: " + (card.before_summary || ""));
      appendReviewMeta(cardNode, "After: " + (card.after_summary || ""));
      appendReviewMeta(cardNode, "Confidence: " + friendlyLabel(card.confidence_band));
      appendReviewMeta(cardNode, "Status: " + friendlyLabel(card.draft_status));
      appendReviewMeta(cardNode, "Mutation allowed: " + String(card.mutation_allowed === true));
      appendReviewDetailList(cardNode, "Source proposals", card.source_proposal_ids, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "Source traits", card.source_trait_hypothesis_ids, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "Evidence rows", card.supporting_evidence_row_ids, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "Risk labels", card.risk_label_ids, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "Conflicts", card.conflict_note_ids, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "Rollback refs", card.rollback_ref_ids, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "Review gates", card.review_gate_result_ids, function (value) {
        return value;
      });
    }
    if (card.card_kind === "source_persona_draft_unchanged_field_review") {
      appendReviewMeta(cardNode, "Unchanged field: " + (card.field_path || ""));
      appendReviewMeta(cardNode, "Reason: " + (card.reason || ""));
    }
    if (card.card_kind === "source_persona_draft_conflict_review") {
      appendReviewMeta(cardNode, "Conflict code: " + friendlyLabel(card.conflict_code));
      appendReviewMeta(cardNode, "Severity: " + friendlyLabel(card.severity));
      appendReviewMeta(cardNode, "Blocks auto apply: " + String(card.blocks_auto_apply === true));
    }
    if (card.card_kind === "source_persona_draft_rollback_review") {
      appendReviewMeta(cardNode, "Rollback: " + (card.rollback_ref_id || ""));
      appendReviewMeta(cardNode, "Restore: " + (card.restore_summary || ""));
      appendReviewMeta(cardNode, "Runtime rollback ready: " + String(card.runtime_rollback_ready === true));
    }
    if (card.card_kind === "source_persona_draft_gate_review") {
      appendReviewMeta(cardNode, "Gate code: " + friendlyLabel(card.gate_code));
      appendReviewMeta(cardNode, "Status: " + friendlyLabel(card.status));
      appendReviewMeta(cardNode, "Blocks apply when failed: " + String(card.blocks_apply_when_failed === true));
    }
    if (card.card_kind === "source_persona_draft_outcome_review") {
      appendReviewMeta(cardNode, "Outcome: " + friendlyLabel(card.outcome));
    }
    appendReviewMeta(cardNode, "Source: source proposal persona draft");
    appendReviewMeta(cardNode, "Automatic apply: " + String(card.automatic_apply === true));
    appendReviewMeta(cardNode, "Sends messages: " + String(card.sends_messages === true));
  }

  function appendSourceDraftApplyReadinessReviewDetails(cardNode, card) {
    if (card.source_surface !== "source_draft_apply_readiness") {
      return;
    }
    if (card.card_kind === "source_readiness_field_record_review") {
      appendReviewMeta(cardNode, "Readiness record: " + (card.readiness_record_id || ""));
      appendReviewMeta(cardNode, "Draft change: " + (card.draft_change_id || ""));
      appendReviewMeta(cardNode, "Field: " + (card.persona_field_path || ""));
      appendReviewMeta(cardNode, "Outcome: " + friendlyLabel(card.readiness_outcome));
      appendReviewMeta(cardNode, "Future apply note: " + (card.future_apply_design_notes || ""));
      appendReviewDetailList(cardNode, "Blocking conditions", card.blocking_condition_ids, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "Required gates", card.required_review_gate_result_ids, function (value) {
        return value;
      });
      appendReviewDetailList(cardNode, "Rollback refs", card.rollback_ref_ids, function (value) {
        return value;
      });
    }
    if (card.card_kind === "source_readiness_blocked_condition_review") {
      appendReviewMeta(cardNode, "Condition: " + (card.blocked_condition_id || ""));
      appendReviewMeta(cardNode, "Code: " + friendlyLabel(card.condition_code));
      appendReviewMeta(cardNode, "Severity: " + friendlyLabel(card.severity));
      appendReviewMeta(cardNode, "Blocks apply: " + String(card.blocks_apply === true));
      appendReviewDetailList(cardNode, "Affected changes", card.affected_draft_change_ids, function (value) {
        return value;
      });
    }
    if (card.card_kind === "source_readiness_gate_ref_review") {
      appendReviewMeta(cardNode, "Gate: " + (card.review_gate_result_id || ""));
      appendReviewMeta(cardNode, "Code: " + friendlyLabel(card.gate_code));
      appendReviewMeta(cardNode, "Status: " + friendlyLabel(card.status));
      appendReviewMeta(cardNode, "Required before apply: " + String(card.required_before_apply === true));
    }
    if (card.card_kind === "source_readiness_rollback_dependency_review") {
      appendReviewMeta(cardNode, "Rollback: " + (card.rollback_ref_id || ""));
      appendReviewMeta(cardNode, "Restore: " + (card.restore_summary || ""));
      appendReviewMeta(cardNode, "Runtime rollback ready: " + String(card.runtime_rollback_ready === true));
      appendReviewDetailList(cardNode, "Dependent changes", card.dependent_draft_change_ids, function (value) {
        return value;
      });
    }
    if (card.card_kind === "source_readiness_outcome_review") {
      appendReviewMeta(cardNode, "Outcome id: " + (card.outcome_label_id || ""));
      appendReviewMeta(cardNode, "Outcome: " + friendlyLabel(card.outcome));
    }
    appendReviewMeta(cardNode, "Source: source draft apply-readiness");
    appendReviewMeta(cardNode, "Mutation allowed: " + String(card.mutation_allowed === true));
    appendReviewMeta(cardNode, "Automatic apply: " + String(card.automatic_apply === true));
    appendReviewMeta(cardNode, "Sends messages: " + String(card.sends_messages === true));
    appendReviewMeta(cardNode, "Runtime ready: " + String(card.runtime_ready === true));
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
