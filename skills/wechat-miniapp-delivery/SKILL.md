---
name: wechat-miniapp-delivery
description: Universal WeChat miniapp delivery skill for Codex, Claude Code, and OpenClaw. Use when an agent needs to plan, implement, validate, deploy, or release a WeChat mini program change across native-weapp, Taro, uni-app, or hybrid miniapp repos with coordinated developer, release-manager PM, unit and API-contract testing, functional acceptance, visual runtime acceptance, E2E QA, performance acceptance, CloudBase, compliance, or release fallback work.
---

# Wechat Miniapp Delivery

Use this skill as an evidence-first delivery orchestrator. Scale the process to the task, load only references that match the current risk, and preserve proof for every claim.

## Non-Negotiable Rules

- Inspect the repository before choosing a framework, backend, test, or release path.
- Never claim preview, upload, deploy, or publish success without evidence from the tool that performed it.
- Never print or commit `AppSecret`, private keys, merchant secrets, or long-lived tokens.
- Prefer server-side or CloudBase execution for payment, messaging, and privileged APIs.
- If credentials or tooling are missing, complete only safe stages and return an explicit blocker list plus the next setup step.
- Split `feature delivery` from `release enablement` when a feature can be implemented but not safely released.
- For user-visible UI changes, load `wechat-miniapp-design`, define a visual state matrix, and require rendered runtime evidence. Static checks alone do not close visual acceptance.

## Select A Delivery Profile

Select exactly one profile before planning. New risk can increase rigor, never reduce it.

### `quick`

Use for a local, low-risk change that does not alter a shared API contract or request preview, upload, deploy, or publish.

Required exit evidence:
- changed files and rationale
- focused static, unit, or runtime validation
- visual state evidence when UI is affected
- residual risk or explicit `none`

Do not create a full PM task graph, assign every QA role, run environment doctor, or produce release artifacts unless wider impact appears.

### `standard`

Use for feature-sized or multi-file work, shared UI or logic, touched contracts, or coordinated functional, visual, E2E, or performance acceptance.

Required exit evidence:
- scoped plan and acceptance dimensions
- relevant preflight and developer test obligations
- applicable acceptance evidence and blockers
- next owner; rollback only for stateful or release-sensitive work

### `release-critical`

Use for preview, upload, deploy, publish, production configuration, privileged credentials, payment, privacy, authentication, production data, or rollback-sensitive infrastructure.

Required exit evidence:
- full plan, environment doctor, preflight, risk register, and ownership
- applicable quality, security, privacy, and compliance gates
- release or blocker evidence, observation plan, next owner, and rollback target

Escalate `quick -> standard` for shared contracts or multiple ownership areas. Escalate any task to `release-critical` when release intent or a high-risk module enters scope.

## Inspect And Route

Detect:

1. Target: native WeChat, Taro, uni-app, hybrid, or WebView shell.
2. Backend: CloudBase, custom, hybrid, or none.
3. Release path: `miniprogram-ci`, framework wrapper, manual-only, or blocked.
4. Test and observability tooling already used by the repository.
5. Risk modules: payment, privacy, location, auth, AI, CloudBase, WebView compatibility, native UI runtime.
6. Acceptance needed: developer tests, functional, visual runtime, E2E, performance, compliance, release.

Stop clearly if the repository is not a WeChat mini program project.

### Load References On Demand

Do not open every reference preemptively.
Context efficiency is a routing constraint, never a reason to skip guidance required by the selected profile, changed risk, or acceptance evidence.

Use progressive context loading:

1. Start with this entrypoint. Inspect the repository, select the profile, and list active risks, acceptance needs, and unresolved decisions.
2. Before loading a reference, name the unresolved decision it will answer. Search its headings or contents and read the smallest relevant section first.
3. Distill loaded guidance into a short working checklist. Do not paste it into the plan, reread resolved sections, or load adjacent references without a new trigger.
4. Load the next section only when inspection or evidence exposes another gap. Stop when implementation and acceptance decisions are supported.
5. For release-critical work, load workflow, tooling and risk, contracts, and affected framework guidance sequentially. Do not omit a required gate merely to reduce context.

| Trigger | Load |
| --- | --- |
| Quick UI alignment, dynamic layout, modal, theme, or native-layer issue | `wechat-miniapp-design` and its `references/runtime-ui-quality-gates.md` only |
| Multi-stage work or worker coordination | `references/workflow-and-handoffs.md` |
| Plan, validation, or release JSON output | `references/json-contracts.md` |
| Concrete full handoff example | `references/example-handoff-pack.md` |
| Release tooling, environment doctor, compliance, or high-risk modules | `references/tooling-and-risk-checklists.md` |
| Capability-module selection or portability | `references/delivery-toolchain-catalog.md` |
| Changed business logic, APIs, or cloud functions | `references/developer-test-obligations.md` |
| Functional, visual, E2E, or performance evidence boundaries | `references/qa-and-acceptance-matrix.md` |
| Shared packages or multiple framework targets | `references/multi-platform-miniapp-patterns.md` |
| Taro 4 React | `references/taro4-react-patterns.md` |
| Thin native shell loading H5 through `<web-view>` | `references/webview-shell-patterns.md` |

For quick work, load only the matching narrow reference. For release-critical work, the workflow, tooling, contracts, and affected framework references are normally required.

## Execute The Delivery Loop

### 1. Plan

- Record `workflow_profile`, goal, target, scope, acceptance, risk, release intent, and fallback.
- For quick work, use one success case and a compact response.
- For standard or release-critical work, use 2-3 concrete use cases and a task graph.
- Use `references/json-contracts.md` only when structured contracts help the handoff.

### 2. Preflight

- Quick: inspect only tools and runtime needed by the change.
- Standard or release-critical: verify versions, build path, app ID, domains, credentials, DevTools or E2E readiness, observability, and compliance.
- Do not let a missing release prerequisite block safe implementation work.

### 3. Implement

- Follow existing repository patterns and change feature code, cloud code, config, and test seams together when required.
- Keep shared code free of direct platform dependencies where the architecture already uses adapters.
- Add stable selectors, mockable boundaries, and release markers only when they support an acceptance need.
- For user-visible UI, use `wechat-miniapp-design`; for business logic or interfaces, apply Developer and API Contract Test obligations.

### 4. Validate

Run only applicable gates, but never omit one that covers the changed risk:

- static checks and focused unit tests
- API Contract Test for touched request or response surfaces
- functional acceptance for user-visible behavior and failure states
- Visual Runtime Acceptance QA for user-visible UI
- E2E for the top critical flow when the runner is ready
- performance comparison when startup, lists, media, or heavy rendering can regress
- security, privacy, payment, permission, and secret checks for high-risk work

Visual runtime acceptance must audit the affected control family, repeat conditional toggles, verify modal layering over native components, cover affected themes, and capture rendered evidence.

### 5. Decide

Compare evidence with acceptance criteria, not merely green tests. Report:

- pass, fail, or blocked per applicable dimension
- feature-delivery and release-enablement status
- artifacts and exact blockers
- residual risk and next owner

Use `go`, `no-go`, or `needs-review` for release decisions.

### 6. Release And Watch

- Prefer replayable preview, upload, and deploy actions.
- Record version, mode, QR or artifact path, logs, observation notes, and rollback target.
- If upload is blocked, downgrade to preview-only when safe.
- If E2E is blocked, use deterministic unit or simulate evidence and state the residual risk.
- Never mark a candidate `publish-ready` without required observability or an explicit waiver.

## Role And Delegation Boundary

Use detailed roles only for standard or release-critical work. The normal ownership areas are PM or release coordination, implementation, unit and contract tests, functional QA, visual QA, E2E, and performance. Read `references/workflow-and-handoffs.md` before delegating.

Keep one writer per file, give each worker a goal, non-goals, owned paths, inputs, success check, required output, and next owner. If subagents are unavailable, execute the same handoffs sequentially.

## Minimum Output

Always include:

- selected profile
- what changed or was planned
- validation performed and evidence
- blockers and residual risk
- next owner or completion decision

Add release evidence and rollback only when release or stateful risk is in scope.
