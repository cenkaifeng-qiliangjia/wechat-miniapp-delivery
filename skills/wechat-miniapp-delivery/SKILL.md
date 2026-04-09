---
name: wechat-miniapp-delivery
description: Universal WeChat miniapp delivery skill for Codex, Claude Code, and OpenClaw. Use when an agent needs to plan, implement, validate, deploy, or release a WeChat mini program change across native-weapp, Taro, uni-app, or hybrid miniapp repos with coordinated developer, release-manager PM, unit and API-contract testing, functional acceptance, E2E QA, performance acceptance, CloudBase, compliance, or release fallback work.
---

# Wechat Miniapp Delivery

Use this skill as an evidence-first delivery orchestrator, not a generic miniapp helper. Every medium or large task should leave behind `plan -> preflight -> implement -> validate -> release-or-blocker` outputs, each with artifacts, blockers, the next owner, and a rollback target.

Common use cases:
- Implement a feature and produce a release candidate.
- Validate whether a branch is ready for preview, upload, or publish.
- Coordinate coding, unit tests, API contract checks, functional acceptance, E2E, performance acceptance, deployment, and release handoffs across multiple workers.

## Core Rules

- Start with 2-3 concrete use cases for the task at hand before editing.
- Treat release, test, deploy, and compliance work as explicit tool contracts, not ad-hoc shell commands.
- Run an environment doctor before promising preview, upload, E2E, CloudBase MCP, or `minium`.
- Keep structured artifacts compact and handoff-friendly. Another role should be able to continue from your summary alone.
- Never claim preview, upload, deploy, or publish success without evidence from the tool that actually performed it.
- Never commit or print high-sensitivity values such as `AppSecret`, `privateKey`, merchant keys, or long-lived tokens.
- Prefer server-side or CloudBase execution for payment, messaging, and privileged open API calls.
- If release tooling or credentials are missing, continue only with safe stages and return an explicit blocker list plus the next setup step.
- If the repo is hybrid or only partially wired, split status into `feature delivery` and `release enablement`.
- Keep outputs agent-neutral so the same skill works under Codex, Claude Code, and OpenClaw.
- If the environment does not support subagents, emulate the same role handoffs sequentially and keep the same artifacts.

## V5 Workflow Decision

1. Inspect the repo shape before planning.
2. Detect `native-weapp`, `Taro`, `uni-app`, or a hybrid cross-platform workspace.
   - Read `references/multi-platform-miniapp-patterns.md` when the repo mixes shared packages, more than one shell, or more than one framework variant.
   - If Taro 4 with React, read `references/taro4-react-patterns.md` before implementing.
3. Detect whether the miniapp is a **WebView shell** (thin native shell loading an H5 app via `<web-view>`) or a native-page miniapp.
   - Read `references/webview-shell-patterns.md` when the miniapp has very few native pages and loads an H5 URL in a `<web-view>`.
   - WebView shell projects have distinct delivery, testing, CSS compatibility, and release coordination concerns.
4. Detect the framework subtype that actually owns the WeChat build target.
5. Detect backend mode: `CloudBase`, self-hosted backend, or hybrid.
6. Detect the release path: `miniprogram-ci`, framework plugin, `manual-only`, or `blocked`.
7. Detect the existing test stack, observability provider, and compliance config.
8. Detect risk modules such as `payment`, `privacy`, `location`, `auth`, `AI`, `cloudbase`, or `webview-css-compat`.
9. Detect acceptance scope:
   - functional acceptance
   - E2E acceptance
   - performance acceptance
   - developer test obligations for changed APIs and shared logic
10. Run an environment doctor before choosing release or E2E scope:
   - `miniprogram-ci`: Node `>=16.1.0`
   - CloudBase MCP: Node `>=18.15.0`
   - `minium`: Python `>=3.8`
11. Choose one or more capability modules:
   - `weapp_ci_release`
   - `weapp_test_automation`
   - `cloudbase_env_deploy`
   - `security_compliance_gate`
12. Choose one working mode:
   - `plan`
   - `implement`
   - `validate`
   - `release`
13. If the repo is not a WeChat mini program project, stop and say so clearly.
14. If the repo is hybrid or only partially wired for release, split the work into:
   - delivery work that is safe now
   - release-enablement work that must be finished before preview or upload
15. If credentials, DevTools automation, or release keys are missing, continue only with the safe stages and hand back an explicit blocker list.
16. If the project is a WebView shell, also determine whether the current change requires a miniapp release, an H5 deployment, or both. Read `references/webview-shell-patterns.md` for release coordination rules.

Read `references/delivery-toolchain-catalog.md` when you need the module matrix, contract fragments, or downgrade policy.
Read `references/qa-and-acceptance-matrix.md` when you need acceptance-role boundaries or evidence requirements.
Read `references/developer-test-obligations.md` when the developer changes business logic, API surfaces, or cloud functions.

## Capability Modules

Use capability modules as the first-class execution units for delivery work:

### `weapp_ci_release`

- Own `build_npm`, `preview`, `upload`, and `full_release`.
- Prefer `miniprogram-ci`, or the framework wrapper if the repo already standardized on it.
- Must return mode used, artifacts, logs, and whether the run degraded to a safer path.

### `weapp_test_automation`

- Own unit coverage, simulate-based checks, and E2E automation.
- Prefer `miniprogram-simulate` plus the repo test runner for deterministic coverage.
- Use `miniprogram-automator` or `minium` only when the runner and DevTools path are actually ready.

### `cloudbase_env_deploy`

- Own CloudBase env targeting, cloud function deploys, hosting deploys, indexes, and logs.
- Prefer CloudBase MCP when available, with CloudBase CLI as the standard fallback.
- Must never switch env IDs implicitly.

### `security_compliance_gate`

- Own secrets scanning, privacy alignment, payment callback engineering rules, permissions, and release-watch readiness.
- Prefer `gitleaks` plus `trufflehog` for secrets coverage.
- Block high-risk release work when payment, privacy, or secret handling cannot be validated.

## Orchestrate Roles

Use the following roles when the task is larger than a quick one-file edit or when the user explicitly wants parallelism.

### Version Manager PM

- Own scope freeze, version intent, task graph, acceptance gates, and go or no-go decisions.
- Keep a release-candidate summary with risks, blockers, owner, version, downgrade path, and rollback target.
- Avoid editing feature code unless the user explicitly asks for release notes or version metadata changes.

### Developer

- Own implementation files, configuration, CloudBase resources, and test hooks such as stable selectors.
- Update related config when changing risky flows: request domains, `project.config.json`, cloud function `config.json`, permissions, or monitoring tags.
- Own the first-pass test obligation for changed logic and touched APIs.
- Produce a compact change summary, touched API surface list, and note any environment blockers.

### Unit And API Contract Test

- Own component, store, business-function, and touched-interface contract tests.
- Focus first on changed modules and critical pure logic.
- Report coverage, failures, stale fixtures, contract mismatches, and missing seams that block deterministic testing.

### Functional Acceptance QA

- Own business-flow acceptance, edge cases, empty states, retry states, and permission-denied behavior.
- Keep the acceptance matrix grounded in user-visible behavior rather than implementation details.
- Return pass or fail per criterion with clear repro for any blocker.

### E2E QA

- Own critical-flow regression in preview or DevTools automation environments.
- Collect screenshots, logs, failing selectors, and repro steps.
- If automation is flaky, reduce scope to the core flows and make the instability explicit instead of silently skipping it.

### Performance Acceptance QA

- Own startup, first-screen, request-count, heavy-list, rich-content, and low-end-device risk review when the change can affect runtime cost.
- Prefer repo budgets if they exist. Otherwise compare against the current main branch or known stable baseline.
- Return observed regressions, residual risk, and waiver needs explicitly.

### Release Owner

- Default to the PM or orchestrator when no separate release role exists.
- Own preview, upload, CloudBase deploy, release evidence, observation notes, and rollback preparation.
- Never sign off without the artifact path, logs, and watch notes.

## Delegate Safely

If subagents are available, prefer one writer plus parallel read-only or disjoint-write workers:
- PM scout: planning, risk list, acceptance matrix
- Developer: app, cloud, and config files
- Unit and API contract worker: deterministic tests and fixtures only
- Functional QA worker: acceptance matrix only
- E2E QA worker: E2E scripts and evidence only
- Performance QA worker: performance evidence only

Run them in this order:
1. PM produces the plan and ownership.
2. Developer implements against that plan.
3. Unit and API contract validation starts as soon as implementation seams exist.
4. Functional, E2E, and performance acceptance run in parallel on disjoint artifacts.
5. Orchestrator integrates fixes, reruns gates, and returns to PM or release owner for final go or no-go.

Do not let multiple workers edit the same files unless the write boundaries are explicit and non-overlapping.

Read `references/workflow-and-handoffs.md` when you need a fuller stage table, worker context pack, or handoff structure.
Read `references/example-handoff-pack.md` when you want a filled-in example for a realistic feature request.

## High-Risk Gates

- `payment`: callback signature verification, `5s` acknowledgement, retry awareness, idempotency, query fallback, AES-256-GCM decryption, and no client-side secrets.
- `privacy`: declaration alignment, `usePrivacyCheck` or equivalent gate, consent timing, data minimization, and no hidden collection path.
- `location`: key scope, request domains, permission messaging, and cost or license review.
- `auth`: token storage path, session expiry behavior, and no sensitive logs.
- `AI`: quota or cost limits, timeout fallback, and moderation or safety hooks where applicable.
- `cloudbase`: env targeting, `config.json` permissions, secret placement, retry behavior, and rollback path.
- `webview-shell`: H5 domain registered as business domain, domain verification file deployed, PostCSS compatibility pipeline intact (especially `postcss-layer-unwrap` for Tailwind v4), URL allowlist enforced, bridge message types consistent across H5 and miniapp, production build uses correct H5 URL (not localhost).

If a high-risk gate cannot be validated, do not mark the change `publish-ready`.

## Run The Stage Workflow

### 1. Plan

- Translate the request into `Plan JSON`.
- Record:
  - feature goal
  - framework, runtime, backend, and shared-code path
  - selected capability modules
  - acceptance criteria
  - release target: `preview`, `upload`, `publish-ready`, or `none`
  - risk modules such as `payment`, `location`, `auth`, `maps`, `AI`, or `privacy`
  - functional, E2E, and performance acceptance scope
  - developer test obligations for changed APIs and shared logic
  - fallback policy and rollback target
- If the user only asked for planning, stop here and hand back the plan plus the next recommended owner.
- Read `references/json-contracts.md` when you need a ready-made schema.

### 2. Run Environment Doctor And Preflight

- Verify version floors, build path, app ID, release key path, allowed domains, npm build requirements, and DevTools or E2E prerequisites.
- Verify release tooling, CloudBase channels, observability provider, and compliance config.
- Verify framework-specific output paths and shared-package boundaries when the repo is multi-platform.
- Block only the unsafe stages when the environment is incomplete.
- Return the blocker list with the exact downgrade plan.
- Read `references/tooling-and-risk-checklists.md` for the exact preflight list.

### 3. Implement

- Change feature code, cloud functions, and config together.
- When working in a cross-platform or hybrid repo, keep `weapp acceptance` and `shared impact` distinct.
- When working in a Taro 4 React project, follow the framework patterns in `references/taro4-react-patterns.md` to avoid common pitfalls.
- When building or modifying UI, follow the design system and visual standards in `wechat-miniapp-design` skill for token discipline, miniapp CSS constraints, and component patterns.
- Follow `references/developer-test-obligations.md` when touching business logic, APIs, or cloud functions.
- Add test seams while implementing:
  - stable selectors
  - mockable data boundaries
  - observability tags or release markers
- For payment or open API flows, prefer server or cloud execution and include callback verification, idempotency, and fallback query logic.

### 4. Run Tool Gates

- Run static checks first.
- Run `security_compliance_gate`.
- Run unit and interface-contract tests for changed modules, shared logic, and touched APIs.
- Run functional acceptance against the explicit acceptance matrix.
- Run E2E against the core path only after the preview or DevTools environment is ready.
- Run performance acceptance when startup, list rendering, rich content, media, or release-readiness is in scope.
- Run CloudBase deployment only when the feature or release depends on it.
- Run preview or upload only when release prerequisites are present.
- Capture tool outputs, artifacts, warnings, blockers, and fallback mode for every capability module.

### 5. Decide Acceptance

- Compare results against the acceptance matrix, not just "tests green".
- Produce:
  - pass or fail per criterion
  - feature-delivery status
  - release-enablement status if different
  - functional acceptance status
  - E2E acceptance status
  - performance acceptance status
  - developer test obligation status
  - artifacts
  - unresolved risks
  - recommended next owner
- Use PM ownership to decide `go`, `no-go`, or `needs-review`.

### 6. Release And Watch

- Prefer replayable release actions via `preview` or `upload`.
- Capture structured release evidence: version, mode, QR or build artifact path, logs, release notes, rollback target, and observation notes.
- Verify the chosen observability provider after the release or preview validation.
- Keep a hotfix or rollback path ready before calling the release done.

## Default Downgrade Rules

- Upload blocked by auth or network: downgrade to `preview-only` and return the exact blocker.
- E2E blocked by DevTools or runner instability: downgrade to `unit-plus-simulate` and record the residual risk.
- CloudBase MCP unavailable: downgrade to CloudBase CLI with the same env target and summary format.
- Compliance signal partial or ambiguous: block high-risk release work, but continue low-risk implementation with a remediation list.
- Observability missing for a release candidate: do not mark the task `publish-ready` without an explicit waiver.

## Release Evidence

Minimum release evidence:
- version string
- mode used: `preview`, `upload`, `deploy-only`, or `publish-ready`
- QR code path or build artifact path
- tool logs or structured result
- rollback target
- observation notes

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
- Run environment doctor, preflight, compliance, unit, E2E, and release checks.
- Produce a go or no-go summary with blockers and recommended fixes.

### WebView Shell Delivery

User says: "The H5 page shows no styles inside the miniapp WebView."

- Identify the project as a WebView shell architecture.
- Check the H5 PostCSS pipeline for `postcss-layer-unwrap` (required for Tailwind v4).
- Check for `oklch()` color usage without a fallback plugin.
- Verify the H5 domain is registered as a business domain in the admin console.
- If CSS features were recently added, verify WebView engine compatibility.
- Return the root cause, the PostCSS fix, and whether an H5 redeployment is sufficient or a miniapp release is also needed.

## Read References

- Open `references/workflow-and-handoffs.md` for role ownership, artifact handoffs, and delegation patterns.
- Open `references/tooling-and-risk-checklists.md` for framework selection, release tooling, compliance, and high-risk checks.
- Open `references/json-contracts.md` for reusable plan, validation, and release JSON shapes.
- Open `references/example-handoff-pack.md` for a realistic PM to developer to unit to E2E handoff example.
- Use `wechat-miniapp-design` skill for design token system, miniapp CSS constraints, component patterns, and visual quality checklist.
- Open `references/delivery-toolchain-catalog.md` for the capability-module matrix, tool fragments, and portability notes.
- Open `references/multi-platform-miniapp-patterns.md` for shared-package and framework-variant rules.
- Open `references/qa-and-acceptance-matrix.md` for functional, E2E, and performance acceptance expectations.
- Open `references/developer-test-obligations.md` for unit and API-contract test responsibilities.
- Open `references/webview-shell-patterns.md` for WebView shell architecture, bridge communication, CSS compatibility, domain verification, and release coordination.
- Use `wechat-miniapp-design` skill for design token system, miniapp CSS constraints, component patterns, and visual quality checklist.
