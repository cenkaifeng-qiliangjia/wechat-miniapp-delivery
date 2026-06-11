## Why

The skill suite now has broad delivery coverage, but small fixes can trigger excessive ceremony, design defaults can override an existing product system, and repository validation checks structure rather than agent behavior. The remaining installer and iteration workflow also need deterministic safety so future changes stay reviewable and reproducible.

## What Changes

- Add an OpenSpec-based lifecycle for significant skill changes: propose, specify, design, task, verify, and archive.
- Add `quick`, `standard`, and `release-critical` delivery profiles with explicit entry and exit criteria.
- Make the design skill reuse the repository's existing design system first and treat bundled token values as fallback examples.
- Add declarative behavior eval cases for triggering, required behavior, forbidden behavior, and workflow proportionality.
- Extend repository validation and CI to validate eval structure and iteration artifacts.
- Harden GitHub installation with repository validation, safe archive extraction, network timeouts, and atomic destination replacement.
- Preserve separate repository identities while keeping primary and fork behavior synchronized.

## Capabilities

### New Capabilities

- `skill-iteration-governance`: Specification-first lifecycle, validation, and archive requirements for significant skill changes.
- `delivery-task-scaling`: Rules for selecting proportional quick, standard, or release-critical workflows.
- `adaptive-design-guidance`: Design guidance that preserves existing project systems and applies fallback defaults only when needed.
- `skill-behavior-evaluation`: Declarative scenarios that test triggering, required outputs, prohibited behavior, and workflow proportionality.
- `safe-skill-installation`: Deterministic and defensive GitHub archive installation behavior.

### Modified Capabilities

None.

## Impact

- Affects both skill entrypoints, design guidance, catalog versions, repository validation, CI, installer scripts, and maintenance documentation.
- Adds tracked `openspec/` specifications and change history at repository level, not inside distributed skill folders.
- Keeps Python 3.11 as the CI runtime and introduces no runtime dependency beyond the standard library.
