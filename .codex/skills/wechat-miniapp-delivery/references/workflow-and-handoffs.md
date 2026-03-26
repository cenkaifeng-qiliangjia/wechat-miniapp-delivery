# Workflow And Handoffs

Use this reference when the task spans more than one stage or when you need worker coordination.

## Ground The Task In Concrete Use Cases

Use one or more of these starting frames:
- Implement a feature and ship a preview build.
- Harden a release candidate before upload.
- Fix a high-risk bug and decide go or no-go.

If the current task does not fit one of these frames, write a new one-sentence use case before assigning work.

## Run The Seven Delivery Stages

| Stage | Primary owner | Goal | Exit artifact |
| --- | --- | --- | --- |
| Intake and plan | PM | Convert the request into a scoped delivery plan | Plan JSON, acceptance matrix, risk list |
| Preflight | PM plus developer | Confirm framework, build, release, and environment prerequisites | Preflight report with blockers |
| Implementation | Developer | Change code, config, cloud resources, and test seams | Change summary and owned file list |
| Static and compliance gates | Developer or orchestrator | Catch formatting, secrets, privacy, and permission issues | Gate summary with pass or fail |
| Unit gate | Unit test | Prove changed logic is deterministic and covered | Coverage and failure report |
| E2E and acceptance | E2E QA plus PM | Verify the main user path and gather acceptance evidence | Evidence pack and go or no-go recommendation |
| Release and watch | PM | Produce preview or upload evidence and prepare rollback | Release summary, observation notes, rollback target |

Use a sequential workflow for the main path and an iterative refinement loop after validation:
1. PM plans.
2. Developer implements.
3. Unit and E2E validate.
4. Orchestrator or developer fixes.
5. PM closes the loop.

## Build A Worker Context Pack

Give each worker the minimum context needed to succeed:
- Goal: what done looks like
- Non-goals: what not to touch
- Owned paths: files or directories they may change
- Inputs: requirement, plan slice, acceptance criteria, risk modules
- Success check: tests, artifacts, or gate result expected
- Required output: changed files, evidence, blockers, next owner

If you cannot give a worker a clear write boundary, keep the work local instead of parallelizing it.

## Assign Role Contracts

### PM worker

Use for planning, release coordination, and go or no-go decisions.

Expected output:
- plan summary
- acceptance matrix
- risk register
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

Default ownership:
- `tests/e2e`
- QA fixtures
- artifact directories

## Use Safe Handoff Rules

Keep the normal handoff chain:
1. PM to developer
2. Developer to unit test and E2E QA
3. Unit test and E2E QA back to PM
4. PM to release owner

Each handoff must state:
- what changed
- what passed
- what failed
- what remains blocked
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
- return the next human or system action needed

Do not fake preview, upload, or acceptance completion.
