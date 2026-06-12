## Why

The skills now enforce the right delivery behavior, but their always-loaded entrypoints repeat details already available in references. This increases context cost on routine tasks, while several Python orchestration functions have grown large enough to make safe maintenance slower.

## What Changes

- Add effect-preserving context budgets for both skill entrypoints.
- Treat those budgets as ceilings; behavior and acceptance quality override further token reduction.
- Keep profile selection, safety invariants, and reference routing in `SKILL.md`; move detailed catalogs, role contracts, examples, and fallback design values to conditional references.
- Add explicit reference-loading rules so quick tasks do not load release, framework, or example material they do not need.
- Load relevant reference sections progressively as unresolved decisions and evidence gaps appear.
- Add repository validation for entrypoint word and line budgets plus required behavioral markers.
- Split large Python orchestration functions into single-purpose validation, parsing, and execution helpers without changing CLI behavior.
- Preserve existing behavior evals, installer tests, and OpenSpec requirements as regression gates.

## Capabilities

### New Capabilities

- `context-efficient-skill-loading`: Effect-preserving context budgets and conditional reference loading for distributed skills.
- `maintainable-python-utilities`: Single-purpose function boundaries and complexity budgets for repository Python utilities.

### Modified Capabilities

- `skill-behavior-evaluation`: Behavior validation must continue to pass when required guidance moves from an entrypoint into a directly routed reference.

## Impact

- Affects both `SKILL.md` entrypoints, selected references, behavior eval mapping, repository validation, Python utility structure, catalog versions, and CI tests.
- Does not change skill names, installer CLI flags, repository identity, or supported delivery capabilities.
