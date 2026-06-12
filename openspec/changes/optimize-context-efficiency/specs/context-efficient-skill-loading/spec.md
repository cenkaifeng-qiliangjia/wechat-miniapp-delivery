## ADDED Requirements

### Requirement: Skill entrypoints have effect-preserving budgets
The repository SHALL keep the delivery entrypoint at or below 2,200 words and 300 lines and the design entrypoint at or below 1,500 words and 230 lines.

#### Scenario: Entry point grows beyond its budget
- **WHEN** a change pushes either entrypoint beyond its configured word or line budget
- **THEN** repository validation fails and directs detailed material into a reference

### Requirement: References load only for relevant triggers
Each skill SHALL map task conditions to the smallest set of references needed to complete the work safely.

#### Scenario: Quick local button fix
- **WHEN** a task only fixes button alignment in one component family
- **THEN** the agent loads runtime UI quality guidance without loading release tooling, framework catalogs, or full handoff examples

#### Scenario: Release-critical payment change
- **WHEN** a task includes payment and preview or upload work
- **THEN** the agent loads tooling, risk, contracts, and workflow references needed for release evidence and rollback

### Requirement: Core safety remains always loaded
Entrypoint compression MUST retain profile escalation, evidence truthfulness, secret handling, release downgrade, UI runtime proof, and native-component layering requirements.

#### Scenario: Detailed references are not yet loaded
- **WHEN** an agent has loaded only the skill entrypoint
- **THEN** it still knows not to claim unverified release success or close UI work without runtime evidence
