---
name: wechat-miniapp-design
description: Design system and runtime visual quality gate for WeChat miniapp development. Use when building or reviewing miniapp pages, components, WXML/WXSS, Taro or uni-app styles, buttons with text or icons, conditional content, cards, sheets, modals, canvas overlays, theme switching, or any request mentioning UI, layout, styling, alignment, visual jitter, or layer issues. Enforces token discipline, native miniapp CSS constraints, cross-platform consistency, and state-based visual acceptance.
---

# WeChat Miniapp Design

Preserve the product's visual language, respect miniapp runtime constraints, and require rendered proof for user-visible UI work.

## Critical Runtime UI Gate

For every user-visible change:

1. Inventory interactive controls, conditional regions, overlays, and native components.
2. Define only the visual states affected by the change.
3. Inspect shared primitives and resets before patching one local selector.
4. Verify in WeChat Developer Tools or the repository's preview path. Static CSS review alone is not acceptance evidence.
5. Use a real device when `canvas`, `map`, `video`, `camera`, `textarea`, `<web-view>`, safe areas, fonts, or simulator differences are involved.

Load `references/runtime-ui-quality-gates.md` for button alignment, icon-and-text controls, layout jitter, theme switching, sheets, modals, or native-layer conflicts.

## Reuse The Existing Design System First

Inspect existing:

- tokens, CSS variables, themes, and shared style modules
- button, card, modal, typography, and spacing primitives
- framework conversion settings such as Taro `designWidth`, `deviceRatio`, and PostCSS
- density, color, radius, typography, and accessibility conventions

Reuse and extend them for scoped work. Do not force a token migration, rename established variables, or replace primitives unless the request is explicitly a design-system refactor.

If no reusable system exists, load `references/design-system-bootstrap.md` and introduce only the foundation needed by the current scope.

## Platform Rules

- Prefer class selectors and flat style hooks; avoid wildcard and fragile combinators.
- Follow the repository's existing `rpx` and `px` strategy.
- Do not assume `px` converts to `rpx`; verify framework and build configuration.
- Verify generated WeChat output for Taro and uni-app instead of trusting only H5 preview.
- Treat CSS variables, clipping, custom fonts, advanced selectors, viewport units, and WebView CSS as runtime-version concerns.
- A large `z-index` does not reliably cover native components.
- Use a touch target of at least 44px unless the product has a stricter accessible standard.

## High-Risk UI Patterns

### Buttons And Labels

- Reset native button defaults in one shared class, including `box-sizing`, margin, padding, inherited font, border, `::after`, text alignment, and predictable line height.
- For single-line text controls, use `display: flex`, `align-items: center`, `justify-content: center`, an explicit touch-safe height, and a compact line height.
- For icon-and-text controls, use flex gap and a fixed icon box.
- Do not align with spaces, glyph offsets, inherited body line height, or line-height equal to fixed height.
- After changing a shared reset, audit save, destructive, tab, chip, sheet, and modal actions.

### Dynamic Content

- Reserve layout space for bounded helper text, time ranges, validation, or theme details when neighboring content should stay still.
- Prefer a mounted slot with `min-height`, `opacity`, and `visibility` for short bounded content.
- Reserve layout space for the maximum expected wrapped lines.
- Use measured height animation only when expansion is intentional.
- Use conditional mounting when movement is expected or accessibility requires removal.
- Do not hide instability with arbitrary outer margin alone.

### Modals And Native Layers

- Treat `canvas`, `map`, `video`, `camera`, `textarea`, and similar surfaces as separate rendering layers.
- When a blocking modal opens, hide or unmount any native surface that can overlap it, or use the platform-supported cover layer.
- Use a full-screen backdrop and a dedicated opaque modal surface in every affected theme.
- Apply the same button-centering contract to modal actions.
- Verify native-layer behavior on a real device when simulator evidence is uncertain.

## Cross-Platform Boundary

- Keep shared visual semantics stable while allowing platform adapters at the shell.
- Verify every runtime touched by shared component changes; a WeChat fix can still regress H5 or another miniapp target.
- Keep platform-specific visibility, navigation, and native-layer handling at component or shell boundaries.
- For a WebView shell, separate native-shell UI checks from H5 layout and CSS compatibility checks.

## Visual Acceptance

Use the smallest state matrix that proves the change, including the state that exposed the bug.

Check:

- affected text and icon-text controls in default, pressed, disabled, loading, and modal states as applicable
- conditional content hidden, visible, and maximum-wrap states
- sheets and modals in affected themes
- native components mounted while overlays open
- shared control siblings after a reset change
- loading, empty, error, denied, and retry states when touched
- contrast, touch target, animation, and cross-platform impact where relevant

Capture screenshots, recordings, or equivalent rendered evidence. Name the runtime and device. Do not report generic `visual QA passed`; report states checked, evidence paths, and remaining blockers.

## Reference Loading

| Need | Load |
| --- | --- |
| Button centering, dynamic layout, modal layering, or state matrix workflow | `references/runtime-ui-quality-gates.md` |
| Project lacks tokens or component foundations | `references/design-system-bootstrap.md` |

Do not load bootstrap examples for a project that already has a design system.
