## ADDED Requirements

### Requirement: Significant skill changes use OpenSpec
The repository SHALL track significant skill behavior, workflow, distribution, or validation changes through OpenSpec proposal, specification, design, tasks, verification, and archive artifacts.

#### Scenario: Significant workflow change
- **WHEN** a change modifies skill workflow profiles, acceptance gates, installation behavior, or evaluation contracts
- **THEN** the change includes a validated OpenSpec change before implementation is considered complete

### Requirement: Skill folders remain runtime-focused
The repository MUST keep process history and maintenance documentation outside distributed skill folders.

#### Scenario: Iteration documentation is added
- **WHEN** a maintainer records proposal, design, task, or release history
- **THEN** the artifact is stored under repository-level OpenSpec or README paths rather than inside a skill folder

### Requirement: Completed changes preserve capability history
The repository SHALL archive completed OpenSpec changes after implementation and verification succeed.

#### Scenario: All tasks and validations pass
- **WHEN** a change has no incomplete tasks and its strict OpenSpec validation passes
- **THEN** the change is archived and its capability specifications are available under `openspec/specs`
