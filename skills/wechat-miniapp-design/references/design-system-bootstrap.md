# Design System Bootstrap

Use this reference only when the project lacks reusable tokens or component foundations. Adapt values to product context, existing units, runtime support, and accessibility needs. These are starting examples, not universal requirements.

## Contents

1. Semantic Tokens
2. Spacing And Typography
3. Radius And Elevation
4. Component Foundations
5. Cross-Platform Notes

## Semantic Tokens

Organize values by role:

```scss
$color-primary: #0b8f7a;
$color-primary-strong: #066758;
$color-primary-soft: rgba(11, 143, 122, 0.12);
$color-success: #1f8a56;
$color-warning: #d27b11;
$color-error: #b43c2f;

$text-primary: #102a43;
$text-secondary: #526680;
$text-tertiary: #6c7787;
$text-on-primary: #fff;

$surface-page: #f5f7fa;
$surface-card: #fff;
$surface-muted: #fafafa;
$border-default: rgba(16, 42, 67, 0.12);
```

Use a small semantic set first. Add a token only when it is reused or represents a product-level role.

The 60-30-10 color ratio can help a new marketing or content surface, but do not enforce it on data-dense tools, accessibility themes, or products with an established hierarchy.

## Spacing And Typography

A compact 4px-based scale is one reasonable starting point:

```scss
$space-1: 4px;
$space-2: 8px;
$space-3: 12px;
$space-4: 16px;
$space-6: 24px;
$space-8: 32px;
```

Keep related items closer than unrelated groups. Use fewer steps until a real layout requires more.

For typography, start with the smallest hierarchy that supports the page:

```scss
$text-caption: 18px;
$text-body: 22px;
$text-emphasis: 24px;
$text-section: 28px;
$text-page: 36px;
```

- Adapt values to the project's conversion and density.
- Prefer the existing system font stack.
- Use a readable line height for multi-line body copy; `1.5-1.7` is a starting range for Chinese prose.
- Use compact explicit line heights for controls and verify visual centering.
- Use weight and spacing as well as size to create hierarchy.

## Radius And Elevation

Start with a restrained scale:

```scss
$radius-control: 12px;
$radius-card: 20px;
$radius-dialog: 24px;
$radius-pill: 999px;

$shadow-card: 0 8px 32px rgba(0, 0, 0, 0.06);
$shadow-dialog: 0 18px 40px rgba(16, 42, 67, 0.12);
```

Use elevation to express hierarchy, not as decoration on every surface.

## Component Foundations

### Card

```scss
.card {
  box-sizing: border-box;
  padding: $space-4;
  background: $surface-card;
  border: 1px solid $border-default;
  border-radius: $radius-card;
  box-shadow: $shadow-card;
}
```

### Button

Build one native reset and a small set of variants:

- primary action
- secondary or ghost action
- destructive action
- compact chip or segmented action
- modal action

All variants inherit the shared alignment and touch-target contract. Avoid separate local resets.

### Status And Data

- Use semantic success, warning, and error colors with sufficient contrast.
- Keep status badges compact and avoid color-only meaning.
- Align comparable numbers consistently.
- For cost metrics, make direction semantics explicit rather than assuming “up” is positive.

### Empty And Loading States

- Use an inline skeleton for partial loading and a page-level loading indicator only for blocking work.
- Provide concise empty-state copy and a recovery action when one exists.
- Design error, denied, retry, and offline states only when the feature can enter them.

## Cross-Platform Notes

- Native miniapp projects commonly use `rpx`; Taro and uni-app conversion depends on configuration.
- Shared H5 and miniapp styles should use the repository's proven unit convention.
- Verify selectors, fonts, gradients, filters, clipping, and CSS variables in the actual WeChat target.
- Glass effects require runtime support and an opaque fallback.
- Dark mode should use the existing theme mechanism rather than introducing a second one.
