---
name: wechat-miniapp-design
description: Design system and runtime visual quality gate for WeChat miniapp development. Use when building or reviewing miniapp pages, components, WXML/WXSS, Taro or uni-app styles, buttons with text or icons, conditional content, cards, sheets, modals, canvas overlays, theme switching, or any request mentioning UI, layout, styling, alignment, visual jitter, or layer issues. Enforces token discipline, native miniapp CSS constraints, cross-platform consistency, and state-based visual acceptance.
---

# WeChat Miniapp Design

Use this skill as the design quality gate for miniapp UI work. Preserve the product's existing visual language, respect miniapp platform constraints, and require runtime evidence before delivery.

This skill complements `wechat-miniapp-delivery`: delivery handles the workflow (plan → implement → validate → release), design handles the visual standard (tokens → layout → components → quality check).

## Critical Runtime UI Gate

For every user-visible UI change:

1. Identify interactive controls, conditional regions, overlays, and native components before editing styles.
2. Build a visual state matrix that covers the states affected by the change.
3. Inspect shared control resets before patching one local button.
4. Verify the rendered result in the WeChat runtime or Developer Tools. Static CSS review alone is not acceptance evidence.
5. Verify on a real device when the change involves `canvas`, `map`, `video`, `camera`, `textarea`, `<web-view>`, safe areas, or a simulator-only rendering difference.

Read `references/runtime-ui-quality-gates.md` when the task includes button-label alignment, icon-and-text controls, conditional helper text, dynamic card height, theme switching, sheets, modals, or native-component layering.

## Design Thinking For Miniapp

Before writing styles, answer:

1. **Context** — Is this a data-dense dashboard, a content page, a form, or a marketing surface? Each has different density and rhythm needs.
2. **Platform** — Miniapp-only, web-only, or cross-platform shared? This determines which CSS features and units are available.
3. **Hierarchy** — What should the user see first, second, third? Establish visual weight before picking colors and sizes.
4. **Consistency** — Does this page reuse existing tokens and patterns, or does it need new ones? Prefer reuse.

## Reuse The Existing Design System First

Before introducing values or abstractions, inspect:
- existing token files, CSS variables, theme providers, and shared style modules
- shared button, card, modal, typography, and spacing primitives
- framework unit conversion such as Taro `designWidth`, `deviceRatio`, and PostCSS settings
- established density, color, radius, typography, and accessibility conventions

Reuse and extend those conventions for a scoped change. Do not force a token migration, rename established variables, or replace component primitives unless the request requires a design-system refactor.

When the project has no reusable system, introduce the smallest shared foundation needed by the current scope. The values below are fallback examples, not universal requirements.

## Fallback Design Token Examples

### Semantic Color Example

Organize colors by semantic role, not visual appearance:

```scss
// Brand
$color-primary: #0b8f7a;
$color-primary-dark: #066758;
$color-primary-light: rgba(11, 143, 122, 0.12);
$color-accent: #f5a75f;

// Status
$color-success: #1f8a56;
$color-warning: #d27b11;
$color-error: #b43c2f;

// Text hierarchy
$text-primary: #102a43;    // Headings, key numbers
$text-secondary: #526680;  // Descriptions, metadata
$text-tertiary: #6c7787;   // Labels, captions
$text-muted: #888;         // Disabled, placeholders
$text-on-primary: #fff;    // Text on brand-colored backgrounds

// Surfaces
$surface-page: #f5f7fa;
$surface-card: #fff;
$surface-card-glass: rgba(255, 255, 255, 0.88);
$surface-muted: #fafafa;
```

The **60-30-10 rule** can be a useful starting heuristic for a new marketing or content surface:
- 60% — Page background and neutral surfaces
- 30% — Cards, secondary surfaces, borders
- 10% — Brand accent (buttons, links, highlights)

Do not enforce this ratio on data-dense tools, established products, accessibility themes, or pages whose existing hierarchy uses another system.

### Spacing Scale Example

If the project lacks a spacing scale, a compact 4px-based scale is one reasonable starting point:

```scss
$space-2: 4px;    // Tight gaps
$space-4: 8px;    // Default inner gap
$space-6: 12px;   // Card inner padding
$space-8: 16px;   // Section padding
$space-12: 24px;  // Between sections
$space-16: 32px;  // Major section gaps
$space-24: 48px;  // Page-level padding
$space-32: 64px;  // Hero-level spacing
```

Rule: spacing between related elements < spacing between unrelated groups.

### Typography Scale Example

If the project lacks typography tokens, start with the smallest scale that supports the current hierarchy. Adapt these example values to the project's unit strategy and existing visual density:

```scss
$text-xs: 16px;   // Micro labels
$text-sm: 18px;   // Captions, metadata
$text-base: 22px; // Body text
$text-md: 24px;   // Emphasized body
$text-lg: 26px;   // Subheadings
$text-xl: 28px;   // Section titles
$text-2xl: 30px;  // Page subtitles
$text-3xl: 36px;  // Page titles
$text-4xl: 40px;  // Hero titles
```

Rules:
- Use `font-weight` to create hierarchy, not just size
- Use a readable body-copy line height appropriate to the font and density; `1.5-1.7` is a starting range for multi-line Chinese prose, not a control rule
- Use compact explicit line heights for buttons, tabs, chips, labels, and single-line metrics, then verify visual centering at runtime
- Prefer the existing font stack; introduce another family only when product requirements and runtime loading support justify it

### Border Radius Scale Example

```scss
$radius-sm: 8px;     // Code blocks, small tags
$radius-md: 12px;    // Images, inputs
$radius-lg: 16px;    // Buttons, cards (small)
$radius-xl: 20px;    // Cards (standard)
$radius-2xl: 24px;   // Cards (featured)
$radius-3xl: 32px;   // Full-page modals
$radius-full: 999px; // Pills, chips, avatars
```

### Shadow Scale Example

```scss
$shadow-xs: 0 4px 20px rgba(0, 0, 0, 0.06);   // Subtle lift
$shadow-sm: 0 8px 32px rgba(0, 0, 0, 0.06);    // Cards
$shadow-md: 0 18px 40px rgba(16, 42, 67, 0.1);  // Featured panels
```

## Miniapp CSS Constraints

### Selector Rules

- **Use class selectors only**. Tag selectors (`view {}`, `text {}`) are unreliable in miniapp runtime.
- **No `*` wildcard**.
- Child/sibling combinators (`>`, `+`, `~`) have inconsistent support — prefer flat class hooks.
- Exception: tag selectors inside `RichText` containers are acceptable because `RichText` renders real DOM.

### Units

- **`rpx`** is the default responsive unit. `750rpx` = full screen width.
- **`px`** only for hairline borders (`1px`) or intentionally fixed sizes.
- `rem`, `vw`, `vh` have partial support — avoid in production miniapp styles.

### Unsupported Or Limited CSS

| Feature | Limitation |
|---------|-----------|
| `position: fixed` | Only works relative to page viewport, not inside ScrollView |
| `z-index` | A large value does not reliably cover native components such as `map`, `video`, `canvas`, `camera`, or `textarea`; hide/unmount the native surface or use a supported cover layer |
| `overflow: hidden` + `border-radius` | May not clip children on older base library versions |
| `@keyframes` | Names must be unique per component to avoid bundle collisions |
| CSS `var()` | Not supported below base library 2.11.0 |
| Custom fonts (CDN) | Not reliably loadable — use system font stack or bundled fonts |
| `:hover` | No hover state on mobile — use active/pressed states instead |

### SCSS Best Practices

- One co-located `.scss` file per page/component, imported in the `.tsx`
- Flat class names over deep nesting — miniapp style isolation is per-component
- No `@import` chains across packages — shared styles via tokens or copied values
- If using SCSS `@import` (not `@use`), be aware of Dart Sass deprecation timeline

## Cross-Platform Design Patterns

When building shared UI that renders on both miniapp and web:

### Adapter-Compatible Styles

- Write styles that work with both `<View>` (miniapp) and `<div>` (web)
- Use class selectors exclusively — they work everywhere
- Avoid platform-specific pseudo-elements that may not render in miniapp

### Unit Strategy

| Token | Miniapp value | Web value |
|-------|--------------|-----------|
| `$space-8` | Follow repo convention; `16px` only when configured conversion is verified | Follow repo convention |
| Font sizes | Follow repo convention and build conversion | Follow repo convention |
| Border radius | `px` | `px` |

Do not assume `px` converts to `rpx`. Verify the framework and build configuration first. For native miniapps, follow the existing `rpx` and `px` strategy. For Taro or uni-app, confirm conversion and selector behavior in the generated WeChat output.

### Color Consistency

- Both platforms import the same token values
- Dark mode: miniapp uses system dark mode detection via `Taro.getSystemInfoSync().theme`; web uses `prefers-color-scheme` media query
- If the project does not have dark mode, ensure all text/background combinations meet WCAG AA contrast (4.5:1 body, 3:1 large text)

## Component Design Patterns

### Cards

```scss
.card {
  background: $surface-card;
  border-radius: $radius-xl;
  padding: $space-8;
  border: 1px solid $border-default;
  box-shadow: $shadow-xs;
}
```

Variants may include warm or elevated surfaces when they match the product. Use glass effects only after verifying WebView or miniapp runtime support and providing an opaque fallback.

### Buttons

- Primary: brand gradient or solid brand color, white text, `$radius-lg`
- Ghost: white bg with brand border, brand text
- Pill: `$radius-full` for chip-like actions
- All buttons: minimum touch target 44px height on miniapp
- Reset native button defaults in one shared class: `box-sizing`, margin, padding, inherited font, border, `::after`, text alignment, and a predictable base line height
- For a single-line text button, explicitly set `display: flex`, `align-items: center`, `justify-content: center`, a touch-safe height, and `line-height: 1` or `1.2`
- For icon-and-text buttons, use flex alignment and `gap`; give the icon a fixed box instead of aligning with spaces or text glyph baselines
- Do not rely on inherited page `line-height`, native `<button>` padding, or matching `line-height` to a fixed height
- After changing a shared button reset, audit every button variant, including save, delete, tab, chip, sheet, and modal actions

### Dynamic Content And Layout Stability

- Reserve layout space for helper text, time ranges, validation messages, and other content that appears during a toggle when neighboring cards should remain still
- Prefer keeping the node mounted with `min-height`, `opacity`, and `visibility` changes instead of `wx:if` or `display: none`
- Reserve enough height for the maximum expected wrapped lines, not only the current copy
- Keep card padding and inter-card spacing stable across states
- Animate opacity or color before animating layout dimensions; if height must animate, use an explicit measured range

### Modals And Native Layers

- Treat `canvas`, `map`, `video`, `camera`, `textarea`, and similar native surfaces as separate rendering layers
- When a modal opens, hide or unmount any native surface that can overlap it; a high `z-index` alone is not a reliable fix
- Use a full-screen fixed backdrop with `inset: 0`, an isolated stacking context, and an explicit top-layer value
- Give modal cards dedicated opaque surface, border, shadow, and overlay tokens for both light and dark themes; do not depend on a translucent glass card over busy content
- Apply the same button-centering contract to every modal action

### Tags And Badges

- Small pill shape: `$radius-full`, padding `4px 12px`
- Use semantic background colors at low opacity: `rgba($color-primary, 0.12)` with full-strength text
- Status colors: success/warning/error each with `0.08` opacity bg + full text

### Data Display (KPI Cards, Metrics)

- Primary metric: large font, bold, `$text-primary` color
- Label: small font, `$text-tertiary`
- Trend indicator: `$color-success` for positive, `$color-error` for negative
- **Invert for cost metrics**: cost down = good = green
- Right-align numbers in tables and metric grids

### Empty And Loading States

- Skeleton: shimmer animation with `background-size: 400% 100%`, speed 2-3s
- Empty: centered text with muted color, optional illustration
- Loading: `Taro.showLoading` for full-page; inline skeleton for partial

## Visual Quality Checklist

Before marking any miniapp UI work as done:

- [ ] **System reuse**: Existing tokens, primitives, units, and visual conventions were inspected before introducing new ones
- [ ] **Tokens**: Repeated or semantic values reuse the project system; deliberate local values are explained
- [ ] **Color hierarchy**: Semantic colors and the product's established hierarchy are preserved
- [ ] **Typography**: Clear size/weight hierarchy; readable body copy and explicit compact control line heights
- [ ] **Spacing**: Consistent scale; related items closer than unrelated groups
- [ ] **Touch targets**: All interactive elements >= 44px height
- [ ] **Control alignment**: Every text or icon-and-text button is visually centered in default, pressed, disabled, and modal states
- [ ] **Dynamic layout**: Toggling helper text, theme details, validation, or optional controls does not move unrelated content unexpectedly
- [ ] **Overlay layering**: Modals and sheets cover or explicitly hide conflicting native components
- [ ] **States**: Loading skeleton, empty state, and error state all designed
- [ ] **Contrast**: Text meets WCAG AA (4.5:1 body, 3:1 large)
- [ ] **Platform constraints**: No forbidden CSS features used (check table above)
- [ ] **Cross-platform**: If shared component, verified on both miniapp and web
- [ ] **Animation**: Subtle and purposeful; respects platform performance limits
- [ ] **Runtime proof**: Capture screenshots or equivalent visual evidence for the affected state matrix

## Integration With wechat-miniapp-delivery

When used together with the delivery skill:

- **Plan stage**: Design skill provides the visual scope and token requirements
- **Implement stage**: Developer follows token, control, dynamic-layout, and overlay patterns from this skill
- **Validate stage**: Visual Quality Checklist and the affected runtime state matrix run as acceptance gates
- **Release stage**: No visual regressions from the design standard

The delivery skill's PM role can reference this checklist in the acceptance matrix. The developer role should import the token file and follow component patterns. The QA role can use the checklist for visual inspection.

## Read References

- Open `references/runtime-ui-quality-gates.md` for the reusable audit workflow, native button reset, layout-stability patterns, modal layering decision tree, framework notes, and acceptance matrix.
