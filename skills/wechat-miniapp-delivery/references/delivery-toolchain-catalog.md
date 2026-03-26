# Delivery Toolchain Catalog

Use this reference when choosing capability modules, checking environment floors, or deciding how to downgrade safely.

## Capability Module Matrix

| Module | Turn it on when | Preferred path | Minimum environment | Safe fallback | Required evidence |
| --- | --- | --- | --- | --- | --- |
| `weapp_ci_release` | Preview, upload, or npm build automation is needed | `miniprogram-ci` or repo-standard wrapper | Node `>=16.1.0` | Preview-only or release-blocked | mode, artifacts, logs, degraded flag |
| `weapp_test_automation` | Deterministic unit, API contract, functional, E2E, or performance proof is needed | `miniprogram-simulate` plus repo runner, then `miniprogram-automator` or `minium`, plus repo acceptance artifacts | Node for JS runners, Python `>=3.8` for `minium` | Unit-only or simulate-only | coverage, contract, acceptance, or flow evidence plus residual risk |
| `cloudbase_env_deploy` | Cloud functions, hosting, indexes, or env wiring changed | CloudBase MCP | Node `>=18.15.0` | CloudBase CLI | env ID, action log, rollback note |
| `security_compliance_gate` | Secrets, privacy, payment, or release-readiness risk is in scope | `gitleaks` plus `trufflehog` plus rule checks | CLI availability plus repo access | Warning-only for low confidence, block high risk | blockers, warnings, artifacts |

## `weapp_ci_release`

Use for `build_npm`, `preview`, `upload`, or `full_release`.

Input fragment:

```json
{
  "module": "weapp_ci_release",
  "action": "preview|upload|full_release",
  "project_path": "./dist/weapp",
  "appid": "wx1234567890",
  "private_key_path": "./secrets/upload.pem",
  "robot": 1,
  "version": "1.2.3"
}
```

Output fragment:

```json
{
  "ok": true,
  "mode": "preview",
  "degraded": false,
  "artifacts": ["./artifacts/preview.png"],
  "issues": []
}
```

Downgrade policy:
- auth or network failure during upload: retry if safe, then downgrade to `preview-only`
- missing key, app ID, or build output: block release work and return setup steps

## `weapp_test_automation`

Use for unit, API contract, simulate, functional, E2E, or performance evidence.

Input fragment:

```json
{
  "module": "weapp_test_automation",
  "mode": "unit|api-contract|functional|e2e|performance|unit+api-contract+e2e",
  "unit_runner": "jest",
  "e2e_runner": "miniprogram-automator|minium",
  "flows": ["order-list-filter"]
}
```

Output fragment:

```json
{
  "ok": true,
  "mode": "unit+api-contract+e2e",
  "degraded": false,
  "coverage": {
    "lines": 0.82
  },
  "contract_surfaces": ["api/order/list"],
  "artifacts": ["./artifacts/e2e/order-list-filter.png"],
  "issues": []
}
```

Downgrade policy:
- DevTools, port, or runner instability: degrade to `unit-only` or `simulate-only`
- missing stable selectors: report as implementation debt, do not silently skip the flow

## `cloudbase_env_deploy`

Use for CloudBase environment setup, function deploys, hosting deploys, indexes, or logs.

Input fragment:

```json
{
  "module": "cloudbase_env_deploy",
  "channel": "mcp|cli",
  "env_id": "prod-1234",
  "actions": ["functions", "hosting"],
  "artifact_root": "./artifacts/cloudbase"
}
```

Output fragment:

```json
{
  "ok": true,
  "channel": "cli",
  "env_id": "prod-1234",
  "actions": ["functions"],
  "artifacts": ["./artifacts/cloudbase/deploy.log"],
  "issues": []
}
```

Downgrade policy:
- CloudBase MCP unavailable or version floor not met: switch to CloudBase CLI
- missing env ID or auth: block deploy work and keep feature delivery separate

## `security_compliance_gate`

Use for every real release candidate and for any change touching payment, privacy, auth, or backend secrets.

Input fragment:

```json
{
  "module": "security_compliance_gate",
  "secret_scan": true,
  "privacy_check": true,
  "payment_check": true,
  "observability_check": true
}
```

Output fragment:

```json
{
  "ok": true,
  "blockers": [],
  "warnings": [],
  "artifacts": ["./artifacts/security/gitleaks.json"]
}
```

High-risk blockers:
- secrets committed to repo or client bundle
- payment callback missing signature verification, `5s` acknowledgement, idempotency, query fallback, or AES-256-GCM handling
- privacy declaration or consent path missing for privacy APIs

Low-confidence findings can remain warnings, but high-risk blockers should stop release work.

## Portability And Packaging Notes

- Keep the canonical source in `skills/wechat-miniapp-delivery`.
- Treat `.codex/skills/wechat-miniapp-delivery` and `.claude/skills/wechat-miniapp-delivery` as generated mirrors.
- Keep semantic content identical across agents; only UI metadata should differ.
- For GitHub-based installation, the canonical repo path is `skills/wechat-miniapp-delivery`.

## Common Module Bundles

- Feature delivery with preview: `weapp_test_automation` + `security_compliance_gate` + `weapp_ci_release`
- CloudBase-backed feature: `weapp_test_automation` + `cloudbase_env_deploy` + `security_compliance_gate`
- Release-readiness audit: all four modules
- Acceptance-heavy change: `weapp_test_automation` plus explicit functional, E2E, and performance evidence packs
