# Wechat Miniapp Delivery

Project-local Codex skill for building, testing, accepting, and releasing WeChat mini program changes.

## Repo Layout

```text
.
├── README.md
└── .codex/skills/wechat-miniapp-delivery/
    ├── SKILL.md
    ├── agents/openai.yaml
    └── references/
```

## What This Skill Covers

- Developer, release-manager PM, unit-test, and E2E QA role coordination
- Plan, implementation, validation, acceptance, preview or upload, and post-release checks
- High-risk miniapp concerns such as payment, privacy, secrets, CloudBase permissions, observability, and rollback readiness

## Use It

1. Open this repo in Codex, or copy `.codex/skills/wechat-miniapp-delivery` into another repo's `.codex/skills/`.
2. Ask Codex to use `$wechat-miniapp-delivery` for a miniapp task.
3. Start with a prompt such as:
   - `Use $wechat-miniapp-delivery to add status filtering to the order list and prepare a preview release.`
   - `Use $wechat-miniapp-delivery to validate whether this miniapp version is release-ready.`
   - `Use $wechat-miniapp-delivery to add payment confirmation, unit tests, and E2E coverage.`

## Best-Practice Choices

- Progressive disclosure: `SKILL.md` stays small and detailed material lives in `references/`
- Explicit trigger language in frontmatter
- Examples, troubleshooting, and gate-based workflow in the skill body
- A filled-in handoff example for PM, developer, unit-test, and E2E coordination
- Repo-level README for GitHub distribution and no README inside the skill folder
- Project-local `.codex/skills/` path for easy discovery

## Source Inputs

- A deep-research report on miniapp engineering, testing, release, and observability
- Anthropic's "The Complete Guide to Building Skills for Claude"
