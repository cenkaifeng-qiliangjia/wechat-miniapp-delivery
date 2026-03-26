# Tooling And Risk Checklists

Use this reference during preflight, validation, and release.

## Run The Environment Doctor First

| Surface | Minimum requirement | Why it matters | Safe fallback |
| --- | --- | --- | --- |
| `miniprogram-ci` | Node `>=16.1.0` | Preview, upload, and npm build automation | Stop release work or keep the task in `plan` / `implement` / `validate` only |
| CloudBase MCP | Node `>=18.15.0` | Direct cloud operations from the agent | Switch to CloudBase CLI with the same env target |
| `minium` | Python `>=3.8` | Python-based E2E automation | Use `miniprogram-simulate` or JS E2E instead |
| DevTools automation | Available runner, port, and account session | Stable E2E and preview automation | Restrict to unit plus simulate evidence |

If any required surface is missing, record:
- the blocker
- the downgraded path
- the exact next setup step

## Detect The Project Shape

Use the repo layout to classify the project:

| Project type | Common signals | Typical release path |
| --- | --- | --- |
| Native WeChat mini program | `app.json`, `project.config.json`, page folders under a miniapp root | `miniprogram-ci` |
| Taro 3 miniapp | `@tarojs/*` on `^3.x`, Taro config, `src/app.config.*`, build output such as `dist/weapp` | `@tarojs/plugin-mini-ci` or `miniprogram-ci` |
| Taro 4 React miniapp | `@tarojs/*` on `^4.x`, `defineConfig` from `@tarojs/cli`, `defineAppConfig`, `framework: "react"`, `compiler.type: "webpack5"` | `@tarojs/plugin-mini-ci` or `miniprogram-ci` |
| uni-app targeting WeChat | `pages.json`, `manifest.json`, uni build scripts | framework build plus `miniprogram-ci` fallback |

If the classification is ambiguous, stop and inspect the build scripts before editing release logic.

## Taro 4 Specific Preflight

When the repo is Taro 4 with React, verify these before editing or releasing:
- `compiler.type` matches the expected build pipeline, typically `webpack5`
- `mini.compile.include` covers any workspace source packages that must be compiled into the miniapp build
- `compiler.prebundle.enable` is disabled when the repo consumes unbuilt workspace packages as source
- `project.config.json` has a valid generic app config and its `miniprogramRoot` points at the real Taro output directory
- `@tarojs/plugin-platform-weapp` or the repo-standard Taro WeChat plugin path is present when the build expects it

## Map Capability Modules Early

| Capability module | Turn it on when | Preferred path | Standard fallback | Must return |
| --- | --- | --- | --- | --- |
| `weapp_ci_release` | Preview, upload, or build automation is required | `miniprogram-ci` or repo-standard wrapper | Preview-only or release-blocked | mode, artifacts, logs, degraded flag |
| `weapp_test_automation` | Deterministic unit or E2E evidence is required | `miniprogram-simulate` plus repo runner, then `miniprogram-automator` or `minium` | Unit-only or simulate-only | coverage or flow evidence, residual risk |
| `cloudbase_env_deploy` | Cloud functions, hosting, indexes, or env wiring changed | CloudBase MCP | CloudBase CLI | env ID, actions, logs, rollback note |
| `security_compliance_gate` | Any real release, privacy, payment, or secret handling is in scope | `gitleaks` plus `trufflehog` plus rule checks | Warning-only on low confidence, block high risk | blockers, warnings, artifacts |

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
- privacy declarations and `usePrivacyCheck` or equivalent guard if privacy APIs are involved
- payment callback handling path if payment or refund flows are touched

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
- Taro 4 build: `pnpm taro build --type weapp` or the repo-standard Taro build script
- Taro 4 typecheck: `pnpm tsc --noEmit` or the repo-standard typecheck script
- Taro 4 tests: `pnpm test` or the repo-standard unit runner
- Taro 4 monorepo package build: `pnpm --filter <shared-package> build` before miniapp build when shared packages are prebuilt artifacts
- Unit tests: `miniprogram-simulate` with the repo's test runner
- E2E: `miniprogram-automator` or `minium`
- Observability: RUM or Sentry
- Secrets scan: `gitleaks` plus `trufflehog`
- Cloud backend: CloudBase where the project already uses it

## Run The Mandatory Quality Gates

### Static and formatting gate

- lint
- formatter
- obvious dead-code or config drift checks

### Security and compliance gate

- `gitleaks`
- `trufflehog`
- privacy declaration alignment
- `usePrivacyCheck` or equivalent consent gate when privacy APIs are used
- open API or CloudBase permission checks
- payment callback rule scan for signature verification, `5s` ack, idempotency, query fallback, and AES-256-GCM handling
- high-risk pattern scan for secrets in client code or missing callbacks

### Unit gate

- test changed components and shared logic first
- keep or set a line coverage threshold
- default to `0.75` line coverage for changed logic if the repo has no threshold

### E2E gate

- cover the top 1-3 user flows that prove the change works
- use stable selectors
- collect screenshots, logs, and failure evidence

### Release watch gate

- verify the current observability provider can identify the candidate release
- add or reuse a release tag for RUM, Sentry, or the repo-standard system
- keep watch notes and rollback trigger conditions with the release summary

### Acceptance gate

- map each acceptance criterion to proof
- mark any unmet criterion explicitly
- recommend `go`, `no-go`, or `needs-review`

## Apply Extra Checks For High-Risk Modules

| Risk module | Required extra checks |
| --- | --- |
| Payment | Callback verification, `5s` acknowledgement, retry awareness, idempotency, reconciliation or query fallback, AES-256-GCM decryption, no secrets in client code |
| Privacy or personal data | Declaration alignment, `usePrivacyCheck` or equivalent gate, consent flow, data minimization, no hidden collection path |
| Location or maps | Key management, legal domains, cost or license review, permission messaging |
| Auth or login | Token storage path, session expiry behavior, error-state handling, no sensitive logs |
| AI or model calls | Cost limits, quota handling, latency fallback, moderation or safety hooks where needed |
| CloudBase or open API | `config.json` permissions, env targeting, backend-only secrets, retry behavior |
| Cross-platform shared code | No direct `Taro`, `wx`, or `uni` API imports in shared packages, adapter boundary stays at the app edge |
| Monorepo dependency resolution | `mini.compile.include` is complete, circular dependencies are absent or understood, prebundle mode matches package build strategy |

## Downgrade Matrix

| Problem | Downgrade path | Report format |
| --- | --- | --- |
| Upload blocked by auth or network | Preview-only if possible, otherwise release-blocked | blocker, attempted mode, next setup step |
| E2E runner or DevTools unstable | Unit-only or simulate-only | degraded flag, residual risk, missing evidence |
| CloudBase MCP unavailable | CloudBase CLI | channel switched, env ID, action log |
| Compliance signal ambiguous | Block high-risk release, continue low-risk implementation only | blockers, warnings, remediation list |
| Observability missing | Do not mark `publish-ready` | waiver needed, monitoring gap |

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
