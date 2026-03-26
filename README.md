# Wechat Miniapp Delivery

Universal WeChat miniapp delivery skill for Codex, Claude Code, and OpenClaw.

## Repo Layout

```text
.
├── README.md
├── catalog.json
├── scripts/
│   ├── install_from_github.py
│   ├── install_skill.py
│   └── sync_skill_layout.py
├── skills/
│   └── wechat-miniapp-delivery/
├── .codex/skills/
└── .claude/skills/
```

`skills/wechat-miniapp-delivery` is the canonical source. `.codex/skills` and `.claude/skills` are generated mirrors for repo-local use. `catalog.json` is the lightweight portability manifest for installers and future registries.

## What This Skill Covers

- Developer, release-manager PM, unit-test, and E2E QA coordination
- Tool-oriented miniapp delivery: CI release, unit and E2E automation, CloudBase deployment, and security or compliance gates
- High-risk concerns such as payment callbacks, privacy guidance, secrets leakage, CloudBase permissions, release fallback, and release observation

## Agent Compatibility

| Agent surface | Recommended path |
| --- | --- |
| OpenClaw | `skills/wechat-miniapp-delivery` |
| Codex | `.codex/skills/wechat-miniapp-delivery` or GitHub repo-path install from `skills/wechat-miniapp-delivery` |
| Claude Code | `.claude/skills/wechat-miniapp-delivery` |

## Install From A Local Clone

- Codex: `python3 scripts/install_skill.py --target codex`
- Claude Code: `python3 scripts/install_skill.py --target claude`
- Codex + Claude: `python3 scripts/install_skill.py --target all`
- OpenClaw into another workspace: `python3 scripts/install_skill.py --target openclaw --dest /path/to/workspace/skills`

OpenClaw users can also just open this repo as a workspace because the canonical skill already lives under `skills/`.

## Install Directly From GitHub

- Codex native repo-path install:

```bash
python3 "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo cenkaifeng-qiliangjia/wechat-miniapp-delivery \
  --path skills/wechat-miniapp-delivery
```

- Generic GitHub bootstrap:

```bash
curl -fsSL https://raw.githubusercontent.com/cenkaifeng-qiliangjia/wechat-miniapp-delivery/main/scripts/install_from_github.py \
  | python3 - --target all
```

For OpenClaw target-copy installs, add `--target openclaw --dest /path/to/workspace/skills`.

## Maintainer Workflow

1. Edit only `skills/wechat-miniapp-delivery`.
2. Run `python3 scripts/sync_skill_layout.py`.
3. Validate the canonical skill with `python3 "$CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py" skills/wechat-miniapp-delivery`.
4. Smoke-test the install scripts.
5. Commit the canonical skill plus refreshed mirrors.

## Source Inputs

- `deep-research-report.md`
- `deep-research-report _V2.md`
- Anthropic's "The Complete Guide to Building Skills for Claude"
