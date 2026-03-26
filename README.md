# Wechat Miniapp Delivery

通用微信小程序交付 Skill，面向 Codex、Claude Code 和 OpenClaw。

这个仓库现在只保留一个真源：`skills/wechat-miniapp-delivery`。  
`.codex/` 和 `.claude/` 不再作为仓库内容提交，避免三份完全相同的 skill 目录长期重复维护；如果需要做本地联调，可以用脚本按需生成它们。

## 仓库结构

```text
.
├── README.md
├── .gitignore
├── catalog.json
├── scripts/
│   ├── install_from_github.py
│   ├── install_skill.py
│   └── sync_skill_layout.py
└── skills/
    └── wechat-miniapp-delivery/
```

目录说明：
- `skills/wechat-miniapp-delivery`：唯一真源，也是 GitHub repo-path 安装入口
- `scripts/install_skill.py`：从本地 clone 安装到 Codex、Claude Code 或 OpenClaw
- `scripts/install_from_github.py`：不 clone 仓库，直接从 GitHub 安装
- `scripts/sync_skill_layout.py`：按需生成本地 `.codex/`、`.claude/` 镜像，仅用于联调，不建议入库
- `catalog.json`：轻量级分发清单，给安装器或注册中心使用

## Skill 覆盖范围

这个 skill 主要覆盖微信小程序从需求到上线的完整交付流程，包括：
- 开发者、版本管理 PM、单元测试、E2E 测试的角色编排
- `miniprogram-ci`、自动化测试、CloudBase 部署、安全与合规门禁
- 支付、隐私、密钥泄露、发布回退、发布观测等高风险环节
- Taro 4 + React 的通用编码模式和常见坑规避

## 为什么只保留真源

之前仓库里同时提交了：
- `skills/wechat-miniapp-delivery`
- `.codex/skills/wechat-miniapp-delivery`
- `.claude/skills/wechat-miniapp-delivery`

它们的内容是一样的，差别只在“给谁读”。继续把三份都放进 git，会带来两个问题：
- 每次改 skill 都要同步三处，容易漏
- PR diff 会被重复内容放大，阅读和 review 成本更高

现在的策略是：
- 仓库里只维护 `skills/` 真源
- Codex / Claude 的 repo-local 镜像按需生成，不入库
- 安装时优先直接从 `skills/wechat-miniapp-delivery` 这一路径消费

## 兼容方式

| 使用端 | 推荐方式 |
| --- | --- |
| Codex | 直接用 GitHub repo-path 安装 `skills/wechat-miniapp-delivery` |
| Claude Code | 用本地或 GitHub 安装脚本复制到 `~/.claude/skills` |
| OpenClaw | 直接消费仓库内 `skills/wechat-miniapp-delivery`，或复制到目标 workspace 的 `skills/` |

## 本地安装

从本地 clone 安装：

- Codex：`python3 scripts/install_skill.py --target codex`
- Claude Code：`python3 scripts/install_skill.py --target claude`
- Codex + Claude：`python3 scripts/install_skill.py --target all`
- OpenClaw：`python3 scripts/install_skill.py --target openclaw --dest /path/to/workspace/skills`

如果你只是想在 OpenClaw 里直接使用，也可以把这个仓库本身作为 workspace 打开，因为 skill 真源已经位于 `skills/` 下。

## 从 GitHub 直接安装

Codex 原生 repo-path 安装：

```bash
python3 "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo cenkaifeng-qiliangjia/wechat-miniapp-delivery \
  --path skills/wechat-miniapp-delivery
```

通用 GitHub 一键安装：

```bash
curl -fsSL https://raw.githubusercontent.com/cenkaifeng-qiliangjia/wechat-miniapp-delivery/main/scripts/install_from_github.py \
  | python3 - --target all
```

如果是 OpenClaw 目标路径安装，再加：

```bash
--target openclaw --dest /path/to/workspace/skills
```

## 本地镜像生成

如果你确实需要 repo-local 的 `.codex/` 或 `.claude/` 目录做联调，可以手动生成：

```bash
python3 scripts/sync_skill_layout.py
```

注意：
- 这些镜像目录已经被 `.gitignore` 忽略
- 它们只是调试产物，不是仓库真源
- 日常维护不应该直接编辑它们

## 维护流程

1. 只编辑 `skills/wechat-miniapp-delivery`
2. 用官方 validator 校验真源：

```bash
python3 "$CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py" \
  skills/wechat-miniapp-delivery
```

3. 运行本地安装 smoke test
4. 如果需要做 repo-local 联调，再运行 `python3 scripts/sync_skill_layout.py`
5. 提交真源与必要脚本改动，不提交生成镜像

## 资料来源

- `deep-research-report.md`
- `deep-research-report _V2.md`
- Anthropic《The Complete Guide to Building Skills for Claude》
