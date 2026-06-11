# Wechat Miniapp Delivery

通用微信小程序 Skill 套件，面向 Codex、Claude Code 和 OpenClaw。

当前套件包含两个互补的 skill：
- `wechat-miniapp-delivery`：交付流程编排，负责“怎么交付”
- `wechat-miniapp-design`：设计与视觉质量门禁，负责“怎么设计”

仓库只保留 `skills/` 下的真源。`.codex/` 和 `.claude/` 不入库，按需用脚本生成。

## 仓库结构

```text
.
├── README.md
├── .gitignore
├── catalog.json
├── repository.json
├── .github/workflows/validate.yml
├── scripts/
│   ├── check_repository_sync.py
│   ├── install_from_github.py
│   ├── install_skill.py
│   ├── sync_skill_layout.py
│   └── validate_repo.py
└── skills/
    ├── wechat-miniapp-delivery/
    └── wechat-miniapp-design/
```

目录说明：
- `skills/wechat-miniapp-delivery`：交付编排 skill 真源
- `skills/wechat-miniapp-design`：设计质量 skill 真源
- `scripts/install_skill.py`：从本地 clone 安装整套 skills，或按名称筛选安装
- `scripts/install_from_github.py`：不 clone 仓库，直接从 GitHub 安装整套 skills，或按名称筛选安装
- `scripts/sync_skill_layout.py`：按需生成本地 `.codex/`、`.claude/` 镜像，仅用于联调
- `scripts/validate_repo.py`：校验 Skill 结构、JSON 示例、引用、仓库身份和 Visual QA 契约
- `scripts/check_repository_sync.py`：比较主仓库与 fork，只允许仓库身份字段不同
- `catalog.json`：skills 套件分发清单
- `repository.json`：当前仓库身份、主仓库或 fork 角色及上游关系

## Skill 说明

### `wechat-miniapp-delivery`

覆盖微信小程序从需求到上线的完整交付流程：
- 原生小程序、Taro、uni-app、混合跨平台仓库的交付编排
- 开发者、版本管理 PM、单元与接口契约测试、功能验收、E2E、性能验收的角色编排
- `miniprogram-ci`、自动化测试、CloudBase 部署、安全与合规门禁
- 支付、隐私、密钥泄露、发布回退、发布观测等高风险环节
- Taro 4 React、多平台共享层约束、研发接口测试责任与验收证据

### `wechat-miniapp-design`

负责小程序 UI 开发的设计系统和视觉质量标准：
- Design Token 体系
- 小程序 CSS 约束与 SCSS 规范
- 跨平台设计一致性
- 组件模式、状态模式、视觉质量检查清单
- 原生按钮文字/图标对齐、动态内容防抖、弹窗与 Canvas 等原生层级检查
- 按视觉状态矩阵执行 Developer Tools / 真机运行时验收

### 两个 Skill 如何协作

| 交付阶段 | delivery 负责 | design 负责 |
| --- | --- | --- |
| Plan | 需求拆解、角色分配、风险识别、验收矩阵 | 视觉范围、token 需求、组件模式 |
| Implement | 代码实现、云函数、配置、测试义务 | token 体系、组件样式、平台 CSS 约束 |
| Validate | 单元、接口契约、功能验收、E2E、性能、合规 | Visual Quality Checklist、运行时状态矩阵、截图证据 |
| Release | 预览、上传、回退、观测 | 视觉回归确认 |

## 安装

### 从 GitHub 直接安装整套 skills

```bash
curl -fsSL https://raw.githubusercontent.com/cenkaifeng-qiliangjia/wechat-miniapp-delivery/main/scripts/install_from_github.py \
  | python3 - --target all
```

只安装某一个 skill：

```bash
curl -fsSL https://raw.githubusercontent.com/cenkaifeng-qiliangjia/wechat-miniapp-delivery/main/scripts/install_from_github.py \
  | python3 - --target all --skill wechat-miniapp-delivery
curl -fsSL https://raw.githubusercontent.com/cenkaifeng-qiliangjia/wechat-miniapp-delivery/main/scripts/install_from_github.py \
  | python3 - --target all --skill wechat-miniapp-design
```

### 从本地 clone 安装整套 skills

```bash
git clone https://github.com/cenkaifeng-qiliangjia/wechat-miniapp-delivery.git
cd wechat-miniapp-delivery
python3 scripts/install_skill.py --target all
```

只安装某一个 skill：

```bash
python3 scripts/install_skill.py --target all --skill wechat-miniapp-delivery
python3 scripts/install_skill.py --target all --skill wechat-miniapp-design
```

### Codex 原生 repo-path 安装

Codex 的官方 installer 目前按单个 skill 路径安装，所以两条命令分别执行：

```bash
python3 "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo cenkaifeng-qiliangjia/wechat-miniapp-delivery \
  --path skills/wechat-miniapp-delivery
```

```bash
python3 "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo cenkaifeng-qiliangjia/wechat-miniapp-delivery \
  --path skills/wechat-miniapp-design
```

`scripts/install_from_github.py` 在本地 clone 中运行时会优先读取当前 checkout
的 `origin`。通过上述 raw URL 执行时，则默认安装提供该脚本的仓库；也可以用
`--repo owner/repo` 显式覆盖。

## 本地镜像生成

如需 `.codex/` 或 `.claude/` 目录做联调：

```bash
python3 scripts/sync_skill_layout.py
```

按 skill 名称筛选生成：

```bash
python3 scripts/sync_skill_layout.py --skill wechat-miniapp-delivery
```

注意：
- 镜像目录已被 `.gitignore` 忽略
- 镜像只是本地调试产物，不是仓库真源
- 日常维护不要直接编辑镜像

## 使用

安装后可以这样触发：

```text
Use $wechat-miniapp-delivery to plan a preview release for a Taro miniapp feature with API contract tests, functional acceptance, E2E, and performance acceptance.

Use $wechat-miniapp-design to review the SCSS of the dashboard page for token compliance and miniapp CSS constraints.
```

## 维护流程

1. 只编辑 `skills/` 下的真源
2. 运行 `python3 scripts/validate_repo.py`
3. 使用 `python3 scripts/check_repository_sync.py --other <另一个仓库路径>` 检查主仓库与 fork
4. 运行安装 smoke test
5. 如需联调，再生成 `.codex/` / `.claude/` 镜像
6. 提交真源与脚本改动，不提交生成镜像

GitHub Actions 会在 push 和 pull request 时自动运行仓库校验及本地安装 smoke test。

## 资料来源

- Anthropic《The Complete Guide to Building Skills for Claude》
- 微信小程序官方文档、Taro 官方文档、uni-app 官方文档
- `miniprogram-ci`、`miniprogram-simulate`、`minium`、CloudBase 相关工具文档
