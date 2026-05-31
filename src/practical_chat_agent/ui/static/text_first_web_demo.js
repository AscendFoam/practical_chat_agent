(function () {
  const fallbackState = {
    schema_version: "text_first_web_demo_state_v1",
    user_id: "user_synthetic",
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
    }
  };

  const baseState = state();
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
      "voice-avatar-locked": "Voice / Avatar"
    };
    const panels = {
      "safe-review": "chat",
      "blocked-persona": "persona",
      "crisis-chat": "chat",
      "dependency-proactive": "proactive",
      "life-review": "life",
      "controls-review": "controls",
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

    text("#identity-strip", data.onboarding.ai_identity_disclosure_text);
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

  activateTabs();
  activateScenarios();
  setScenario("safe-review");
})();
