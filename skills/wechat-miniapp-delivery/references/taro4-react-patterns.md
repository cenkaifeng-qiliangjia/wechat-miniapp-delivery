# Taro 4 React Patterns

Use this reference when the detected project is a Taro 4 miniapp using React. Keep the guidance framework-level and generic.

## Identifying Taro 4 Projects

Look for most of these signals together:
- `@tarojs/*` dependencies on `^4.x`
- `defineConfig` imported from `@tarojs/cli`
- `defineAppConfig` used in `app.config.ts`
- `framework: "react"`
- `compiler.type: "webpack5"`
- build output under `dist/` or `dist/weapp`

If the repo says Taro but those signals are mixed or missing, stop and inspect the actual build config before editing.

## Lifecycle Hooks

- Use `useEffect` for mount-only setup that should run once per component lifetime.
- Use `useDidShow` for logic that must run every time the page becomes visible again.
- Use `useDidHide` for pause or suspend behavior when the page stays in the stack but is no longer active.
- Use `usePullDownRefresh` for pull-to-refresh flows and always pair successful completion with `Taro.stopPullDownRefresh()`.
- Use `useReachBottom` for pagination or incremental loading near the bottom of the page.
- Use `useShareAppMessage` for page-level share payloads.
- Use `useLoad` for initial route parameter parsing.
- Use `useReady` for logic that depends on the page tree being ready.

Rule of thumb:
- `useEffect` = mount only
- `useDidShow` = every time the page becomes visible

## React Hooks Pitfalls In Miniapp

- Stabilize mutable external state with `useRef` when callbacks or memoized values need the latest value without triggering dependency churn.
- When `useMemo` or `useCallback` reads changing state only to access the latest snapshot, mirror that state into a ref first instead of widening dependencies until the page re-renders forever.
- Never put `Taro.getStorageSync()` directly in a dependency array. It can return a fresh reference even when the logical content did not change.
- Pages stay alive in the miniapp stack. Do not assume leaving a page triggers unmount immediately.
- Use `useDidHide` for pause and resume boundaries. Do not rely on `useEffect` cleanup alone for page visibility transitions.

## Component Mapping

- `View` is the default layout container, not `div`.
- `Text` is the safe default for inline text, truncation, and nested text blocks.
- `Image` needs explicit sizing and mode choices that match miniapp behavior instead of web CSS defaults.
- `RichText` is for sanitized HTML-like content, not arbitrary interactive DOM.
- `ScrollView` owns its own scroll container semantics and events; do not assume document scroll behavior.
- `Input` reads from `onInput` with `e.detail.value`, not web-style `onChange`.
- `onClick` works well on `View` and `Text`, but not every native component behaves like a web element. Check the component event model before reusing generic handlers.

## Styling Rules

### Selector restrictions

- Prefer flat class selectors. Tag selectors such as `view {}` or `text {}` are ignored or unreliable in the miniapp runtime.
- Do not rely on the `*` wildcard selector. It is not supported.
- Descendant combinators work, but child and sibling combinators such as `>`, `+`, and `~` have inconsistent support across base library versions. Prefer direct class hooks instead.
- Use `:global` only when the project is actually using CSS Modules. Taro's default SCSS setup is not CSS Modules, so check the style config before reaching for it.

### Units

- Use `rpx` as the default responsive unit. `750rpx` maps to the full screen width across devices.
- Use `px` only when a fixed physical size is intentional, such as `1px` hairline borders.
- Treat `rem`, `em`, `vw`, and `vh` as partial-support options. `rpx` is the standard choice for layout and spacing.

### Unsupported or limited CSS

- Do not expect `position: fixed` to work inside scroll containers. It is fixed to the page viewport, not the nested scroll area.
- Keep `z-index` expectations local to the current stacking context. Native components such as `map`, `video`, `canvas`, and `textarea` still render above normal layers.
- Be careful with `overflow: hidden` plus `border-radius`. Older base library versions may fail to clip children correctly.
- CSS animations and transitions work, but `@keyframes` names should be unique per component to avoid bundle-level collisions.
- Do not rely on CSS custom properties with `var()` when the target base library can be below `2.11.0`.

### SCSS in Taro 4

- Taro 4 supports SCSS out of the box when `sass` is present in `devDependencies`.
- Keep a co-located `.scss` file for each page or component and import it from the `.tsx` entry.
- Prefer flat class names over deep nesting. Miniapp style isolation is already per component by default.
- Avoid long `@import` chains across packages. Shared styles should flow through design tokens or copied values, because workspace SCSS imports may not resolve cleanly through Taro's compilation scope.

## HTML Content In Miniapp

- `RichText` is the standard way to render HTML content in a miniapp.
- Links rendered through `RichText` are not reliably clickable. Provide a separate explicit action for opening or copying the URL.
- Always sanitize incoming HTML before rendering it. Strip `script`, `iframe`, inline `on*` handlers, and `javascript:` URLs.
- When content contains URLs, provide a separate "copy link" UI instead of assuming inline anchors will work.
- For long-press image actions, prefer `showMenuByLongpress` on `Image`.

## Page Navigation And Data Passing

- Keep route query payloads small. Query length is limited, so large or nested payloads should move through storage or a state bridge.
- The page stack limit is `10`. Use `redirectTo` for screens that should replace the current entry instead of growing the stack.
- Use storage for large transient payloads, but clear it after consumption to avoid stale state leaks.
- Wrap external URLs in a dedicated `WebView` page rather than pushing raw external links into normal miniapp navigation.

## Monorepo And Cross-Platform Patterns

- Use `mini.compile.include` when workspace source packages must be compiled into the miniapp build.
- Set `compiler.prebundle.enable: false` when consuming unbuilt workspace packages that should stay as source during development.
- Prefer an adapter pattern for shared UI: shared components receive platform component maps or platform services as props instead of importing miniapp APIs directly.
- Shared packages must never import `Taro`, `wx`, or `uni` APIs directly.
- Keep platform bindings at the app edge so shared packages stay portable across miniapp, web, and other runtimes.

## Toast And Modal Constraints

- Keep `showToast` titles short: about `7` Chinese characters or `12` English characters before truncation risk becomes high.
- `showModal` is the native confirm dialog; use it when the user must explicitly confirm or cancel.
- Use `showLoading` and `hideLoading` around longer async transitions instead of overloading toast messaging.

## Build Configuration

- Prefer `defineConfig` for typed config and clearer environment branching.
- Output builds to `dist/` and let DevTools read from the generated miniapp directory there.
- Keep `project.config.json` aligned so `miniprogramRoot` points at the actual build output.
- When build behavior differs between local and CI, inspect the Taro config first instead of patching generated files.
