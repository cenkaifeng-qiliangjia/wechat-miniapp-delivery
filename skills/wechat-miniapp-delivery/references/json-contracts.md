# JSON Contracts

Use these contracts for planning, validation, and release handoffs. Keep them compact. Return them in the response unless the user asked for files on disk.

## Unified Task Input

```json
{
  "mode": "plan|implement|validate|release",
  "execution_surface": {
    "agent": "codex|claude-code|openclaw",
    "subagents_available": true
  },
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
    "type": "native-weapp|taro-react|taro-vue|uni-app-vue|hybrid-cross-platform",
    "repo_path": "./",
    "appid": "wx1234567890",
    "backend": "cloudbase|custom|hybrid",
    "env": "dev|staging|prod"
  },
  "runtime": {
    "node_version": "18.19.0",
    "python_version": "3.11.7",
    "devtools_automation": true
  },
  "tech_choices": {
    "ui_library": "weui|tdesign|vant|existing",
    "observability": "rum|sentry|both|none"
  },
  "capability_plan": [
    {
      "name": "weapp_ci_release",
      "requested_action": "preview",
      "required": true,
      "fallback": "preview-only"
    },
    {
      "name": "weapp_test_automation",
      "requested_action": "unit+api-contract+e2e",
      "required": true,
      "fallback": "unit-only"
    },
    {
      "name": "security_compliance_gate",
      "requested_action": "full",
      "required": true,
      "fallback": "block-high-risk"
    }
  ],
  "fallback_policy": {
    "split_feature_delivery_and_release_enablement": true,
    "allow_release_without_observability": false
  },
  "release": {
    "action": "preview|upload|publish|none",
    "version": "1.2.3",
    "robot": 1
  },
  "quality_gates": {
    "unit_coverage_min": 0.75,
    "api_contract_surfaces": [
      "api/order/list",
      "cloudfunctions/orderList"
    ],
    "e2e_flows": [
      "order-list-filter",
      "order-detail-pay"
    ],
    "functional_acceptance": [
      "filter_options_match_supported_states",
      "refresh_preserves_selected_filter"
    ],
    "performance_acceptance": [
      "no_regression_on_first_screen",
      "request_count_stays_within_baseline"
    ],
    "privacy_data_types": [
      "profile",
      "location"
    ]
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
  "env_doctor": {
    "status": "pass|fail|needs-setup",
    "issues": [],
    "downgrade_plan": []
  },
  "architecture_decisions": [
    {
      "topic": "release_tool",
      "choice": "miniprogram-ci",
      "reason": "Native miniapp project with existing preview flow"
    }
  ],
  "capability_plan": [
    {
      "name": "weapp_ci_release",
      "action": "preview",
      "status": "planned",
      "fallback": "preview-only if upload is blocked"
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
      "owner": "functional_qa",
      "scope": "acceptance matrix and user-visible edge states",
      "acceptance": "Business criteria are explicitly proved or blocked"
    },
    {
      "id": "T4",
      "owner": "e2e",
      "scope": "tests/e2e/order-list-filter",
      "acceptance": "Critical flow passes in automation"
    },
    {
      "id": "T5",
      "owner": "performance_qa",
      "scope": "first-screen latency and request-count comparison",
      "acceptance": "No unacceptable regression against baseline"
    }
  ],
  "developer_test_obligations": {
    "unit": [
      "order_status_mapper",
      "refresh_state_transition"
    ],
    "api_contract": [
      "order_list_request_params",
      "order_list_response_shape"
    ]
  },
  "delivery_split": {
    "feature_delivery": "in_scope",
    "release_enablement": "in_scope"
  },
  "handoff": {
    "owner": "developer",
    "next_action": "implement_change",
    "artifacts": [
      "plan",
      "acceptance_matrix",
      "risk_list",
      "env_doctor"
    ]
  },
  "rollback": {
    "available": true,
    "target_version": "current_production"
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
  "feature_delivery": {
    "status": "pass|fail|needs-review",
    "notes": []
  },
  "release_enablement": {
    "status": "pass|fail|needs-review",
    "notes": []
  },
  "developer_test_obligations": {
    "status": "pass|fail|needs-review",
    "notes": []
  },
  "env_doctor": {
    "status": "pass|fail|needs-setup",
    "issues": [],
    "downgrade_plan": []
  },
  "changes": {
    "files": [
      "pages/order-list/index.js",
      "tests/unit/order-list.test.js"
    ],
    "api_surfaces": [
      "api/order/list"
    ],
    "cloud_resources": [
      "cloudfunctions/makeOrder"
    ]
  },
  "tool_runs": {
    "weapp_ci_release": {
      "ok": true,
      "mode": "preview",
      "degraded": false,
      "artifacts": [
        "./artifacts/preview.png"
      ],
      "issues": []
    },
    "weapp_test_automation": {
      "ok": true,
      "mode": "unit+api-contract+e2e",
      "degraded": false,
      "issues": []
    },
    "cloudbase_env_deploy": {
      "ok": true,
      "channel": "mcp|cli|skipped",
      "issues": []
    },
    "security_compliance_gate": {
      "ok": true,
      "blockers": [],
      "warnings": [],
      "artifacts": []
    }
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
    "api_contract": {
      "ok": true,
      "surfaces": [
        "api/order/list"
      ],
      "artifacts": []
    },
    "functional_acceptance": {
      "ok": true,
      "failed_criteria": [],
      "artifacts": []
    },
    "e2e": {
      "ok": true,
      "failed_flows": [],
      "artifacts": [
        "./artifacts/e2e/order-list-filter.png"
      ]
    },
    "performance": {
      "ok": true,
      "baseline": "main",
      "issues": [],
      "artifacts": []
    },
    "compliance": {
      "privacy_ok": true,
      "secrets_ok": true,
      "payment_ok": true,
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
  "release_evidence": {
    "version": "1.2.3",
    "mode": "preview",
    "artifact_paths": [
      "./artifacts/preview.png"
    ],
    "logs": [
      "./artifacts/release.log"
    ],
    "observation_notes": [
      "RUM release tag set to 1.2.3"
    ]
  },
  "handoff": {
    "owner": "pm",
    "next_action": "approve_release",
    "artifacts": [
      "validation_summary",
      "functional_acceptance",
      "performance_report",
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
- `feature_delivery`
- `release_enablement`
- `env_doctor`
- `tool_runs`
- `validations`
- `developer_test_obligations`
- `handoff`
- `rollback`

Do not drop `handoff` or `rollback` on release-related tasks.
