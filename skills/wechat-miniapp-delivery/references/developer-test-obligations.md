# Developer Test Obligations

Use this reference when the developer changes business logic, data-fetching layers, cloud functions, or user-visible flows. The developer is accountable for the first line of test acceptance, not just implementation.

## Cover Changed Logic With Unit Tests

Require unit coverage for changed:
- pure business functions
- hooks
- state stores
- formatters, mappers, and guards
- error-state transitions

Do not push obviously testable logic into E2E-only coverage.

## Treat Touched APIs As Contract Surfaces

When a feature touches an API, cloud function, or backend response shape, require the developer to verify:
- request parameters
- response schema assumptions
- empty or partial payload handling
- error-code mapping
- retry or idempotency behavior where relevant
- mock fixtures that match the current contract

If the repo has no formal contract tests, add the smallest deterministic check that protects the touched surface.

## Keep Fixtures Honest

- Update fixtures when request or response fields change.
- Keep example payloads close to the current contract.
- Do not let stale mocks become the reason tests stay green while production breaks.

## Hand Off Test Ownership Clearly

Developer output should include:
- changed API surfaces
- unit tests added or updated
- contract checks added or updated
- known gaps that still need QA or release-owner attention

If a touched interface cannot be tested deterministically, explain why and mark it as an explicit acceptance risk.
