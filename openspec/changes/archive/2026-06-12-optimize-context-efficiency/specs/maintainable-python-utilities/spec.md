## ADDED Requirements

### Requirement: Python orchestration uses single-purpose helpers
Repository Python scripts SHALL separate input parsing, validation, transformation, execution, and result reporting when a function would otherwise coordinate several responsibilities.

#### Scenario: Behavior eval execution
- **WHEN** the eval runner validates multiple cases
- **THEN** schema checks, per-case checks, concept checks, and reporting are implemented by distinct helpers

### Requirement: Function size is bounded
Repository validation SHALL reject Python functions longer than 45 source lines unless a documented exception is added to the validator.

#### Scenario: New orchestration logic exceeds the limit
- **WHEN** a Python function grows beyond 45 lines
- **THEN** validation fails before merge

### Requirement: Public script behavior remains stable
Refactoring MUST preserve existing command-line arguments, success output, error semantics, and installer safety behavior.

#### Scenario: Installer tests run after refactoring
- **WHEN** the Python utilities are decomposed
- **THEN** all installer unit tests and remote installation smoke tests continue to pass
