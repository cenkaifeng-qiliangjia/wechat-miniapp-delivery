# Workflow And Handoffs

Use this reference when the task spans more than one stage or when you need worker coordination. This is the evidence-first V2 flow: every handoff should preserve plan, blockers, fallback, evidence, and rollback information.

## Ground The Task In Concrete Use Cases

Use one or more of these starting frames:
- Implement a feature and ship a preview build.
- Harden a release candidate before upload.
- Fix a high-risk bug and decide go or no-go.

If the current task does not fit one of these frames, write a new one-sentence use case before assigning work.

## Run The Delivery Stages

| Stage | Primary owner | Goal | Exit artifact |
| --- | --- | --- | --- |
| Intake and plan | PM | Convert the request into a scoped delivery plan | Plan JSON, acceptance matrix, risk list |
| Environment doctor | PM plus developer | Confirm version floors, credentials, automation runners, and tool availability | Environment report with downgrade path |
| Preflight | PM plus developer | Confirm framework, build, release, compliance, and observability prerequisites | Preflight report with blockers |
| Implementation | Developer | Change code, config, cloud resources, and test seams | Change summary and owned file list |
| Tool gates | Developer, unit, E2E, or orchestrator | Catch formatting, secrets, privacy, unit, E2E, and deploy issues | Capability-run summary with pass, fail, or degraded mode |
| Unit gate | Unit test | Prove changed logic is deterministic and covered | Coverage and failure report |
| E2E and acceptance | E2E QA plus PM | Verify the main user path and gather acceptance evidence | Evidence pack and go or no-go recommendation |
| Release and watch | Release owner, defaulting to PM | Produce preview or upload evidence, watch notes, and rollback readiness | Release summary, observation notes, rollback target |

Use a sequential workflow for the main path and an iterative refinement loop after validation:
1. PM plans.
2. PM and developer run environment doctor and preflight.
3. Developer implements.
4. Unit and E2E validate.
5. Orchestrator or developer fixes.
6. PM or release owner closes the loop.

If the project is hybrid or release tooling is incomplete, keep two status tracks:
- `feature delivery`
- `release enablement`

## Build A Worker Context Pack

Give each worker the minimum context needed to succeed:
- Goal: what done looks like
- Non-goals: what not to touch
- Owned paths: files or directories they may change
- Inputs: requirement, plan slice, acceptance criteria, risk modules, capability modules
- Environment and fallback: what tool path is expected, what downgrade path is allowed
- Success check: tests, artifacts, or gate result expected
- Required output: changed files, evidence, blockers, fallback used, next owner
- Rollback note: what state should be preserved if the work touches release or deploy surfaces

If you cannot give a worker a clear write boundary, keep the work local instead of parallelizing it.

## Assign Role Contracts

### PM worker

Use for planning, release coordination, and go or no-go decisions.

Expected output:
- plan summary
- acceptance matrix
- risk register
- environment doctor
- release recommendation
- rollback target

Default ownership:
- read-only on product code
- may edit release notes, version checklist, or deployment notes if explicitly assigned

### Developer worker

Use for implementation across app code, cloud code, and configuration.

Expected output:
- changed files
- why each change was required
- test seams added
- blockers or assumptions
- release-enablement items if the feature depends on unavailable tooling

Default ownership:
- feature source files
- cloud functions
- config touched by the feature

### Unit test worker

Use for unit tests, mocks, fixtures, and coverage enforcement.

Expected output:
- changed test files
- coverage result
- failed cases
- missing seams or deterministic gaps

Default ownership:
- `tests/unit`
- unit fixtures
- coverage config if needed

### E2E QA worker

Use for critical-path automation and acceptance evidence.

Expected output:
- changed E2E scripts
- screenshots or logs
- repro steps for failures
- release risk summary
- degraded mode note if E2E had to fall back to simulate or unit-only evidence

Default ownership:
- `tests/e2e`
- QA fixtures
- artifact directories

### Release owner

Use for preview, upload, deploy, and release observation. This is usually the PM or orchestrator if the team does not define a separate role.

Expected output:
- release mode used
- version string
- artifact paths
- logs
- observation notes
- rollback target

## Use Safe Handoff Rules

Keep the normal handoff chain:
1. PM to developer
2. Developer to unit test and E2E QA
3. Unit test and E2E QA back to PM or release owner
4. PM to release owner or human approver

Each handoff must state:
- what changed
- what passed
- what failed
- what remains blocked
- whether the run degraded to a fallback path
- whether `feature delivery` and `release enablement` differ
- who owns the next action

Never hand off only a diff. Always include a short decision-oriented summary.

## Keep Write Boundaries Clean

- One writer per file.
- Many readers, one integrator.
- If overlap appears after delegation, stop the parallel write and reintegrate locally.
- Do not let PM, unit, and E2E workers rewrite feature files owned by the developer.

## Handle Incomplete Environments

If release or E2E prerequisites are missing:
- complete the safe parts of the workflow
- produce the exact blocker list
- state the allowed downgrade path
- return the next human or system action needed

Do not fake preview, upload, or acceptance completion.
