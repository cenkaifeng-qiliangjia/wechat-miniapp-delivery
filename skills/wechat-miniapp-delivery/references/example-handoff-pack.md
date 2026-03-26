# Example Handoff Pack

Use this reference when the request is feature-sized and you want a concrete example of how to hand work across PM, developer, unit-test, and E2E roles.

## Example Request

Add status filtering and pull-to-refresh to the order list page, then prepare the change for preview release.

## PM Intake Pack

### Plan JSON

```json
{
  "summary": {
    "decision": "needs-review",
    "stage": "plan"
  },
  "env_doctor": {
    "status": "pass",
    "issues": [],
    "downgrade_plan": []
  },
  "architecture_decisions": [
    {
      "topic": "release_tool",
      "choice": "miniprogram-ci",
      "reason": "Native miniapp project with preview requirement"
    },
    {
      "topic": "observability",
      "choice": "reuse existing provider",
      "reason": "No new provider should be introduced for this feature"
    }
  ],
  "capability_plan": [
    {
      "name": "weapp_test_automation",
      "action": "unit+e2e",
      "fallback": "unit-only"
    },
    {
      "name": "security_compliance_gate",
      "action": "full",
      "fallback": "block-high-risk"
    },
    {
      "name": "weapp_ci_release",
      "action": "preview",
      "fallback": "preview-only"
    }
  ],
  "task_graph": [
    {
      "id": "T1",
      "owner": "developer",
      "scope": "order list page, filter UI, refresh behavior",
      "acceptance": "User can filter by status and refresh the list"
    },
    {
      "id": "T2",
      "owner": "unit",
      "scope": "filter mapping, refresh state, list rendering edge cases",
      "acceptance": "Changed logic is covered with deterministic tests"
    },
    {
      "id": "T3",
      "owner": "e2e",
      "scope": "order list filter flow and refresh flow",
      "acceptance": "Critical user path passes in automation"
    },
    {
      "id": "T4",
      "owner": "pm",
      "scope": "preview readiness and release evidence",
      "acceptance": "Preview blockers and release prerequisites are explicit"
    }
  ],
  "delivery_split": {
    "feature_delivery": "in_scope",
    "release_enablement": "preview-in-scope upload-out-of-scope"
  },
  "handoff": {
    "owner": "developer",
    "next_action": "implement_change",
    "artifacts": [
      "plan_json",
      "acceptance_matrix",
      "risk_list",
      "env_doctor"
    ]
  }
}
```

### Acceptance Matrix

| Criterion | Proof needed | Owner |
| --- | --- | --- |
| Filter options match supported order states | UI diff or code evidence plus unit test | Developer and unit |
| Changing the filter updates the list correctly | Unit test plus E2E evidence | Unit and E2E |
| Pull-to-refresh keeps the selected filter and refreshes data | Unit test plus manual or E2E evidence | Developer, unit, E2E |
| Preview release can be attempted safely | Preflight or release report with blockers or success evidence | PM |
| Upload can stay blocked if preview succeeds but permissions are incomplete | Explicit release-enable status with blocker | PM |

### Risk List

- Upload robot permission may be missing even if preview works.
- Existing list selectors may be unstable for E2E.
- Order status mapping may be duplicated in UI and API layers.

### Preflight Notes

- `miniprogram-ci` and preview credentials are present.
- Upload robot permission is not enabled yet, so preview is allowed but upload is blocked.
- Existing RUM provider is available and should receive the preview tag.

## Developer Handoff

Give the developer:
- Goal: implement filter UI, filtered fetch behavior, refresh behavior, and stable selectors.
- Non-goals: no payment, no unrelated list redesign, no new observability provider.
- Owned paths:
  - order list page files
  - related API or data mapping files
  - config touched by selectors or release-safe behavior
- Success check:
  - filter and refresh work locally
  - stable selectors exist for E2E
  - changed files are summarized

Expected output:
- changed files list
- assumptions about order status source
- new selectors or test seams
- blockers for preview or upload readiness

## Unit-Test Handoff

Give the unit-test worker:
- Goal: cover filter mapping, empty-state behavior, refresh state transitions, and selected-filter persistence.
- Non-goals: do not rewrite feature files.
- Owned paths:
  - `tests/unit`
  - fixtures or mocks used by those tests
- Success check:
  - changed logic covered
  - failing cases and missing seams reported clearly

Expected output:
- changed test files
- coverage result
- failed cases or missing seams

## E2E Handoff

Give the E2E worker:
- Goal: prove the user can open the list, change a filter, and refresh the list without losing state.
- Non-goals: do not cover unrelated order detail flows in the same pass.
- Owned paths:
  - `tests/e2e`
  - QA fixtures
  - screenshots or logs
- Success check:
  - critical flow script exists
  - screenshots or logs exist for pass or fail

Expected output:
- changed E2E files
- artifact paths
- exact failure point if the flow fails

## PM Closeout Pack

Use this summary when all workers return:

```json
{
  "summary": {
    "decision": "needs-review",
    "stage": "release_candidate"
  },
  "feature_delivery": {
    "status": "pass",
    "notes": [
      "Filter UI, refresh logic, and stable selectors are implemented"
    ]
  },
  "release_enablement": {
    "status": "needs-review",
    "notes": [
      "Preview passed",
      "Upload remains blocked by missing robot permission"
    ]
  },
  "validations": {
    "preflight": {
      "ok": true,
      "issues": [
        "upload robot permission missing"
      ]
    },
    "unit": {
      "ok": true,
      "coverage": {
        "lines": 0.83
      },
      "artifacts": []
    },
    "e2e": {
      "ok": true,
      "failed_flows": [],
      "artifacts": [
        "./artifacts/e2e/order-list-filter.png"
      ]
    },
    "release": {
      "ok": true,
      "mode": "preview",
      "version": "1.2.3",
      "qrcode_path": "./artifacts/preview.png"
    }
  },
  "tool_runs": {
    "weapp_ci_release": {
      "ok": true,
      "mode": "preview",
      "degraded": true,
      "issues": [
        "upload skipped: robot permission missing"
      ]
    }
  },
  "release_evidence": {
    "version": "1.2.3",
    "mode": "preview",
    "artifact_paths": [
      "./artifacts/preview.png"
    ],
    "observation_notes": [
      "RUM preview tag set to 1.2.3-preview"
    ]
  },
  "handoff": {
    "owner": "pm",
    "next_action": "enable_upload_robot_then_retry_upload",
    "artifacts": [
      "validation_summary",
      "e2e_artifacts",
      "release_blocker_list"
    ]
  },
  "rollback": {
    "available": true,
    "target_version": "current_production"
  }
}
```

If the project is hybrid or release tooling is incomplete, split the conclusion into:
- feature delivery status
- release-enablement status

Do not merge them into a fake overall pass.
