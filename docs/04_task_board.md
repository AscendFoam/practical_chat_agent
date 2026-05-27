# Task Board

Updated: 2026-05-27

## Captain Current State Override

- T220 review decision: `PASS`.
- T220 is complete as the schema-only outbound request boundary for M11.
- T220 review observation disposition:
  - Accepted: N01 forbidden metadata frozenset-union style is harmless cleanup debt, N02 full forbidden-key superset documentation can be clearer, N03 no payload max length is acceptable schema-only scope, N04 candidate-action id existence is not store-validated in schema-only scope, N05 approval/gate validators are correct defensive Pydantic v2 usage, N06 allowed-file note is a non-issue, N07 t220 pytest basetemp contents are workspace temp noise, M01 standalone approval/gate validator tests are minor, M02 `is_sendable()` true-path test should be added with T221 gate population, M03 outbound-specific forbidden-key tests should be expanded, M04 timestamp round-trip coverage is minor, M05 all channel values coverage is minor.
  - Deferred: none from the T220 review decision.
  - Rejected: none.
- Current Unique Task: T221 OutboundSendGate.
- Current task package: `docs/tasks/M11_outbound_sendgate_feishu/T221_outbound_send_gate.md`.
- T221 must stay gate-only and non-sending: implement deterministic policy/audit decisions over `OutboundMessageRequest`, but do not send messages, schedule actions, integrate fake/Feishu/WeChat/platform adapters, add CLI/runtime send paths, call LLMs/external services, mutate stores/private artifacts, or treat `CandidateAction` review as send authorization.
- M11 execution constraints now carried forward:
  - `CandidateAction.status="approved"`, `review_state="reviewed"`, and `is_runtime_visible()` remain evidence visibility only, not outbound authorization.
  - `OutboundMessageRequest.human_approval` is separate from `CandidateAction.review_metadata`.
  - `OutboundMessageRequest.channel_preference` is data only, not an adapter target.
  - T221 may set `send_gate.gate_state` to `allowed` or `blocked`, but that is not delivery and must not create fake/real adapter behavior.
  - T222 fake adapter, T223 Feishu adapter, T224 review card, and all WeChat adapter work remain forbidden until their own reviewed tasks.
  - M11 tests must stay synthetic and private-content-free.

- T214 review decision: `PASS`.
- T214 is complete as the behavior safety evaluation task for M10.
- M10 gate decision: `Gate M10 Allow`.
- M10 review artifact: `docs/review/M10_review.md`.
- T214 review observation disposition:
  - Accepted: N01 conflict-handling limitation is conservative scope/design, N02 repeated-review history-count repair is minor test-strength debt outside eval-only scope, N03 CLI path metadata remains accepted offline convention risk, N04 supplementary eval reading of README/02 is harmless, N05 temp/cache cleanup evidence is cosmetic, M01 missing explicit boundary-sensitive draft-enrichment scenario is minor traceability debt, M02 policy-disallowed scenario could trace code more explicitly but is non-blocking.
  - Deferred: none from the T214 review decision.
  - Rejected: none.
- Current Unique Task: T220 OutboundMessageRequest Schema.
- Current task package: `docs/tasks/M11_outbound_sendgate_feishu/T220_outbound_message_request_schema.md`.
- T220 must stay schema-only and non-sending: define a separate outbound request contract for later send-gate evaluation, but do not send messages, schedule actions, integrate platforms, add runtime loops/CLI execution, call LLMs/external services, mutate stores/private artifacts, or treat `CandidateAction` approval/runtime visibility as outbound authorization.
- M11 opening constraints now carried forward:
  - M10 authorizes review-only behavior-planner artifacts only.
  - `CandidateAction.status="approved"`, `review_state="reviewed"`, or `is_runtime_visible()` must not be interpreted as sendable, schedulable, platform-executable, or runtime authorization.
  - T220 must keep `OutboundMessageRequest` separate from `CandidateAction`.
  - T221 must implement an explicit send gate before any fake or real adapter work.
  - Feishu/WeChat/platform adapters remain forbidden until their later reviewed tasks.
  - M11 tests must stay synthetic and private-content-free.

- T213 review decision: `PASS`.
- T213 is complete as the manual CandidateAction review CLI task for M10.
- T213 review observation disposition:
  - Accepted: N01 Captain-authored T212 close-out governance diffs are established convention noise, N02 safe `input_path` / `output_path` stdout follows prior offline CLI convention, N03 T212 reviewer explanation in the working tree is prior reviewer/Captain artifact noise, N04 default in-place overwrite follows existing review-CLI convention and is low risk for offline workflow, N05 `_apply_decision` type suppression is cosmetic typing debt, M01 missing CLI freeze/archive/reject smoke tests are minor, M02 missing repeated-review history-count test is minor, M03 missing CLI reject/freeze/archive round-trip tests are minor.
  - Deferred: none.
  - Rejected: none.
- Current Unique Task: T214 Behavior Safety Eval.
- Current task package: `docs/tasks/M10_behavior_planner/T214_behavior_safety_eval.md`.
- T214 must stay evaluation-only and non-executing: inspect and report on the T210-T213 behavior-planner slice, but do not modify code/tests/schemas/CLIs/services, send messages, schedule actions, integrate platforms, call LLMs, mutate stores, read private chat history, or treat approval as outbound authorization.
- M10 execution constraints now carried forward:
  - T213 approvals make reviewed candidate artifacts visible for review workflows only; they do not authorize send, schedule, platform execution, or state mutation.
  - `CandidateAction.status="approved"`, `review_state="reviewed"`, or `is_runtime_visible()` must not be interpreted as sendable or schedulable.
  - T214 may recommend a Gate M10 status, but it must not start M11 implementation.
  - Any future outbound/platform work remains behind later OutboundSendGate milestones.
  - BehaviorPlanner work must consume only approved/review-safe context surfaces and must not reopen raw transcript ingestion.

- T212 review decision: `PASS`.
- T212 is complete as the deterministic draft-enrichment task for M10.
- T212 review observation disposition:
  - Accepted: N01 reviewer explanation allowed-files overrun is established convention noise, N02 static draft literals keyed by `BehaviorActionType` are acceptable for deterministic scope and forward-compatible `reply_follow_up_draft` / `topic_suggestion` entries are harmless, N03 unreachable fallback with `pragma: no cover` is cosmetic defensive code, N04 `model_copy(update=...)` without revalidation is acceptable because the only change is optional `draft_text` on an already validated payload, N05 overwriting existing `draft_text` is acceptable for initial-enrichment scope, M01 existing-draft overwrite mapping test gap is minor, M02 pipeline coverage for unsupported-but-available draft families is minor, M03 idempotence test gap is minor.
  - Deferred: none.
  - Rejected: none.
- Current Unique Task: T213 CandidateAction Review CLI.
- Current task package: `docs/tasks/M10_behavior_planner/T213_candidate_action_review_cli.md`.
- T213 must stay manual-review-only and non-executing: approve/reject/freeze/archive enriched `CandidateAction` records, but do not send messages, schedule actions, integrate platforms, call LLMs, mutate stores, or treat approval as outbound authorization.
- M10 execution constraints now carried forward:
  - T212 enriches draft text only; it does not execute, send, or schedule.
  - T213 may change review status and metadata, not outbound semantics.
  - `CandidateAction.status="approved"` or `is_runtime_visible()` must not be interpreted as sendable or schedulable.
  - Any future outbound/platform work remains behind later OutboundSendGate milestones.
  - BehaviorPlanner work must consume only approved/review-safe context surfaces and must not reopen raw transcript ingestion.

- T211 review decision: `PASS`.
- T211 is complete as the deterministic rule-engine task for M10.
- T211 review observation disposition:
  - Accepted: N01 reviewer explanation allowed-files overrun is established convention noise and worker summary is allowed/conventional, N02 truncated SHA-1 deterministic ids are acceptable for current offline single-user workflow, N03 overlap between boundary-trigger and proactive-blocking flags is intentional conservative behavior, N04 `contact_id=None` fallback to `user_id` is acceptable for current non-contact-targeted candidates, N05 `casefold()` normalization is acceptable with documented safe label expectations, M01 label-only memory-review prompt test gap is minor, M02 per-blocking-flag coverage gap is minor, M03 contact fallback test gap is minor, M04 multi-boundary-flag single-note test gap is minor, M05 boundary-label-only trigger test gap is minor.
  - Deferred: none.
  - Rejected: none.
- Current Unique Task: T212 Proactive Draft Generator.
- Current task package: `docs/tasks/M10_behavior_planner/T212_proactive_draft_generator.md`.
- T212 must stay deterministic, draft-only, local, and review-only: enrich `CandidateAction.payload.draft_text` for review-safe candidate actions, but do not send messages, schedule actions, integrate platforms, call LLMs, add CLI/runtime wiring, mutate stores, or bypass human review.
- M10 execution constraints now carried forward:
  - T211 emits candidate actions only; it does not approve, execute, schedule, or send.
  - T212 may add draft text, not outbound requests or platform targets.
  - `CandidateAction.status="approved"` or `is_runtime_visible()` must not be interpreted as sendable or schedulable.
  - Any future outbound/platform work remains behind later OutboundSendGate milestones.
  - BehaviorPlanner work must consume only approved/review-safe context surfaces and must not reopen raw transcript ingestion.

- T210 review decision: `PASS`.
- T210 is complete as the schema-only opening task for M10.
- T210 review observation disposition:
  - Accepted: N01 reviewer explanation allowed-files overrun is established convention noise, N02 worker-summary allowed-files overrun is established convention noise, N03/M03 explicit credential-key test gap is a low-risk test-strength note because the shared metadata validator covers the full forbidden-key set, N04 `CandidateAction.status` reuse of `DistillationStatus` is acceptable for this schema-first stage, N05 duplicated safety invariant fields on policy/action artifacts are acceptable independent-safety redundancy, M01 `max_candidates` boundary test gap is minor, M02 `AgentSelfState(contact_id=None)` round-trip gap is minor, M04 `review_notes` round-trip gap is minor.
  - Deferred: none.
  - Rejected: none.
- Current Unique Task: T211 Action Planner Rule Engine.
- Current task package: `docs/tasks/M10_behavior_planner/T211_action_planner_rule_engine.md`.
- T211 must stay deterministic, local, and candidate-only: produce review-only `CandidateAction` records from safe approved context and `AgentSelfState`, but do not send messages, schedule real actions, integrate platforms, call LLMs, mutate stores, add CLI/runtime wiring, or bypass human review.
- M10 execution constraints now carried forward:
  - T210 schemas are accepted as non-executable contracts only.
  - `CandidateAction.status="approved"` or `is_runtime_visible()` must not be interpreted as sendable or schedulable.
  - Any future outbound/platform work remains behind later OutboundSendGate milestones.
  - BehaviorPlanner work must consume only approved/review-safe context surfaces and must not reopen raw transcript ingestion.

- T203 review decision: `PASS`.
- T203 is complete as the optional Mem0 adapter spike task for M9.
- T203 warning disposition:
  - Accepted: N01 `.claude/settings.json` workspace-artifact overrun is established convention noise, N02 `docs/worker_summary/T203_worker_summary.md` worker-summary overrun is established convention noise, N03 T203 reuses the T202 eval shape rather than importing the T202 runner directly which is acceptable for a spike, N04 documentation/test-count discrepancies are harmless, N05 English keyword memory-type inference is acceptable for spike scope, M01 no `limit=0` test is acceptable for spike scope, M02 no empty-string `contact_id` test is acceptable for spike scope, M03 no direct `ImportError` simulation is acceptable because safe not-configured behavior is covered, M04 non-`Exception` propagation is correct behavior.
  - Deferred: none.
  - Rejected: none.
- M9 completion status: M9 is complete at the task level with Gate M9 `Allow`.
- Current Unique Task: T210 Behavior Schema.
- Current task package: `docs/tasks/M10_behavior_planner/T210_behavior_schema.md`.
- T210 must stay schema-only and draft-only: define proactive-behavior data contracts but do not send messages, schedule real actions, integrate platforms, mutate memory, wire runtime planners, or claim autonomous behavior.
- M10 execution constraints now carried forward:
  - Candidate actions must be review-only artifacts, not executable actions.
  - Any future send/platform work remains behind later OutboundSendGate milestones.
  - BehaviorPlanner work must consume only approved/review-safe context surfaces and must not reopen raw transcript ingestion.

- T202 review decision: `PASS`.
- T202 is complete as the retrieval eval set task for M9.
- T202 warning disposition:
  - Accepted: N01 `.claude/settings.json` workspace-artifact overrun is established convention noise, N02 `docs/worker_summary/T202_worker_summary.md` worker-summary overrun is established convention noise, N03 eval coverage on `LocalApprovedStoreRetriever` rather than context-bound `LocalMemoryRetriever` is acceptable for a reusable protocol eval baseline, M01 no dedicated empty-string query case is acceptable because T201 covers it and T202 covers adjacent query boundaries, M02 uniform excluded-record scores are acceptable because exclusion is the behavior under test.
  - Deferred: none.
  - Rejected: none.
- Current Unique Task: T203 Optional Mem0 Adapter Spike.
- Current task package: `docs/tasks/M9_memory_retrieval_layer/T203_optional_mem0_adapter_spike.md`.
- T203 must stay a contained optional adapter spike: no required Mem0 dependency, no production external-memory adoption, no provider/service calls in committed tests, no private chat content, no raw transcript indexing, no memory auto-write, no approved-store mutation, no ChatContext wiring, no ReplyPlanner/policy/send behavior changes, and no platform integration.
- M9 execution constraints now carried forward:
  - T203 should place any adapter work behind `MemoryRetriever.retrieve()` and `MemoryRetrieverResult`.
  - T203 should reuse the T202 synthetic eval shape where feasible.
  - T203 should gracefully handle missing optional dependency/configuration as `not_configured` or an explicitly documented spike limitation.

- T201 review decision: `PASS`.
- T201 is complete as the local approved-store retriever task for M9.
- T201 warning disposition:
  - Accepted: N01 `.claude/settings.json` workspace-artifact overrun is established convention noise, N02 `docs/worker_summary/T201_worker_summary.md` worker-summary overrun is established convention noise, N03 per-call store-file reads without caching are acceptable for current offline-first single-user workflow, M01 `limit=0` test is a harmless boundary guard, M02 concurrent-read tests are outside current single-user offline scope.
  - Deferred: none.
  - Rejected: none.
- Current Unique Task: T202 Retrieval Eval Set.
- Current task package: `docs/tasks/M9_memory_retrieval_layer/T202_retrieval_eval_set.md`.
- T202 must stay evaluation-only and synthetic: no private chat content, no vector DB, no Mem0/Zep, no embedding/provider calls, no raw transcript reads, no ChatContext wiring, no planner/policy/send behavior changes, and no external services.
- M9 execution constraints now carried forward:
  - T202 should exercise retrievers through `MemoryRetriever.retrieve()` and `MemoryRetrieverResult`.
  - T202 should cover relevant hits, exclusions, query behavior, deterministic ordering, and boundary behavior.
  - T202 should create reusable synthetic cases before any optional external adapter work.

- T200 review decision: `PASS`.
- T200 is complete as the contract-first MemoryRetriever opening task for M9.
- T200 warning disposition:
  - Accepted: N01 `.claude/settings.json` workspace-artifact overrun is established convention noise, N02 `docs/worker_summary/T200_worker_summary.md` worker-summary overrun is established convention noise, N03 free-form `MemoryHit.source` is acceptable because convention values are documented and future adapter extensibility is intentional, M01 guarded adapter-test assertions are minor test-strength observations covered by a direct hit-producing setup test.
  - Deferred: none.
  - Rejected: none.
- Current Unique Task: T201 Local Approved-Store Retriever.
- Current task package: `docs/tasks/M9_memory_retrieval_layer/T201_local_approved_store_retriever.md`.
- T201 must implement the T200 protocol over approved local store records only: no vector DB, no Mem0/Zep adapter, no embedding/provider calls, no raw transcript reads, no auto-write or store mutation, and no planner/policy/send behavior changes.
- M9 execution constraints now carried forward:
  - T201 should return `MemoryHit` items with `source="approved_store"`.
  - T201 should filter to approved/runtime-ready records and exclude candidate/rejected/frozen/archived/not-human-reviewed records.
  - T201 should preserve evidence refs and use simple deterministic query/limit behavior suitable for later T202 evaluation.

- T195 review decision: `PASS_WITH_WARNINGS`.
- T195 is complete as the evaluation-only closing task for M8.
- T195 warning disposition:
  - Accepted: W01 worker milestone-review/handoff mechanism claim was factually wrong and is corrected in the captain governance sync, W04 `docs/for_human/T195_review_explanation.md` allowed-files overrun is treated as established low-risk convention noise.
  - Deferred: W02 relationship dimension-change values are present in `ChatContext` but unused by `ReplyPlanner` / `ReplyPlanPolicyEngine`, W03 relationship guidance reaching summary/retrieval-note surfaces is informational only and does not create semantic consumption.
  - Rejected: none.
- M8 completion status: M8 is complete as a relationship-state infrastructure/evaluation milestone. It does not yet provide dimension-aware reply behavior; approved relationship context is currently behaviorally inert.
- Current Unique Task: T200 MemoryRetriever interface.
- Current task package: `docs/tasks/M9_memory_retrieval_layer/T200_memory_retriever_interface.md`.
- T200 must stay contract-first and local-only: no vector DB, no Mem0/Zep adapter, no auto-write, and no raw transcript retrieval.
- M9 execution constraints now carried forward:
  - T200 should define retriever boundaries before any adapter work.
  - T200 should preserve approved-only, review-safe retrieval surfaces.
  - T200 must not use T195 as justification to claim relationship-aware planner behavior already exists.

- T194 review decision: `PASS_WITH_WARNINGS`.
- T194 is complete as the compact relationship-context task for M8.
- T194 warning disposition:
  - Accepted: N01 relationship context reads individual delta JSON files rather than a store-file abstraction, N02 `.claude/settings.json` workspace-artifact overrun, S01 diagnostic notes flowing into retrieval notes are a project-wide convention, S02 `ApprovedStoreContextStatus` reuse is cross-domain coupling but acceptable here, S03 no AppContainer wiring is outside current scope.
  - Deferred: M01 summary truncation edge case not directly tested, M02 path-is-directory branch not tested, M03 empty `delta_rationale` input not directly tested.
  - Rejected: none.
- Current Unique Task: T195 Relationship-aware reply eval.
- Current task package: `docs/tasks/M8_relationship_state/T195_relationship_aware_eval.md`.
- T195 must stay evaluation-only: no code changes, no private artifacts committed, and no state application or context mutation.
- M8 execution constraints now carried forward:
  - T195 should compare reply behavior under different approved relationship contexts and record evidence only.
  - T195 must not invent new runtime semantics or reopen earlier review layers.
  - T195 is the milestone-level evaluation and does not authorize new implementation work by itself.

- T193 review decision: `PASS_WITH_WARNINGS`.
- T193 is complete as the explicit relationship-delta review task for M8.
- T193 warning disposition:
  - Accepted: N02 default input-file overwrite risk follows established review-CLI pattern, N04 `.claude/settings.json` workspace-artifact overrun.
  - Deferred: N01 no committed CLI-level integration tests, N03 no evidence pre-validation gate before approval, M01 no Typer-command test coverage, M02 no explicit empty-string note test.
  - Rejected: none.
- Current Unique Task: T194 RelationshipState compact context.
- Current task package: `docs/tasks/M8_relationship_state/T194_relationship_state_context.md`.
- T194 must stay context-only and approval-gated: no raw signal history injection, no RelationshipState auto-update, no send-behavior change, and no reopening of delta review semantics.
- M8 execution constraints now carried forward:
  - T194 should expose only compact, approved relationship-state guidance to `ChatContext`.
  - T194 should assume approved deltas may still require evidence caution; it must not silently treat review approval as a full validation substitute.
  - T194 must keep relationship-state context additive and avoid leaking raw signal or review-history detail.

- T192 review decision: `PASS_WITH_WARNINGS`.
- T192 is complete as the conservative delta-generation task for M8.
- T192 warning disposition:
  - Accepted: N01 heuristic `_MAGNITUDE_SCALE` / `_MIN_STRENGTH` defaults are acceptable for candidate-only scope, N02 max-strength aggregation is acceptable for current conservative scope, N03 `.claude/settings.json` workspace-artifact overrun, N04 `dimension_name` type-ignore suppression is cosmetic typing debt, N05 `_DIRECTION_SIGN` uses string keys but is functionally safe.
  - Deferred: M01 no committed test for unknown dimension names being skipped safely, M02 no committed test for mixed known+unknown/stable direction sets on the same dimension, M04 no committed test for empty `evidence_refs` after state-evidence-only deduplication.
  - Rejected: none.
- Current Unique Task: T193 Relationship review CLI.
- Current task package: `docs/tasks/M8_relationship_state/T193_relationship_review_cli.md`.
- T193 must stay review-only and auditable: no auto-apply to `RelationshipState`, no unrelated memory/ContactSkill mutation, no send/platform integration, and no dimension semantics rewrite.
- M8 execution constraints now carried forward:
  - T193 should review `RelationshipDeltaCandidate` records as whole candidate artifacts with explicit human decisions.
  - T193 should preserve evidence refs, signal refs, and review history.
  - T193 must keep delta review separate from actual state application; T194 is still later and context-only.

- T191 review decision: `PASS_WITH_WARNINGS`.
- T191 is complete as the conservative signal-extraction task for M8.
- T191 warning disposition:
  - Accepted: N01 handoff test-count mismatch is a documentation accuracy issue, N02 `.claude/settings.json` workspace-artifact overrun, N04 static rule-table typing suppression is acceptable for the current deterministic extractor scope, N05 sparse coverage over 3 of 8 dimensions is intentional and conservative.
  - Deferred: N03 `RelationshipSignal` missing `updated_at`, M01 no committed test for approved `RelationshipSignal` runtime-ready path, M02 no committed test for `signal_id` format.
  - Rejected: none.
- Current Unique Task: T192 RelationshipDeltaCandidate.
- Current task package: `docs/tasks/M8_relationship_state/T192_relationship_delta_candidate.md`.
- T192 must stay delta-only and reviewable: no auto-approve, no auto-apply, no send/platform integration, no scalar-collapse, and no raw-text dependency.
- M8 execution constraints now carried forward:
  - T192 should consume T191 signals and emit explicit dimension deltas with evidence refs and signal refs.
  - T192 should recompute or validate magnitude/direction semantics rather than assuming schema defaults are sufficient.
  - T192 must preserve T190/T191 review-first semantics and not claim state-update completion.

- T190 review decision: `PASS_WITH_WARNINGS`.
- T190 is complete as the schema-only opening task for M8.
- T190 warning disposition:
  - Accepted: N01 `.claude/settings.json` workspace-artifact overrun, N04 `RelationshipState.source_type` can remain extensible for a later approved-delta source.
  - Deferred: N02 `RelationshipDeltaDimension.magnitude` is not schema-enforced against `current_value` / `proposed_value`, N03 `RelationshipDeltaDirection="stable"` lacks contract guidance, M01 no committed automated schema validation tests yet exist.
  - Rejected: none.
- Current Unique Task: T191 Relationship signal extractor.
- Current task package: `docs/tasks/M8_relationship_state/T191_relationship_signal_extractor.md`.
- T191 must stay extraction-only and conservative: no raw chat-history reads, no RelationshipState auto-update, no delta generation, no review CLI, no send/platform integration, and no LLM dependency unless a later Captain task explicitly permits it.
- M8 execution constraints now carried forward:
  - T191 should emit evidence-backed relationship signals that later T192 delta generation can reference.
  - T191 should prefer under-generation over speculative inference; ambiguous cases should be skipped rather than forced into a dimension.
  - T191 must preserve T190 schema semantics and keep M8 review-first; T190 does not close M8.

- T185 review decision: `PASS_WITH_WARNINGS`.
- T185 is complete as the narrow hybrid alignment task.
- T185 warning disposition:
  - Accepted: N01 `.claude/settings.json` workspace-artifact overrun, N02 heuristic safety-context detection, N03 prompt-level language enforcement instead of a hard validator.
  - Deferred: none.
  - Rejected: none.
- Gate M7 verdict: `Allow`.
- Current Unique Task: T190 RelationshipState schema.
- Current task package: `docs/tasks/M8_relationship_state/T190_relationship_state_schema.md`.
- T190 must stay schema-only and conservative: no signal extraction, no review CLI, no auto-update, no send/platform integration, and no single-score collapse.
- M8 execution constraints now carried forward:
  - T190 should define multidimensional `RelationshipState` and `RelationshipDeltaCandidate` concepts with explicit evidence refs and timestamps.
  - T190 must preserve review-only delta modeling and avoid automatic state mutation.
  - T190 should not claim M8 completion until later review/eval tasks are revisited.

- T183 review decision: `PASS_WITH_WARNINGS`.
- T183 is complete as the opt-in hybrid planner integration M7 task.
- T183 warning disposition:
  - Accepted: N01 `.claude/settings.json` workspace-artifact overrun.
  - Deferred: N02 no committed test exercises the valid LLM-candidate merge success path, M01 no end-to-end hybrid success test, M02 no explicit reranked-order assertion after merge.
  - Rejected: none.
- Current Unique Task: T184 Planner Holdout Eval.
- Current task package: `docs/tasks/M7_llm_reply_planner/T184_llm_planner_holdout_eval.md`.
- T184 must stay evaluation-only: no planner code changes, no send/platform integration, no raw private content in committed artifacts, and no quality claim without evidence.
- M7 execution constraints now carried forward:
  - T184 may compare template vs hybrid outputs on anonymized holdout scenarios, but it must not modify planner logic or promote quality claims beyond the observed evidence.
  - T184 must preserve privacy, boundary safety, and review-only semantics.
  - T184 should clearly distinguish committed tests from private smoke evaluation and should not treat smoke-only evidence as a substitute for committed regression coverage.

- T182 review decision: `PASS_WITH_WARNINGS`.
- T182 is complete as the shared validator-hardening M7 task.
- T182 warning disposition:
  - Accepted: N02 `.claude/settings.json` workspace-artifact overrun.
  - Deferred: N01 broken `INPUT_TOO_LARGE` preflight call-site bug, M01 missing regression test for the `INPUT_TOO_LARGE` refusal path.
  - Rejected: none.
- Current Unique Task: T183 Hybrid ReplyPlanner.
- Current task package: `docs/tasks/M7_llm_reply_planner/T183_hybrid_reply_planner.md`.
- T183 must stay opt-in, additive, and review-only: no default LLM mode, no send/platform integration, no runtime mutation, and no bypass of validator or policy gating.
- M7 execution constraints now carried forward:
  - T183 may integrate template and optional LLM candidates into one review-only planner surface, but template mode must remain backward-compatible and authoritative by default.
  - T183 must preserve compact-context boundaries, deterministic validation, policy/boundary review, and private-artifact discipline.
  - T183 must not claim quality completion; holdout quality judgment remains deferred to T184.

- T181 review decision: `PASS_WITH_WARNINGS`.
- T181 is complete as the first executable M7 task.
- T181 warning disposition:
  - Accepted: N01 allowed-files overrun for `.claude/settings.json` and `docs/reference/AI_coding_workflow.md`, N02 default `policy_boundary` refs rather than LLM-provided supporting refs, N03 redundant `validate_ranks` call.
  - Deferred: N04 substring-only privacy leak detection, N05 dead `INPUT_TOO_LARGE` refusal path, M01 `_build_llm_input` output-shape coverage gap, M02 `_parse_provider_response` error-path coverage gap, M03 missing generator-to-validator pipeline test, M04 missing CLI stdout privacy regression test.
  - Rejected: none.
- Current Unique Task: T182 Candidate Validator.
- Current task package: `docs/tasks/M7_llm_reply_planner/T182_candidate_validator.md`.
- T182 must stay validator-only, additive, and private-by-default: no new candidate generation path, no hybrid planner behavior, no default LLM mode, no send/platform integration, and no runtime mutation.
- M7 execution constraints now carried forward:
  - T182 may harden deterministic validation shared across template and LLM candidates, but it must not change the compact-context input boundary established by T123/T164/T174/T181.
  - T182 may add explicit input-size refusal enforcement, privacy/impersonation hardening, and regression tests, but it must not rewrite planner strategy selection or claim quality completion.
  - T182 must preserve review-only mode, no-impersonation rules, approved-store semantics, and human-approved outbound policy.

- T180 review decision: `PASS`.
- T180 is complete as the contract-only M7 opening task.
- Current Unique Task: T181 LLM Candidate Offline CLI.
- Current task package: `docs/tasks/M7_llm_reply_planner/T181_llm_candidate_offline_cli.md`.
- T181 must stay offline, opt-in, additive, and private-artifact-only: no hybrid planner behavior, no default LLM mode, no ReplyPlanner behavior changes, no runtime mutation, and no send/platform integration.
- M7 execution constraints now carried forward:
  - T181 may consume only safe synthetic/redacted `ChatContext` JSON that already respects the T123/T164/T174 compact-context boundary.
  - T181 must emit either a validated private `LLMReplyPlan` artifact or a structured refusal; it must not bypass deterministic validation.
  - T181 must not alter `chat-reply-plan`, `ReplyPlanPolicyEngine`, approved-store semantics, or feedback/review-only gating.

- T174 review decision: `PASS`.
- T174 is complete as an additive context-integration-only M6 task.
- Gate M6 is now `Allow`.
- Current Unique Task: T180 LLM Candidate Generator Contract.
- Current task package: `docs/tasks/M7_llm_reply_planner/T180_llm_candidate_contract.md`.
- T180 must stay contract-only, additive, and non-breaking: no LLM calls, no ReplyPlanner behavior changes, no send/platform integration, no runtime mutation, and no deprecation claim.
- M6 is now complete: T170-T174 together preserve ContactSkill compatibility, evidence ownership boundaries, `ApprovedContactSkillBrief` fallback behavior, and coexistence with the separate T164 approved-patch compact-context path.
- M7 opening constraints now carried forward:
  - T180 must define an optional LLM candidate contract only; it must not invoke a model.
  - Any M7 work must preserve review-only mode, no-impersonation rules, and the existing compact-context contracts from T123/T164/T174.
  - No LLM-generated output may bypass policy/boundary review or approved-store gating.

- T173 review decision: `PASS`.
- T173 is complete as an additive projection-only M6 task.

- T172 review decision: `PASS`.
- T172 is complete as an additive schema-only M6 task.

- T171 review decision: `PASS`.
- T171 is complete as an additive schema-only M6 task.

- T170 review decision: `PASS`.
- T170 is complete as a design-only M6 compatibility task.

- T164 review decision: `PASS_WITH_WARNINGS`.
- T164 is complete as an approved patch compact context task.
- T164 warning disposition:
  - Accepted: N01 `.claude/settings.json` is a workspace artifact rather than a T164 scope violation, N02 `_compact_text` duplication is low-risk refactor debt, N03 `ApprovedPatchContext.status` reuses a slightly broader status enum than strictly necessary, N04 per-assemble `ApprovedPatchContextService()` instantiation is low-impact for the current offline workflow, N05 handoff test-count wording was inaccurate and is corrected in the governance sync, N06 carrying `supporting_cluster_ids` through compact briefs is safe because they are deterministic labels rather than raw text.
  - Deferred: M01 missing explicit frozen/archived exclusion tests, M02 missing `ChatContextAssembler` end-to-end patch-path integration test, M03 missing empty/whitespace `behavior_instruction` edge-case coverage.
  - Rejected: none.

- T163 review decision: `PASS_WITH_WARNINGS`.
- T163 is complete as a manual patch review task.
- T163 warning disposition:
  - Accepted: N05 `.claude/settings.json` is a workspace artifact rather than a T163 scope violation.
  - Deferred: N01 the contract still overclaims deterministic `patch_id` behavior, N02 no committed automated tests yet cover `PatchReviewService` / `chat-feedback-review-patch`, N03 review writes back to the input file by default and may risk in-place corruption on write failure, N04 review history can grow without bound.
  - Rejected: none.
- T162 review decision: `PASS_WITH_WARNINGS`.
- T162 is complete as a deterministic, candidate-only patch proposal task.
- T162 warning disposition:
  - Accepted: N05 `.claude/settings.json` is a workspace artifact rather than a T162 scope violation.
  - Deferred: N01 the contract still overclaims deterministic `patch_id` behavior, N02 raw `input_path` remains present in proposal stdout/output and stays tracked as project-wide path-handling/privacy debt, N03 no committed automated tests yet cover `PatchProposalService` / `chat-feedback-propose-patch`, N04 malformed cluster input with empty `contact_id` can still crash proposal generation instead of being skipped defensively.
  - Rejected: none.
- T161 review decision: `PASS_WITH_WARNINGS`.
- T161 is complete as a deterministic, privacy-safe feedback clusterer task.
- T161 warning disposition:
  - Accepted: N01 `reason_tag_summary` naming is slightly misleading but documented well enough for current scope, N03 `counts_by_approach_label` may safely degrade to empty when plan files are unavailable, N05 `.claude/settings.json` is a workspace artifact rather than a T161 scope violation.
  - Deferred: N02 no committed automated tests yet cover `FeedbackClusterService` / `chat-feedback-cluster`, N04 raw `input_path` remains present in cluster stdout/output and stays tracked as project-wide path-handling/privacy debt.
  - Rejected: none.
- T160 review decision: `PASS_WITH_WARNINGS`.
- T160 is complete as a schema-only PreferencePatch candidate contract task.
- T160 warning disposition:
  - Accepted: N01 `instruction_scope` remains free-form at schema stage, N04 `schema_version` remains a plain string for consistency with existing patterns, N05 broader working-tree modifications are a hygiene note rather than a T160 scope violation.
  - Deferred: N02 `positive_examples` / `negative_examples` are not structurally constrained to safe-only summaries or references, N03 no committed automated tests yet cover `PreferencePatchCandidate` validation.
  - Rejected: none.
- T152 review decision: `PASS_WITH_WARNINGS`.
- T152 is complete as a committed feedback CLI regression-hardening task.
- T152 warning disposition:
  - Accepted: N03 `--validation-report` CLI wiring is covered at the service level rather than by a dedicated end-to-end CLI test, N04 no single append->validate->summarize integration test yet, N05 `test_approach_labels_loaded` is intentionally brittle as a regression guard.
  - Deferred: N01 validation `record_results` can still grow unboundedly on large logs, N02 service-level output-path confinement is still by warning/convention rather than hard enforcement.
  - Rejected: none.
- Gate M3 remains `Conditional` for quality/maturity claims.
- Gate M4.5 is now `Allow`.
- M4 review-only feedback infrastructure is now reproducible from committed repo contents.
- M5 is now authorized only at the review-only patch-candidate layer: no auto-apply, no runtime injection, no automatic ContactSkill/Memory mutation, no outbound send behavior, and no LLM use unless a future task package explicitly allows it.
- T151 review decision: `PASS_WITH_WARNINGS`.
- T151 is complete as a committed policy-fixture and direct policy-engine regression-hardening task.
- T151 warning disposition:
  - Accepted: N01 `_candidate_is_over_proactive` conservative fallback branch not independently covered, N02 confidence-penalty coverage not fully additive across every combination, N03 baseline fixture contamination found and corrected by the new direct tests.
  - Deferred: none.
  - Rejected: none.
- T150 review decision: `PASS_WITH_WARNINGS`.
- T150 is complete as a committed ReplyPlanner regression-hardening task.
- T150 warning disposition:
  - Accepted: N01 overlapping `not_configured` fixture coverage, N02 no direct `ReplyPlanPolicyEngine` unit tests yet, N03 summary-text assertion fragility, N04 false-negative probe asserts current absence rather than a gap marker, N05 helper constructors not tested independently, N06 no `notes_on_candidate_differences` assertion yet.
  - Deferred: none.
  - Rejected: none.
- T140 review decision: `PASS_WITH_WARNINGS`.
- T140 is complete as a review-only feedback capture task.
- T140 warning disposition:
  - Accepted: N03 redundant recount, N04 `reply_plan_id` proxy semantics, N06 `Literal` action type.
  - Deferred: N01 corrupted-log silent reset, N02 unstable `source_plan_path`, N05 missing private-path confinement.
- T141 review decision: `PASS_WITH_WARNINGS`.
- T141 is complete as a read-only feedback log validator.
- T141 warning disposition:
  - Accepted: N01 raw `input_path` in CLI output, N03 coarse private-path heuristic, N04 CWD-dependent relative path resolution, N05 stored-but-unused `strict_mode`.
  - Deferred: N02 `reply_plan_id` coherence not cross-checked, N06 `record_results` may get large.
  - Rejected: none.
- T142 review decision: `PASS_WITH_WARNINGS`.
- T142 is complete as a privacy-safe aggregate feedback summary exporter.
- T142 warning disposition:
  - Accepted: N01 duplicated plan-loading helpers, N02 raw `input_path` in stdout, N03 aggregate presence counts expose low-risk existence patterns, N04 unreadable input can still produce an output artifact, N05 untyped summary `dict`, N06 no `reason_tag` / `policy_risk_flag` aggregation because those fields do not yet exist.
  - Deferred: none.
  - Rejected: none.
- Gate M4 was `Conditional` at milestone review time and is now satisfied through completed M4.5 regression hardening.
- M4 remains review-only: no auto-send, no realtime platform integration, no automatic ContactSkill/Memory mutation, no feedback-to-patch behavior, and no relationship-aware maturity claim before regression hardening.
- M4.5 is complete: T150/T151/T152 together provide committed deterministic coverage for ReplyPlanner, direct policy behavior, and the feedback CLI loop.
- The project may now continue beyond M5. M5 is functionally complete within review-only, non-mutating constraints, and later work must preserve its approval-gated interpretation.

## Current Unique Task

T221: OutboundSendGate.

Task package: `docs/tasks/M11_outbound_sendgate_feishu/T221_outbound_send_gate.md`

Why now: T220 has landed with `PASS`, so the repo now has a separate inert `OutboundMessageRequest` contract. The next smallest safe step is a deterministic send gate that evaluates that request and records explicit allowed/blocked audit state before any fake adapter, Feishu adapter, scheduler, runtime autonomy, or automatic send behavior.

## Board Rules

- Current mainline is WeFlow-export-driven offline distillation and review-only reply planning.
- Only the `Current Unique Task` may be assigned to a worker.
- Worker must stay within the task package `Allowed files`.
- `private/` chat history and private distilled artifacts must never be committed.
- Fixtures, tests, and docs must stay redacted.
- Do not resume T01 or restart WeChat scan / SDK / realtime platform work on the current mainline.
- Do not add fine-tuning, automatic sending, or digital-clone behavior.

## Paused Legacy Track: WeChat SDK / Scan

- [x] T00: SDK install and QR-stage probe. Review `PASS`.
- [ ] T01: login/session validation. Review `BLOCK`. User chose not to repair it; legacy track remains paused.

Conclusion: the old iLink / scan track no longer drives the next stage of development.

## Milestone 0: WeFlow Data Contract and Privacy Guardrails

Goal: confirm WeFlow JSONL is parseable and define a normalized event contract plus redacted fixture.

- [x] T100: WeFlow JSONL schema profiling + normalized event contract. Review `PASS`.
- [x] T101: privacy redaction rules + source-ref rules + minimal redacted fixture. Review `PASS`.
- [x] T102: minimal WeFlow normalize CLI. Review `PASS`.
- [x] T103: M0 review. Gate M0 `Conditional`, accepted for M1.

## Milestone 1: Offline Distillation MVP

Goal: generate chunks, memory facts, ContactSkill candidate, and review artifact from one contact or a small sample.

- [x] T110: conversation chunker v0. Review `PASS`.
- [x] T111: distillation schemas. Review `PASS`.
- [x] T112: summary + fact extraction pipeline. Review `PASS`.
- [x] T113: ContactSkill builder + markdown review exporter. Review `PASS_WITH_WARNINGS`.
- [x] T114: MVP sample run + gate review. Gate M1 `Conditional`.

## Milestone 2: Memory / Skill Store and Evidence Validation

Goal: move offline artifacts into project models, storage, and review flow.

- [x] T120: file-store models for memory/skill records. Review `PASS_WITH_WARNINGS`.
- [x] T121: evidence validator. Review `PASS_WITH_WARNINGS`.
- [x] T122: review / approve / export CLI. Review `PASS_WITH_WARNINGS`.
- [x] T123: approved/runtime-ready context integration. Review `PASS_WITH_WARNINGS`.

## Milestone 3: Relationship Reply Planner

Goal: generate interpretable, multi-candidate, safety-aware reply drafts from approved ContactSkill + memory.

- [x] T130: ReplyPlan schema + prompt contract. Review `PASS_WITH_WARNINGS`.
- [x] T131: review-only ReplyPlanner. Review `PASS_WITH_WARNINGS`.
- [x] T132: policy / boundary layer. Review `PASS_WITH_WARNINGS`.
- [x] T133: anonymized holdout eval. Review `PASS_WITH_WARNINGS`. Gate M3 `Conditional`.

## Milestone 4: Feedback Capture

Goal: record, validate, and summarize human feedback on ReplyPlan candidates without applying it automatically.

- [x] T140: feedback log schema + CLI. Review `PASS_WITH_WARNINGS`.
- [x] T141: feedback log validator. Review `PASS_WITH_WARNINGS`.
- [x] T142: feedback summary exporter. Review `PASS_WITH_WARNINGS`. Gate M4 `Conditional`.

## Milestone 4.5: Regression Hardening

Goal: turn M3/M4 behavior into committed reproducible tests before feedback-to-patch or LLM drafting work.

- [x] T150: ReplyPlanner regression tests. Review `PASS_WITH_WARNINGS`.
- [x] T151: policy fixture suite. Review `PASS_WITH_WARNINGS`.
- [x] T152: feedback CLI regression tests. Review `PASS_WITH_WARNINGS`. Gate M4.5 `Allow`.

## Milestone 5: Feedback to Patch

Goal: convert repeated feedback into reviewable PreferencePatch candidates without automatic approval or mutation.

- [x] T160: PreferencePatch schema. Review `PASS_WITH_WARNINGS`.
- [x] T161: feedback clusterer. Review `PASS_WITH_WARNINGS`.
- [x] T162: patch proposal CLI. Review `PASS_WITH_WARNINGS`.
- [x] T163: patch review CLI. Review `PASS_WITH_WARNINGS`.
- [x] T164: approved patch compact context. Review `PASS_WITH_WARNINGS`.

## Milestone 6: ContactSkill-Compatible Decomposition

Goal: keep ContactSkill compatible while deriving more focused briefs.

- [x] T170: ContactSkill decomposition design. Review `PASS`.
- [x] T171: PartnerPersonaBrief schema. Review `PASS`.
- [x] T172: CommunicationPolicyBrief + BoundaryProfileBrief schemas. Review `PASS`.
- [x] T173: ContactSkill projection service. Review `PASS`.
- [x] T174: derived briefs context integration. Review `PASS`.

## Milestone 7: LLM-Assisted ReplyPlanner

Goal: add optional LLM candidate generation only after regression safety net is in place.

- [x] T180: LLM candidate contract. Review `PASS`.
- [x] T181: LLM candidate offline CLI. Review `PASS_WITH_WARNINGS`.
- [x] T182: candidate validator. Review `PASS_WITH_WARNINGS`.
- [x] T183: hybrid ReplyPlanner. Review `PASS_WITH_WARNINGS`.
- [x] T184: planner holdout eval. Review `PASS_WITH_WARNINGS`.
- [x] T185: hybrid planner language and safety alignment. Review `PASS_WITH_WARNINGS`. Gate M7 `Allow`.

## Milestone 8: RelationshipState

Goal: model multi-axis relationship state with human-reviewed deltas rather than a single scalar affinity score.

- [x] T190: RelationshipState schema. Review `PASS_WITH_WARNINGS`.
- [x] T191: relationship signal extractor. Review `PASS_WITH_WARNINGS`.
- [x] T192: RelationshipDeltaCandidate. Review `PASS_WITH_WARNINGS`.
- [x] T193: relationship review CLI. Review `PASS_WITH_WARNINGS`.
- [x] T194: RelationshipState compact context. Review `PASS_WITH_WARNINGS`.
- [x] T195: relationship-aware reply eval. Review `PASS_WITH_WARNINGS`.

## Milestone 9: Memory Retrieval Layer

Goal: define a retriever abstraction before evaluating external memory adapters.

- [x] T200: MemoryRetriever interface.
- [x] T201: local approved-store retriever.
- [x] T202: retrieval eval set.
- [x] T203: optional Mem0 adapter spike. Gate M9 `Allow`.

## Milestone 10: BehaviorPlanner

Goal: generate draft-only proactive action candidates without automatic sending.

- [x] T210: behavior schema. Review `PASS`.
- [x] T211: action-planner rule engine. Review `PASS`.
- [x] T212: proactive draft generator. Review `PASS`.
- [x] T213: CandidateAction review CLI. Review `PASS`.
- [x] T214: behavior safety eval. Review `PASS`. Gate M10 `Allow`.

## Milestone 11: OutboundSendGate + Feishu Sandbox

Goal: build a platform-independent send gate before any real adapter work.

- [x] T220: OutboundMessageRequest schema. Review `PASS`.
- [ ] T221: OutboundSendGate.
- [ ] T222: local fake adapter.
- [ ] T223: Feishu adapter.
- [ ] T224: Feishu review card.

## Milestone 12: WeChat Adapter

Goal: keep WeChat as a thin final adapter behind the send gate.

- [ ] T230: WeChat adapter research spike.
- [ ] T231: WeChat inbound adapter.
- [ ] T232: WeChat outbound adapter.
- [ ] T233: WeChat safety mode.

## Historical Current Unique Task

T220: OutboundMessageRequest Schema.

It is now complete and accepted with `PASS`. The next worker task is T221, because M11 now needs a deterministic send-gate policy over the separate outbound request contract before any fake adapter, Feishu adapter, scheduler, runtime path, or automatic send behavior.

T214: Behavior Safety Eval.

It is now complete and accepted with `PASS`. M10 closes with `Gate M10 Allow`. The next worker task is T220, because M11 must begin with a separate outbound request schema before send-gate policy, fake adapters, Feishu adapters, or review-card UX.

T213: CandidateAction Review CLI.

It is now complete and accepted with `PASS`. The next worker task is T214, because M10 needs a behavior safety evaluation over the T210-T213 review-only pipeline before any OutboundSendGate or platform work.

T212: Proactive Draft Generator.

It is now complete and accepted with `PASS`. The next worker task is T213, because M10 can now move from draft enrichment to manual review-state transitions while preserving the no-send/no-scheduler/no-platform boundary.

T211: Action Planner Rule Engine.

It is now complete and accepted with `PASS`. The next worker task is T212, because M10 can now move from deterministic candidate proposal to deterministic draft-text enrichment while preserving the no-send/no-scheduler/no-platform boundary.

T210: Behavior Schema.

It is now complete and accepted with `PASS`. The next worker task is T211, because M10 can now move from non-executable contracts to deterministic draft-only candidate proposal rules while preserving the no-send/no-scheduler/no-platform boundary.

T203: Optional Mem0 Adapter Spike.

It is now complete and accepted with `PASS`. M9 is complete at task level with Gate M9 `Allow`. The next worker task is T210, because proactive behavior must start with draft-only schemas before planner logic, scheduling, sending, or platform integration.

## Next Captain Output Required

When handing work to the next worker, Captain must output:

1. Current Unique Task
2. Why this task is next
3. Worker task package
4. Allowed files
5. Forbidden scope
6. Verification commands or acceptance criteria
7. Governance docs to update after completion
