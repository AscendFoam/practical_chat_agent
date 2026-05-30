# M13+ Milestone Plan

## Status

This roadmap is a T240 planning artifact. It does not mark future milestones as
implemented. Each milestone still requires task packages, verification, review,
and Captain judgment before the next milestone opens.

## Gate M13 Recommendation Options

`Gate M13 Allow`:
Only allows entry into M14 Persona Compiler schema/local creation work. It does
not authorize live platform delivery, automatic sending, unauthorized cloning,
voice/face deepfakes, creator marketplace, paid launch, or app-store work.

`Gate M13 Conditional`:
Use if the boundary pack is directionally correct but needs stronger sourcing,
redlines, or M14 scoping before implementation.

`Gate M13 Block`:
Use if the roadmap still attempts platform auto-send, unauthorized cloning,
deceptive real-person simulation, or implementation claims without evidence.

T240 worker recommendation: `Gate M13 Allow` for M14 schema/local Persona
Compiler work only, provided adversarial review finds no overclaiming or
boundary violations.

## Milestone Table

| Milestone | Goal | Scope | Non-goals | Review gate | Candidate task IDs |
| --- | --- | --- | --- | --- | --- |
| M13 Commercial Companion Product Boundary | Convert research into product positioning, safety tiers, architecture, roadmap, and first M14 task package. | Docs-only product, safety, architecture, roadmap, T250 package. | No implementation, no platform delivery, no automatic sending, no clone/deepfake. | Allow only M14 schema/local work. | T240 |
| M14 Persona Compiler | Define and locally prototype transparent, source-labeled, versioned personas. | PersonaCard v1, source/consent policy, local prompt-to-schema prototype, deidentification guard tests, version diff, review card. | No real-person clone, no private reads, no runtime dialogue changes, no proactive send. | Allow M15 only if L1 schema and L2 policy are safe. | T250-T255 |
| M15 Memory OS v2 | Separate factual, inferred, relational, procedural, and imagined memory with provenance and lifecycle controls. | MemoryRecordV2, truth status, migration plan, imagined-memory isolation, retrieval bundle, forget/freeze/tombstone, contamination eval. | No private raw transcript migration by default, no vector DB adoption, no imagined/factual mixing. | Allow M16 only if retrieval isolation is proven. | T260-T266 |
| M16 Relationship Engine Consumption | Make dialogue and behavior planners consume relationship semantics safely. | RelationshipStateV2, relationship policy, ReplyPlanner adapter, BehaviorPlanner adapter, repair scenarios, dependency-risk tests. | No intimacy escalation for retention, no automatic sending, no live platform path. | Allow M17 only if dependency and boundary downshift works. | T270-T276 |
| M17 Proactive Engine Consent | Design consented, rate-limited, review-first proactive companionship. | ProactiveConsent, policy/gate, quiet-hours/frequency/no-response tests, review card, crisis/low-mood policy. | No external-platform automatic sending, no guilt/coercion, no scheduler that sends messages. | Allow in-app/sandbox proactive only. | T280-T285 |
| M18 Virtual Life Stream | Implement text-first virtual life and role dynamics with imagined-memory isolation. | RoleDynamicPost, text generator, AIGC labels, contamination tests, dynamic review card. | No real-person photos, no unlabelled social posts, no live social platform publishing. | Allow only labeled text-first/synthetic stream. | T290-T295 |
| M19 Memory And Persona Control Surface | Provide prototype controls for viewing, editing, deleting, freezing, exporting, and auditing persona/memory records. | Requirements, viewer contract, persona version editor, delete/freeze/export flow, deletion verification. | No raw private transcript exposure, no production deletion claims without verifier. | Allow M20 only if user controls are testable. | T300-T305 |
| M20 Compliance And Safety Baseline | Establish first commercial-governance baseline for identity labels, consent, minors, training-use limits, AIGC labels, crisis handling, and platform policy readiness. | China checklist, international/platform checklist, Consent Center model, AIGC label plan, crisis/dependency policy tests. | No legal advice claim, no filing/submission claim, no launch approval. | Allow M21 closed-test UX only. | T310-T315 |
| M21 Text-First Product UX Prototype | Prototype persona creation, chat, memory explanation, life stream, proactive settings, and data controls. | IA, onboarding/persona prototype, chat+memory explanation, life stream, proactive settings, study protocol. | No voice/video, no real-person clone, no live external delivery, no public marketplace. | Allow limited alpha only if users understand AI identity and controls. | T320-T326 |
| M22 Voice And Avatar Exploration | Explore authorized voice and non-real-avatar routes after compliance baseline. | Voice survey, voice consent model, ASR/TTS benchmark, non-real avatar survey, multimodal labeling test. | No third-party voice clone, no real face generation, no deceased/public-figure mode, no live video production. | Allow sandbox only for authorized voices/non-real avatars. | T330-T335 |

## M14 Candidate Task List

- T250: PersonaCard v1 schema and source/consent policy.
- T251: Local prompt-to-schema Persona Compiler prototype.
- T252: DeidentificationGuard synthetic tests.
- T253: PersonaVersion diff and rollback repository.
- T254: Persona review card renderer.
- T255: M14 milestone review.

## M15 Candidate Task List

- T260: MemoryRecordV2 schema.
- T261: TruthStatus and MemoryType migration plan.
- T262: ImaginedMemoryStore isolation.
- T263: MemoryRetrieverV2 provenance bundle.
- T264: Forget/freeze/tombstone semantics.
- T265: Memory contamination eval.
- T266: M15 milestone review.

## M16 Candidate Task List

- T270: RelationshipStateV2 schema.
- T271: RelationshipPolicy rules.
- T272: ReplyPlanner relationship adapter.
- T273: BehaviorPlanner relationship adapter.
- T274: Conflict/repair synthetic scenarios.
- T275: Dependency-risk downshift tests.
- T276: M16 milestone review.

## M17 Candidate Task List

- T280: ProactiveConsent schema.
- T281: ProactivePolicy and gate.
- T282: Quiet-hours/frequency/no-response tests.
- T283: Proactive review card.
- T284: Crisis/low-mood scenario policy.
- T285: M17 milestone review.

## M18 Candidate Task List

- T290: RoleDynamicPost schema.
- T291: VirtualLifeEngine text generator.
- T292: AIGC labeling metadata.
- T293: Imagined/factual contamination tests.
- T294: Dynamic review card.
- T295: M18 milestone review.

## M19 Candidate Task List

- T300: Memory/persona control requirements.
- T301: Memory viewer data contract.
- T302: Persona version editor contract.
- T303: Delete/freeze/export local flow.
- T304: Deletion verification tests.
- T305: M19 milestone review.

## M20 Candidate Task List

- T310: China compliance checklist.
- T311: International privacy/platform policy checklist.
- T312: Consent Center data model.
- T313: AIGC labeling plan.
- T314: Crisis/dependency policy tests.
- T315: M20 milestone review.

## M21 Candidate Task List

- T320: UX information architecture.
- T321: Onboarding/persona creation prototype.
- T322: Chat plus memory explanation prototype.
- T323: Life stream prototype.
- T324: Proactive settings prototype.
- T325: User study protocol.
- T326: M21 milestone review.

## M22 Candidate Task List

- T330: Voice technology survey.
- T331: Voice consent data model.
- T332: ASR/TTS latency benchmark.
- T333: Non-real avatar route survey.
- T334: Multimodal labeling test.
- T335: M22 milestone review.

## Roadmap Safety Invariants

- One Current Unique Task at a time.
- Review and Captain integration before opening the next task.
- Private chat history and private distilled artifacts never enter committed
  docs/examples/tests.
- Future plans must not be written as completed facts.
- L5 unauthorized clone behavior remains prohibited.
- Automatic sending remains blocked unless a later task explicitly changes
  policy and passes review.
- Imagined memory must remain isolated from factual memory.
