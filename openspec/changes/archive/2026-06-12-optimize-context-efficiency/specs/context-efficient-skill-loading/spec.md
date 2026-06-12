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

### Requirement: Reference guidance is disclosed progressively
The skills SHALL direct agents to identify an unresolved decision, locate the smallest relevant reference section, distill its actionable rules, and expand context only when a new risk or evidence gap appears.

#### Scenario: A reference contains several unrelated sections
- **WHEN** one section answers the current implementation or acceptance decision
- **THEN** the agent reads that section first instead of loading the full reference by default

#### Scenario: Release-critical work needs several references
- **WHEN** workflow, tooling, contracts, and framework guidance are all required
- **THEN** the agent loads them sequentially as their decisions become active without omitting required gates

### Requirement: Core safety remains always loaded
Entrypoint compression MUST retain profile escalation, evidence truthfulness, secret handling, release downgrade, UI runtime proof, and native-component layering requirements.

#### Scenario: Detailed references are not yet loaded
- **WHEN** an agent has loaded only the skill entrypoint
- **THEN** it still knows not to claim unverified release success or close UI work without runtime evidence

### Requirement: Delivery effectiveness takes precedence over context reduction
Context budgets SHALL act as upper bounds against unnecessary growth, not as targets that override comprehension, risk detection, or acceptance quality.

#### Scenario: A smaller entrypoint weakens task outcomes
- **WHEN** behavior evals or representative task regression reveal weaker routing, safety, or acceptance behavior after compression
- **THEN** maintainers restore the necessary instruction or improve its reference route even when context usage increases
