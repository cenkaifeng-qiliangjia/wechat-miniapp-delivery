# JSON Contracts

Use these contracts for planning, validation, and release handoffs. Keep them compact. Return them in the response unless the user asked for files on disk.

## Input Contract

```json
{
  "mode": "plan|implement|validate|release",
  "requirement": {
    "title": "Order list filtering and preview release",
    "description": "Add status filtering, pull-to-refresh, and release validation.",
    "acceptance": [
      "Filter options work",
      "Refresh updates the list",
      "Preview release evidence is available"
    ]
  },
  "project": {
    "type": "native-weapp|taro|uni-app",
    "repo_path": "./",
    "appid": "wx1234567890",
    "env": "dev|staging|prod"
  },
  "tech_choices": {
    "ui_library": "weui|tdesign|vant|existing",
    "backend": "cloudbase|custom|hybrid",
    "observability": "rum|sentry|both|none"
  },
  "release": {
    "action": "preview|upload|publish|none",
    "version": "1.2.3",
    "robot": 1
  },
  "quality_gates": {
    "unit_coverage_min": 0.75,
    "e2e_flows": [
      "order-list-filter",
      "order-detail-pay"
    ],
    "privacy_data_types": [
      "profile",
      "location"
    ],
    "secret_scan": true
  },
  "risk_modules": [
    "payment",
    "privacy"
  ]
}
```

## Plan Output Contract

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
      "reason": "Native miniapp project with existing preview flow"
    }
  ],
  "task_graph": [
    {
      "id": "T1",
      "owner": "developer",
      "scope": "pages/order-list",
      "acceptance": "Filtering and refresh work"
    },
    {
      "id": "T2",
      "owner": "unit",
      "scope": "tests/unit/order-list",
      "acceptance": "Changed logic is covered"
    },
    {
      "id": "T3",
      "owner": "e2e",
      "scope": "tests/e2e/order-list-filter",
      "acceptance": "Critical flow passes in automation"
    }
  ],
  "handoff": {
    "owner": "developer",
    "next_action": "implement_change",
    "artifacts": [
      "plan",
      "acceptance_matrix",
      "risk_list"
    ]
  }
}
```

## Validation And Release Output Contract

```json
{
  "summary": {
    "decision": "pass|fail|needs-review",
    "stage": "validate|release_candidate|post_release"
  },
  "changes": {
    "files": [
      "pages/order-list/index.js",
      "tests/unit/order-list.test.js"
    ],
    "cloud_resources": [
      "cloudfunctions/makeOrder"
    ]
  },
  "validations": {
    "preflight": {
      "ok": true,
      "issues": []
    },
    "lint": {
      "ok": true,
      "issues": []
    },
    "unit": {
      "ok": true,
      "coverage": {
        "lines": 0.82
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
    "compliance": {
      "privacy_ok": true,
      "secrets_ok": true,
      "issues": []
    },
    "release": {
      "ok": true,
      "mode": "preview",
      "version": "1.2.3",
      "qrcode_path": "./artifacts/preview.png"
    },
    "observability": {
      "ok": true,
      "provider": "rum",
      "release_tag": "1.2.3"
    }
  },
  "handoff": {
    "owner": "pm",
    "next_action": "approve_release",
    "artifacts": [
      "validation_summary",
      "release_evidence",
      "rollback_target"
    ]
  },
  "rollback": {
    "available": true,
    "target_version": "1.2.2"
  }
}
```

## Minimal Response Shape

For small tasks, reduce the response to these fields:
- `summary`
- `validations`
- `handoff`
- `rollback`

Do not drop `handoff` or `rollback` on release-related tasks.
