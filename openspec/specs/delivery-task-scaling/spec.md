# delivery-task-scaling Specification

## Purpose
Define proportional quick, standard, and release-critical workflows for WeChat miniapp delivery tasks.
## Requirements
### Requirement: Delivery work selects a proportional profile
The delivery skill SHALL select exactly one of `quick`, `standard`, or `release-critical` before choosing roles and artifacts.

#### Scenario: Local one-file correction
- **WHEN** a change is local, low-risk, does not alter an API contract, and does not request preview or release
- **THEN** the skill selects `quick` and avoids full PM and multi-role ceremony

#### Scenario: Feature-sized implementation
- **WHEN** a change spans multiple files or requires functional, visual, contract, or E2E acceptance without high-risk release work
- **THEN** the skill selects `standard`

#### Scenario: High-risk or release operation
- **WHEN** a change touches payment, privacy, authentication, production data, publish or upload actions, privileged credentials, or rollback-sensitive infrastructure
- **THEN** the skill selects `release-critical`

### Requirement: Risk can only increase workflow rigor
The delivery skill MUST escalate the selected profile when release intent, affected systems, or discovered risks require stronger gates.

#### Scenario: Quick task discovers a shared API change
- **WHEN** implementation reveals that a local UI fix changes a shared request or response contract
- **THEN** the profile escalates from `quick` to at least `standard`

### Requirement: Each profile has explicit exit evidence
The delivery skill SHALL define the minimum artifacts and validation evidence required to close each profile.

#### Scenario: Quick task completion
- **WHEN** a quick task is ready to close
- **THEN** it includes changed files, focused validation, residual risk, and any relevant runtime UI proof without requiring unrelated release artifacts
