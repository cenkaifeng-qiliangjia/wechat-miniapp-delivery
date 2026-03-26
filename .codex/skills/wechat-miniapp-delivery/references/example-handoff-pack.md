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
  "handoff": {
    "owner": "developer",
    "next_action": "implement_change",
    "artifacts": [
      "plan_json",
      "acceptance_matrix",
      "risk_list"
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

### Risk List

- Release tooling may be missing or partially configured.
- Existing list selectors may be unstable for E2E.
- Order status mapping may be duplicated in UI and API layers.

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
- blockers for preview readiness

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
  "validations": {
    "preflight": {
      "ok": false,
      "issues": [
        "private key path for preview release is missing"
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
    }
  },
  "handoff": {
    "owner": "pm",
    "next_action": "collect_release_key_and_run_preview",
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
