# Multi-Platform Miniapp Patterns

Use this reference when the repo targets more than one miniapp framework, mixes shared packages with platform-specific shells, or needs framework-aware delivery planning.

## Detect The Delivery Variant

Classify the repo before editing:
- `native-weapp`: `app.json`, `project.config.json`, page folders under the miniapp root
- `taro-react`: `@tarojs/*`, React entry files, Taro build config, output such as `dist/weapp`
- `taro-vue`: `@tarojs/*`, Vue SFCs or Vue entry files, Taro build config
- `uni-app-vue`: `pages.json`, `manifest.json`, `uni_modules`, Vue pages or composables
- `hybrid-cross-platform`: one shared package graph feeding more than one runtime shell

If more than one variant is present, record both:
- the current WeChat delivery target
- the shared code surfaces that may affect other runtimes

## Keep Shared Code Portable

- Keep shared packages free of direct `wx`, `Taro`, or `uni` API imports.
- Push platform APIs behind adapters at the app edge.
- Pass platform components, navigation helpers, storage helpers, or upload services into shared UI instead of importing them directly.
- Keep runtime-specific config, permissions, and page declarations in the platform shell, not in shared packages.
- Split `shared delivery` status from `weapp acceptance` status whenever a change touches common code.

## Normalize Runtime Boundaries

Use a thin abstraction for cross-platform surfaces:
- navigation
- storage
- request or upload
- permissions
- analytics or observability
- auth session refresh

Keep the abstraction stable and testable. Do not let feature code branch on platform in many places.

## Expect Event And Component Differences

- Treat component events as framework-specific until proven otherwise.
- Re-check form input, scroll, share, and pull-to-refresh behavior when code is shared across runtimes.
- Do not assume web-like bubbling or DOM availability in shared UI logic.
- Keep platform-only components behind adapters or shell components so shared packages stay framework-neutral.

## Plan The Release Path Per Variant

Use the framework-specific build path that already exists in the repo:
- `native-weapp`: direct `miniprogram-ci`
- `taro-react` or `taro-vue`: framework build first, then `miniprogram-ci` or repo wrapper
- `uni-app-vue`: uni build first, then the WeChat output path and release flow

Never assume a shared package change is release-ready until the actual WeChat output path is verified.

## Plan Acceptance Per Variant

When shared code is touched, track at least two acceptance scopes:
- `weapp acceptance`: what must pass for the current release target
- `shared impact`: what other runtimes or shells may regress even if they are not being released now

For WeChat release work, keep these acceptance dimensions explicit:
- functional acceptance
- E2E acceptance
- performance acceptance
- developer test obligations for touched APIs and shared logic

## Escalate When A Repo Needs Variant-Specific Rules

- If the repo is Taro 4 with React, also read `references/taro4-react-patterns.md`.
- If the repo uses a framework variant with recurring pitfalls, add a dedicated reference instead of bloating `SKILL.md`.
- If a shared package requires platform branching, document the branch boundary and why the abstraction could not stay pure.
