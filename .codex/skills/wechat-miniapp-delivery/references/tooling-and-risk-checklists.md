# Tooling And Risk Checklists

Use this reference during preflight, validation, and release.

## Detect The Project Shape

Use the repo layout to classify the project:

| Project type | Common signals | Typical release path |
| --- | --- | --- |
| Native WeChat mini program | `app.json`, `project.config.json`, page folders under a miniapp root | `miniprogram-ci` |
| Taro miniapp | `src/app.config.*`, Taro config, build output such as `dist/weapp` | `@tarojs/plugin-mini-ci` or `miniprogram-ci` |
| uni-app targeting WeChat | `pages.json`, `manifest.json`, uni build scripts | framework build plus `miniprogram-ci` fallback |

If the classification is ambiguous, stop and inspect the build scripts before editing release logic.

## Run Preflight Before Editing Or Releasing

Check the following first:
- app ID and main project config file
- build output path
- package manager and build command
- npm build expectations for miniapp packages
- legal request, upload, and download domains
- CloudBase env ID or backend environment
- release key path, robot ID, and allowlist assumptions
- DevTools automation readiness for E2E
- observability provider and release tagging path

High-value files to inspect early:
- `project.config.json`
- `project.private.config.json` if present and readable
- `package.json`
- framework build config
- `cloudfunctions/*/config.json`
- app config or routing config

## Prefer The P0 Tool Stack

Use these defaults unless the repo already standardized on an equivalent:
- Build and release: `miniprogram-ci`
- Taro release wrapper: `@tarojs/plugin-mini-ci`
- Unit tests: `miniprogram-simulate` with the repo's test runner
- E2E: `miniprogram-automator` or `minium`
- Observability: RUM or Sentry
- Secrets scan: `gitleaks` or `trufflehog`
- Cloud backend: CloudBase where the project already uses it

## Run The Mandatory Quality Gates

### Static and formatting gate

- lint
- formatter
- obvious dead-code or config drift checks

### Compliance gate

- secrets scan
- privacy declaration alignment
- open API or CloudBase permission checks
- high-risk pattern scan for payment, secrets in client code, or missing callbacks

### Unit gate

- test changed components and shared logic first
- keep or set a line coverage threshold
- default to `0.75` line coverage for changed logic if the repo has no threshold

### E2E gate

- cover the top 1-3 user flows that prove the change works
- use stable selectors
- collect screenshots, logs, and failure evidence

### Acceptance gate

- map each acceptance criterion to proof
- mark any unmet criterion explicitly
- recommend `go`, `no-go`, or `needs-review`

## Apply Extra Checks For High-Risk Modules

| Risk module | Required extra checks |
| --- | --- |
| Payment | Callback verification, idempotency, reconciliation or query fallback, no secrets in client code |
| Privacy or personal data | Declaration alignment, consent flow, data minimization, no hidden collection path |
| Location or maps | Key management, legal domains, cost or license review, permission messaging |
| Auth or login | Token storage path, session expiry behavior, error-state handling, no sensitive logs |
| AI or model calls | Cost limits, quota handling, latency fallback, moderation or safety hooks where needed |
| CloudBase or open API | `config.json` permissions, env targeting, backend-only secrets, retry behavior |

## Decide Release Readiness

Only call a change release-ready when all of the following are true:
- acceptance criteria have evidence
- blockers are empty or explicitly waived
- release prerequisites are present
- rollback target is known
- observability can identify the release

Expected release evidence:
- release mode used
- version string
- QR or build artifact path
- logs or command result
- rollback target
- observation notes

If preview or upload fails, classify the failure as one of:
- configuration
- permissions
- network
- build output mismatch
- tooling instability

Return the class with the exact next step instead of a generic failure message.
