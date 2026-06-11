# QA And Acceptance Matrix

Use this reference when splitting acceptance work across QA roles or when deciding what evidence is required before a miniapp change can be called ready.

## Functional Acceptance QA

Own business correctness and edge-case behavior.

Check at least:
- happy path
- empty state
- loading and retry state
- permission denied path
- offline or weak-network behavior if relevant
- error toast, modal, or fallback copy

Required output:
- acceptance matrix with pass or fail per criterion
- exact repro for failures
- residual risk list

## E2E QA

Own automation for the top user flows that prove the release candidate is real.

Check at least:
- critical route transitions
- stable selectors
- primary data mutation or confirmation path
- screenshots, logs, and artifact paths for pass or fail

Required output:
- executed flow list
- failed step if any
- screenshots or logs
- degraded-mode note if automation fell back to simulate or manual evidence

## Visual Runtime Acceptance

Own rendered UI correctness for user-visible changes. Load `wechat-miniapp-design`, then use its `references/runtime-ui-quality-gates.md` for the detailed workflow.

Check at least:
- affected text-only and icon-and-text controls in default, pressed, disabled, and modal states
- conditional helper text or validation content with hidden and visible states
- card and neighboring-control stability during repeated toggles
- sheets and modals in every affected theme
- overlap with `canvas`, `map`, `video`, `camera`, `textarea`, or other native components
- real-device behavior when simulator rendering is not representative

Required output:
- visual state matrix with pass or fail per state
- screenshots, recording, or equivalent rendered evidence
- audited shared control family
- exact blocker and device or runtime when a failure remains

## Performance Acceptance QA

Own release-readiness from a user-experience and runtime-cost perspective.

Check at least:
- startup or first-screen behavior
- critical page load latency
- request count spikes
- oversized images or bundle regressions
- long lists, rich content, or heavy components on low-end devices if they are in scope

Use repo budgets if they already exist. If no budget exists, compare against the current main branch or known stable baseline instead of inventing a hard threshold.

Required output:
- baseline used
- observed regressions or wins
- blocking performance issues
- waiver note if a regression is accepted temporarily

## Acceptance Pack Shape

Every meaningful acceptance handoff should state:
- criterion
- owner
- proof
- status
- blocker or waiver

Keep these sections distinct:
- functional acceptance
- visual runtime acceptance
- E2E acceptance
- performance acceptance

Do not collapse them into one generic `QA passed` summary.
