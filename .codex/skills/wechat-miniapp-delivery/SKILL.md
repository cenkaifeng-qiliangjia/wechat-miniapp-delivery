---
name: wechat-miniapp-delivery
description: Build, modify, test, accept, and release WeChat mini programs with coordinated developer, release-manager PM, unit-test, and E2E QA roles. Use when Codex needs to work on a miniapp repo, add a feature, fix a bug, validate release readiness, coordinate CloudBase or miniprogram-ci tooling, or ship a change safely from plan through preview or upload.
---

# Wechat Miniapp Delivery

Use this skill to run a full miniapp delivery loop. Keep `SKILL.md` focused on the orchestration skeleton and load the linked references only when needed.

Common use cases:
- Implement a feature and produce a release candidate.
- Validate whether a branch is ready for preview, upload, or publish.
- Coordinate coding, unit tests, E2E, acceptance, and release handoffs across multiple workers.

## Core Rules

- Start with 2-3 concrete use cases for the task at hand before editing.
- Treat the work as staged delivery, not just code generation.
- Prefer problem-first orchestration: the user states the outcome, then you choose the right framework path and tools.
- Keep structured artifacts compact and handoff-friendly. Another role should be able to continue from your summary alone.
- Never claim release success without evidence from the tool that actually performed the release.
- Never commit or print high-sensitivity values such as `AppSecret`, `privateKey`, merchant keys, or long-lived tokens.
- Prefer server-side or CloudBase execution for payment, messaging, and privileged open API calls.
- If the environment does not support subagents, emulate the same role handoffs sequentially and keep the same artifacts.

## Workflow Decision

1. Inspect the repo shape before planning.
2. Detect `native-weapp`, `Taro`, or `uni-app`.
3. Detect backend mode: `CloudBase`, self-hosted backend, or hybrid.
4. Detect the release path: `miniprogram-ci`, framework plugin, or manual-only.
5. Detect the existing test stack, observability stack, and compliance config.
6. Choose one working mode:
   - `plan`
   - `implement`
   - `validate`
   - `release`
7. If the repo is not a WeChat mini program project, stop and say so clearly.
8. If the repo is hybrid or only partially wired for release, split the work into:
   - delivery work that is safe now
   - release-enablement work that must be finished before preview or upload
9. If credentials, DevTools automation, or release keys are missing, continue only with the safe stages and hand back an explicit blocker list.

## Orchestrate Roles

Use the following roles when the task is larger than a quick one-file edit or when the user explicitly wants parallelism.

### Version Manager PM

- Own scope freeze, version intent, task graph, acceptance gates, and go or no-go decisions.
- Keep a release-candidate summary with risks, blockers, owner, version, and rollback target.
- Avoid editing feature code unless the user explicitly asks for release notes or version metadata changes.

### Developer

- Own implementation files, configuration, CloudBase resources, and test hooks such as stable selectors.
- Update related config when changing risky flows: request domains, `project.config.json`, cloud function `config.json`, permissions, or monitoring tags.
- Produce a compact change summary and note any environment blockers.

### Unit Test

- Own component, store, and business-function tests.
- Focus first on changed modules and critical pure logic.
- Report coverage, failures, and missing seams that block deterministic testing.

### E2E QA

- Own critical-flow regression in preview or DevTools automation environments.
- Collect screenshots, logs, failing selectors, and repro steps.
- If automation is flaky, reduce scope to the core flows and make the instability explicit instead of silently skipping it.

## Delegate Safely

If subagents are available, prefer one writer plus parallel read-only or disjoint-write workers:
- PM scout: planning, risk list, acceptance matrix
- Developer: app, cloud, and config files
- Unit test worker: unit tests only
- E2E QA worker: E2E scripts and evidence only

Run them in this order:
1. PM produces the plan and ownership.
2. Developer implements against that plan.
3. Unit and E2E workers run in parallel on disjoint files.
4. Orchestrator integrates fixes, reruns gates, and returns to PM for final go or no-go.

Do not let multiple workers edit the same files unless the write boundaries are explicit and non-overlapping.

Read `references/workflow-and-handoffs.md` when you need a fuller stage table, worker context pack, or handoff structure.
Read `references/example-handoff-pack.md` when you want a filled-in example for a realistic feature request.

## Run The Stage Workflow

### 1. Plan The Change

- Translate the request into `Plan JSON`.
- Record:
  - feature goal
  - framework and runtime path
  - acceptance criteria
  - release target: `preview`, `upload`, `publish-ready`, or `none`
  - risk modules such as `payment`, `location`, `auth`, `maps`, `AI`, or `privacy`
- If the user only asked for planning, stop here and hand back the plan plus the next recommended owner.
- Read `references/json-contracts.md` when you need a ready-made schema.

### 2. Run Preflight

- Verify build path, app ID, release key path, allowed domains, npm build requirements, and DevTools or E2E prerequisites.
- Verify release tooling:
  - Taro: prefer `@tarojs/plugin-mini-ci` if already present and stable
  - Native: prefer `miniprogram-ci`
  - CloudBase: verify env ID, permissions, and deployment path
- Block early if the change cannot be validated safely.
- Read `references/tooling-and-risk-checklists.md` for the exact preflight list.

### 3. Implement Safely

- Change feature code, cloud functions, and config together.
- Add test seams while implementing:
  - stable selectors
  - mockable data boundaries
  - observability tags or release markers
- For payment or open API flows, prefer server or cloud execution and include callback verification, idempotency, and fallback query logic.

### 4. Run Quality Gates

- Run static checks first.
- Run unit tests for changed modules and shared logic.
- Run E2E against the core path only after the preview or DevTools environment is ready.
- Run compliance gates:
  - secrets scan
  - privacy declaration alignment
  - CloudBase or open API permission checks
- Do not mark the task complete if gates were skipped without a written reason.

### 5. Decide Acceptance

- Compare results against the acceptance matrix, not just "tests green".
- Produce:
  - pass or fail per criterion
  - artifacts
  - unresolved risks
  - recommended next owner
- Use PM ownership to decide `go`, `no-go`, or `needs-review`.

### 6. Prepare Release And Watch The Outcome

- Prefer replayable release actions via `preview` or `upload`.
- Capture structured release evidence: version, mode, QR or build artifact path, logs, release notes, and rollback target.
- Verify the chosen observability provider after the release or preview validation.
- Keep a hotfix or rollback path ready before calling the release done.

## Handle Common Problems

### Release Tooling Missing

- Symptom: no `miniprogram-ci`, no framework CI plugin, or missing key path.
- Action: stop before release, document the missing prerequisite, and continue only with plan, implementation, or validation steps that are safe.

### E2E Environment Flaky

- Symptom: DevTools automation port or preview environment is unstable.
- Action: keep unit coverage as the minimum gate, restrict E2E to the top 1-3 flows, and record the remaining risk explicitly.

### Sensitive Flow Under-Specified

- Symptom: payment, privacy, login, map, or AI work is requested without a backend or compliance story.
- Action: stop and add the missing design constraints before shipping. Do not invent a release-safe path.

## Example Requests

### Feature Delivery

User says: "Add payment confirmation to the order detail page and prepare a preview release."

- Plan the feature and mark `payment` as high risk.
- Implement UI, backend or cloud payment path, callback safety, and stable selectors.
- Run unit coverage for order and payment logic.
- Run E2E for detail to pay confirmation.
- Return acceptance summary, preview evidence, and rollback target.

### Release Readiness

User says: "Check whether this miniapp version is safe to ship."

- Skip new feature implementation.
- Run preflight, compliance, unit, E2E, and release checks.
- Produce a go or no-go summary with blockers and recommended fixes.

## Read References

- Open `references/workflow-and-handoffs.md` for role ownership, artifact handoffs, and delegation patterns.
- Open `references/tooling-and-risk-checklists.md` for framework selection, release tooling, compliance, and high-risk checks.
- Open `references/json-contracts.md` for reusable plan, validation, and release JSON shapes.
- Open `references/example-handoff-pack.md` for a realistic PM to developer to unit to E2E handoff example.
