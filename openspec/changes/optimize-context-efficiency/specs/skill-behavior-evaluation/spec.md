## MODIFIED Requirements

### Requirement: Eval cases cover realistic regressions
The eval suite MUST include UI alignment, dynamic layout stability, overlay layering, release downgrade, task proportionality, negative-trigger scenarios, and context-loading expectations.

#### Scenario: Button alignment regression
- **WHEN** the eval suite is run
- **THEN** at least one case requires shared button reset review, vertical centering, rendered runtime evidence, and avoids unrelated release references

#### Scenario: Backend-only change
- **WHEN** a case describes a backend-only change without UI impact
- **THEN** the expected skills do not include the design skill

#### Scenario: Release-critical change
- **WHEN** a case requests high-risk release work
- **THEN** the expected concepts include the detailed workflow and tooling references required for evidence and rollback
