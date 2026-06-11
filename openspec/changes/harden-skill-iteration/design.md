## Context

The repository distributes two text-first skills and a small set of Python installation and validation utilities. The skills already encode detailed delivery and UI runtime gates, but workflow proportionality, project-specific design adaptation, behavioral evaluation, and installer safety are not enforced consistently. The repository has two synchronized identities, so changes must remain portable while allowing repository address metadata to differ.

## Goals / Non-Goals

**Goals:**
- Make significant skill changes traceable from proposal through verified implementation.
- Keep small delivery tasks lightweight while preserving full gates for high-risk release work.
- Prevent generic design defaults from overriding established project conventions.
- Add deterministic behavior-contract evals that run in CI without model credentials.
- Make remote installation defensive and failure-safe.

**Non-Goals:**
- Build a model-scoring platform or depend on a hosted LLM in CI.
- Replace repository-specific tests in downstream miniapp projects.
- Force an existing miniapp to migrate its design tokens or styling framework.
- Make primary and fork Git histories identical.

## Decisions

### Track OpenSpec artifacts at repository level

Significant changes SHALL use tracked `openspec/changes/` artifacts and archive completed specifications into `openspec/specs/`. Skill folders remain limited to runtime instructions and bundled resources.

Alternative considered: document the process only in README. Rejected because it cannot validate requirements or preserve capability history.

### Use three proportional delivery profiles

The delivery skill will select `quick`, `standard`, or `release-critical` before orchestration. Risk and release intent can only increase the profile. Each profile has explicit required artifacts and exit criteria.

Alternative considered: infer proportionality informally. Rejected because recent small tasks can still trigger the full role workflow.

### Reuse existing design systems before fallback guidance

The design skill will inspect project tokens, component primitives, units, build conversion, and visual conventions first. Bundled token values and ratios become examples for projects without an established system, not universal requirements.

Alternative considered: keep one strict default system. Rejected because it creates unrelated migrations and can conflict with framework configuration.

### Store behavior evals as declarative JSON

`evals/cases.json` will describe prompts, expected skill selection, workflow profile, required concepts, and forbidden concepts. `scripts/run_skill_evals.py` will verify that skill instructions contain enforceable guidance for those cases. This is a deterministic contract suite; live forward-tests remain a separate release activity.

Alternative considered: call hosted models in CI. Rejected because credentials, cost, nondeterminism, and private prompt handling would make baseline validation fragile.

### Harden installation with standard-library primitives

The remote installer will validate `owner/repo`, apply network timeouts, reject unsafe ZIP members, copy into staging directories, and atomically replace destinations only after all selected skill sources are validated.

Alternative considered: add a third-party installer library. Rejected because the script is intentionally pipe-executable and dependency-free.

## Risks / Trade-offs

- Deterministic evals prove instruction coverage, not model compliance. → Keep realistic cases and require periodic forward-testing for significant releases.
- OpenSpec adds repository files and maintenance steps. → Validate only significant changes and keep the core profile.
- Atomic replacement cannot make multiple target roots one filesystem transaction. → Validate all sources first, stage per target, and restore the previous destination on replacement failure.
- Existing users may rely on the current broad design defaults. → Preserve examples while clearly marking them as fallback guidance.

## Migration Plan

1. Add and validate the OpenSpec change.
2. Update skill guidance, behavior evals, and repository CI.
3. Release the first-round skill content changes to primary and fork.
4. Harden installers and add installer tests.
5. Verify both repositories, archive the OpenSpec change, and release final versions.

Rollback is a normal Git revert of the corresponding round. Existing installed skills remain usable because no folder names or entrypoint formats change.

## Open Questions

None. Live model forward-testing can be expanded later without changing the declarative eval schema.
