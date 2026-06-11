# skill-behavior-evaluation Specification

## Purpose
Define deterministic behavior-contract evals that protect skill triggering, workflow proportionality, and required guardrails.
## Requirements
### Requirement: Behavior eval cases are declarative
The repository SHALL store skill behavior cases in a machine-readable file with a unique identifier, prompt, expected skills, expected workflow profile, required concepts, and forbidden concepts.

#### Scenario: New regression case
- **WHEN** maintainers discover a repeated skill failure
- **THEN** they can add a case without modifying the eval runner

### Requirement: Eval cases cover realistic regressions
The eval suite MUST include UI alignment, dynamic layout stability, overlay layering, release downgrade, task proportionality, and negative-trigger scenarios.

#### Scenario: Button alignment regression
- **WHEN** the eval suite is run
- **THEN** at least one case requires shared button reset review, vertical centering, and rendered runtime evidence

#### Scenario: Backend-only change
- **WHEN** a case describes a backend-only change without UI impact
- **THEN** the expected skills do not include the design skill

### Requirement: CI rejects stale eval contracts
Repository validation SHALL fail when eval schema is invalid, identifiers are duplicated, referenced skills are unknown, or required profile guidance is absent from the skill.

#### Scenario: Unknown workflow profile
- **WHEN** an eval case names a profile outside the supported profile set
- **THEN** CI fails with the case identifier and invalid value
