# Wechat Miniapp Delivery

通用微信小程序交付 Skill 套件，面向 Codex、Claude Code 和 OpenClaw。

包含两个互补的 skill：
- **wechat-miniapp-delivery** — 交付流程编排（怎么交付）
- **wechat-miniapp-design** — 设计质量门禁（怎么设计）

仓库只保留一份真源：`skills/`。`.codex/` 和 `.claude/` 不入库，按需用脚本生成。

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
    ├── wechat-miniapp-delivery/
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   └── references/
    │       ├── taro4-react-patterns.md
    │       ├── tooling-and-risk-checklists.md
    │       ├── workflow-and-handoffs.md
    │       ├── json-contracts.md
    │       ├── example-handoff-pack.md
    │       └── v2-toolchain-catalog.md
    └── wechat-miniapp-design/
        └── SKILL.md
```

目录说明：
- `skills/wechat-miniapp-delivery`：交付编排 skill 真源
- `skills/wechat-miniapp-design`：设计质量 skill 真源
- `scripts/install_skill.py`：从本地 clone 安装到 Codex、Claude Code 或 OpenClaw
- `scripts/install_from_github.py`：不 clone 仓库，直接从 GitHub 安装
- `scripts/sync_skill_layout.py`：按需生成本地 `.codex/`、`.claude/` 镜像，仅用于联调，不建议入库
- `catalog.json`：轻量级分发清单，给安装器或注册中心使用

## Skill 说明

### wechat-miniapp-delivery（交付编排）

覆盖微信小程序从需求到上线的完整交付流程：

- **角色编排**：PM、开发者、单元测试、E2E QA 的分工和交接
- **交付流程**：plan → preflight → implement → validate → release，每步有结构化产物
- **工具集成**：`miniprogram-ci`、`miniprogram-simulate`、`minium`、CloudBase MCP/CLI
- **高风险门禁**：支付回调验证、隐私合规、密钥扫描、发布回退
- **Taro 4 支持**：`references/taro4-react-patterns.md` 覆盖生命周期、Hooks 陷阱、组件映射、Monorepo 模式
- **降级策略**：每个能力模块都有明确的 fallback 路径和 blocker 报告格式

### wechat-miniapp-design（设计质量）

小程序 UI 开发的设计系统和视觉质量标准：

- **Design Token 体系**：颜色（60-30-10 规则）、间距（4px 递增）、字号、圆角、阴影的语义化变量
- **小程序 CSS 约束**：选择器限制、rpx 单位、`position: fixed` / `z-index` / `var()` 兼容性表
- **SCSS 规范**：单文件 token 源、扁平 class 命名、跨包样式隔离
- **跨平台设计**：adapter 模式下的共享样式策略、单位映射、颜色一致性
- **组件模式**：卡片、按钮、标签、KPI 数据展示、空态/加载态的标准写法
- **质量检查清单**：10 项视觉验收标准（token 使用、对比度、触摸区域、状态覆盖等）

### 两个 Skill 如何协作

| 交付阶段 | delivery 负责 | design 负责 |
|---------|--------------|------------|
| Plan | 需求拆解、角色分配、风险识别 | 视觉范围和 token 需求 |
| Implement | 代码实现、云函数、配置 | token 体系、组件模式、CSS 约束 |
| Validate | 单元/E2E 测试、合规门禁 | Visual Quality Checklist |
| Release | 预览/上传/发布、回退准备 | 无视觉回归确认 |

## 安装

### 从 GitHub 直接安装

```bash
# Codex
python3 scripts/install_from_github.py --target codex

# Claude Code
python3 scripts/install_from_github.py --target claude

# 全部
python3 scripts/install_from_github.py --target all
```

### 从本地 clone 安装

```bash
git clone https://github.com/cenkaifeng-qiliangjia/wechat-miniapp-delivery.git
cd wechat-miniapp-delivery

# Codex + Claude Code
python3 scripts/install_skill.py --target all
```

### 手动安装

将 `skills/wechat-miniapp-delivery` 和 `skills/wechat-miniapp-design` 复制到目标平台的 skills 目录：

| 平台 | 目标路径 |
|------|---------|
| Codex | `.codex/skills/` |
| Claude Code | `.claude/skills/` |
| OpenClaw | `skills/` |

## 使用

安装后，在对话中触发：

```
Use $wechat-miniapp-delivery to add status filtering to the order list and prepare a preview release.

Use $wechat-miniapp-design to review the SCSS of the dashboard page for token compliance.
```

或在开发小程序功能时，两个 skill 会根据任务类型自动参与。

## 为什么只保留真源

之前仓库里同时提交了三份相同的 skill 目录（`skills/`、`.codex/`、`.claude/`）。现在的策略是：
- 仓库里只维护 `skills/` 真源
- Codex / Claude 的 repo-local 镜像按需生成，不入库
- 安装时优先直接从 `skills/` 路径消费

## 本地镜像生成

如需 `.codex/` 或 `.claude/` 目录做联调：

```bash
python3 scripts/sync_skill_layout.py
```

注意：镜像目录已被 `.gitignore` 忽略，仅用于调试。

## 维护流程

1. 只编辑 `skills/` 下的真源
2. 两个 skill 独立演进，delivery 的 SKILL.md 通过 "Read References" 引用 design skill
3. 提交真源与脚本改动，不提交生成镜像
4. 如需联调，运行 `python3 scripts/sync_skill_layout.py`

## 资料来源

- Anthropic《The Complete Guide to Building Skills for Claude》
- 微信小程序官方文档、Taro 4 官方文档
- `miniprogram-ci`、`miniprogram-simulate`、`minium` 工具文档
