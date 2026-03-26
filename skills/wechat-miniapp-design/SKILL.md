---
name: wechat-miniapp-design
description: Design system and visual quality gate for WeChat miniapp development. Use when building or reviewing miniapp pages, components, or styles. Enforces design token discipline, miniapp CSS constraints, cross-platform consistency, and visual quality standards. Works alongside wechat-miniapp-delivery as the design arm of the delivery pipeline.
---

# WeChat Miniapp Design

Use this skill as the design quality gate for miniapp UI work. It ensures every page and component follows a consistent design system, respects miniapp platform constraints, and meets visual quality standards before delivery.

This skill complements `wechat-miniapp-delivery`: delivery handles the workflow (plan → implement → validate → release), design handles the visual standard (tokens → layout → components → quality check).

## When This Skill Activates

- Building or modifying a miniapp page or component
- Writing or reviewing SCSS/CSS for miniapp
- Creating shared cross-platform UI (miniapp + web)
- Any task involving "样式", "设计", "UI", "页面", "组件", or visual appearance

## Design Thinking For Miniapp

Before writing styles, answer:

1. **Context** — Is this a data-dense dashboard, a content page, a form, or a marketing surface? Each has different density and rhythm needs.
2. **Platform** — Miniapp-only, web-only, or cross-platform shared? This determines which CSS features and units are available.
3. **Hierarchy** — What should the user see first, second, third? Establish visual weight before picking colors and sizes.
4. **Consistency** — Does this page reuse existing tokens and patterns, or does it need new ones? Prefer reuse.

## Design Token System

### Rule: Single Source Of Truth

Every miniapp project should have one token file (e.g. `design-tokens.scss`) imported by all page styles. Never hardcode colors, spacing, or font sizes directly in component SCSS.

### Color Tokens

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

Follow the **60-30-10 rule**:
- 60% — Page background and neutral surfaces
- 30% — Cards, secondary surfaces, borders
- 10% — Brand accent (buttons, links, highlights)

### Spacing Scale

Use a consistent scale based on 4px increments:

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

### Typography Scale

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
- Chinese content: `line-height >= 1.6`
- Limit to 2 font families (display + body)
- Display font for titles and KPI numbers; system font for body text

### Border Radius Scale

```scss
$radius-sm: 8px;     // Code blocks, small tags
$radius-md: 12px;    // Images, inputs
$radius-lg: 16px;    // Buttons, cards (small)
$radius-xl: 20px;    // Cards (standard)
$radius-2xl: 24px;   // Cards (featured)
$radius-3xl: 32px;   // Full-page modals
$radius-full: 999px; // Pills, chips, avatars
```

### Shadow Scale

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
| `z-index` | Native components (`map`, `video`, `canvas`, `textarea`) always render above normal layers |
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
| `$space-8` | `16px` (Taro converts to rpx) | `16px` or `1rem` |
| Font sizes | `px` in SCSS, Taro handles rpx conversion | `px` or `rem` |
| Border radius | `px` | `px` |

Rule: write shared styles in `px` and let the platform build tool handle conversion.

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

Variants: glass (backdrop-filter + semi-transparent bg), warm (gradient bg for data items), elevated (stronger shadow for modals).

### Buttons

- Primary: brand gradient or solid brand color, white text, `$radius-lg`
- Ghost: white bg with brand border, brand text
- Pill: `$radius-full` for chip-like actions
- All buttons: minimum touch target 44px height on miniapp
- Remove default `::after` border on Taro `<Button>`

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

- [ ] **Tokens**: No hardcoded hex values or magic numbers in component styles
- [ ] **Color hierarchy**: 60-30-10 rule maintained; semantic colors used correctly
- [ ] **Typography**: Clear size/weight hierarchy; `line-height >= 1.6` for Chinese
- [ ] **Spacing**: Consistent scale; related items closer than unrelated groups
- [ ] **Touch targets**: All interactive elements >= 44px height
- [ ] **States**: Loading skeleton, empty state, and error state all designed
- [ ] **Contrast**: Text meets WCAG AA (4.5:1 body, 3:1 large)
- [ ] **Platform constraints**: No forbidden CSS features used (check table above)
- [ ] **Cross-platform**: If shared component, verified on both miniapp and web
- [ ] **Animation**: Subtle and purposeful; respects platform performance limits

## Integration With wechat-miniapp-delivery

When used together with the delivery skill:

- **Plan stage**: Design skill provides the visual scope and token requirements
- **Implement stage**: Developer follows token system and component patterns from this skill
- **Validate stage**: Visual Quality Checklist runs as part of the acceptance gate
- **Release stage**: No visual regressions from the design standard

The delivery skill's PM role can reference this checklist in the acceptance matrix. The developer role should import the token file and follow component patterns. The QA role can use the checklist for visual inspection.
