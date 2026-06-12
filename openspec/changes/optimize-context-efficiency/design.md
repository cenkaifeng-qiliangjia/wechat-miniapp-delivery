## Context

Codex and Claude load skill metadata first, then the complete `SKILL.md`, and only load references when directed. The delivery entrypoint is about 3,100 words and the design entrypoint about 2,200 words. Both are below the hard 5,000-word guidance, but significant portions describe details that are only relevant to release-critical, framework-specific, or design-bootstrap tasks.

The Python utilities are dependency-free and intentionally support pipe execution. Refactoring must therefore keep remote installer logic self-contained.

## Goals / Non-Goals

**Goals:**
- Reduce always-loaded skill text without weakening safety or acceptance behavior.
- Make reference loading conditional and easy for an agent to choose correctly.
- Keep quick UI fixes effective while avoiding unrelated release and architecture context.
- Split Python orchestration into small, testable functions.

**Non-Goals:**
- Minimize tokens at the expense of missing required gates.
- Remove detailed references or realistic examples.
- Introduce shared Python modules required by the pipe-executed remote installer.
- Change public CLI behavior.

## Decisions

### Budget entrypoints, not the full knowledge base

The delivery entrypoint will target at most 2,200 words and 300 lines. The design entrypoint will target at most 1,500 words and 230 lines. Detailed knowledge remains available in one-level references.

### Route references by trigger

Each entrypoint will include a compact loading table. Quick work loads only the directly relevant acceptance reference. Standard and release-critical work load contracts, orchestration, tooling, or framework references only when their trigger is present.

### Preserve non-negotiable behavior in entrypoints

Profile escalation, evidence requirements, secret safety, release truthfulness, UI runtime proof, and native-layer risk remain in always-loaded text.

### Move fallback design values to a bootstrap reference

Example colors, spacing, typography, radius, shadows, and component variants are useful only when the repository lacks a design system. They will move to `references/design-system-bootstrap.md`.

### Refactor functions without cross-script coupling

Large functions will be decomposed within their existing script. The remote installer remains a single-file executable. Repository validation will enforce a soft maximum of 45 lines per function, with narrow exceptions avoided where practical.

## Risks / Trade-offs

- Agents may fail to load a needed reference. → Use explicit trigger-to-reference tables and behavior markers.
- Word budgets may encourage terse but ambiguous wording. → Validate behavior contracts and keep safety invariants in entrypoints.
- Function-line metrics are imperfect. → Treat them as maintainability guardrails alongside tests, not as a quality score.

## Migration Plan

1. Refactor Python functions with tests unchanged.
2. Move conditional skill details to references and add loading maps.
3. Add token and function-size validation.
4. Run all behavior, installation, OpenSpec, and sync checks.
5. Archive this change after both repositories pass CI.
