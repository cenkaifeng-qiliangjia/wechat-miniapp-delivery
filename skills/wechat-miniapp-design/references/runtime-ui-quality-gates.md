# Runtime UI Quality Gates

Use this reference for miniapp UI work involving buttons, text alignment, conditional content, cards whose height changes, theme controls, sheets, modals, or native components such as `canvas`, `map`, `video`, `camera`, and `textarea`.

## Contents

1. Failure Patterns
2. Audit Workflow
3. Button And Label Alignment
4. Dynamic Layout Stability
5. Modal And Native-Layer Safety
6. Framework Notes
7. Acceptance Matrix

## Failure Patterns

The following failures often pass static review and only appear in the miniapp runtime:

| Symptom | Root cause | Reusable fix |
| --- | --- | --- |
| Text sits high or low inside save, delete, chip, or modal buttons | Native button padding and line height combine with inherited page typography | Reset native button defaults once, then use explicit flex centering and a local line height for each single-line control |
| Selecting a theme reveals a time range and the page jumps | Conditional content is mounted with `wx:if` or `display: none`, changing the card height | Keep a reserved slot mounted and toggle `opacity` plus `visibility`; define a stable `min-height` |
| A modal backdrop appears behind a timer ring or media surface | `canvas` or another native component is not in the same stacking context as normal views | Hide or unmount the native component while the modal is open; then apply an explicit top-layer backdrop |
| A translucent modal looks visually mixed with the page below | A reusable glass-card surface is too transparent for a blocking dialog | Use dedicated modal surface, overlay, border, and shadow tokens in light and dark themes |
| One reported button is fixed but similar controls remain broken | The patch targets a local selector without auditing shared reset and sibling variants | Search all button usages and validate the full control family after changing the shared base |

## Audit Workflow

### 1. Inventory UI Risk Surfaces

Search the files owned by the current change:

```bash
rg -n "<button|<Button|button\\b|wx:if|v-if|show.*modal|canvas|map|video|camera|textarea" \
  miniprogram src pages components
```

Adjust paths to the repository. Classify each relevant result as:

- text-only button
- icon-only button
- icon-and-text button
- stateful control: selected, pressed, disabled, loading
- conditional region that changes intrinsic height
- sheet or modal
- native component that may escape normal stacking

### 2. Inspect Shared Styles First

Find the global button reset and reusable control components before editing a local selector:

```bash
rg -n "clean-button|button-reset|::after|align-items|justify-content|line-height" \
  miniprogram src styles components
```

If no shared reset exists, add the smallest project-appropriate reset. Do not duplicate a full reset into every page.

### 3. Define The State Matrix

Use only states relevant to the change, but do not omit the state that exposed the bug:

| Surface | Required states |
| --- | --- |
| Button | default, pressed, disabled, loading if supported |
| Theme selector | each theme choice, optional time range hidden and visible |
| Modal | closed, open, light theme, dark theme, native surface mounted |
| Card with optional content | content absent, one line, maximum expected wrapped lines |
| Cross-platform component | WeChat target plus every other supported shell touched by the change |

### 4. Verify Rendered Behavior

- Use WeChat Developer Tools or the repo-standard preview path.
- Toggle the changed state repeatedly, not only once.
- Confirm that unrelated controls keep the same position.
- Confirm that labels remain visually centered, not merely mathematically centered in CSS.
- Capture screenshots or equivalent evidence for the affected states.
- Use a real device when native layers, safe areas, font rendering, or WebView behavior are involved.

## Button And Label Alignment

### Native Button Reset

Native miniapp buttons include platform defaults. A shared reset should usually cover:

```css
.button-reset {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  color: inherit;
  font-family: inherit;
  line-height: 1.2;
  text-align: center;
  background: transparent;
  border: 0;
  border-radius: 0;
}

.button-reset::after {
  border: 0;
}
```

Adapt the class name and syntax to the project. Preserve any existing accessibility, pressed-state, or disabled-state behavior.

### Single-Line Text Buttons

Use explicit layout on the concrete button variant:

```css
.save-button {
  display: flex;
  min-height: 72rpx;
  align-items: center;
  justify-content: center;
  line-height: 1;
}
```

Apply this contract to:

- save and confirm actions
- delete and destructive actions
- chips and segmented controls
- tabs with text
- sheet and modal actions
- compact list-row actions

Do not use a large page-level Chinese body `line-height` for controls. Body copy may need `1.6`; a single-line button label usually needs `1` to `1.2` inside a flex-centered box.

### Icon And Text Buttons

Use a stable icon box and flex gap:

```css
.action-button {
  display: flex;
  min-height: 88rpx;
  align-items: center;
  justify-content: center;
  gap: 12rpx;
  line-height: 1.2;
}

.action-button-icon {
  display: flex;
  width: 32rpx;
  height: 32rpx;
  align-items: center;
  justify-content: center;
  flex: none;
}
```

Do not align icon and label with spaces, punctuation, or glyph-specific offsets.

### Button Acceptance

Check:

- label center at default font scale
- label center in disabled and pressed states
- icon and label share one visual center
- multiline labels are intentional; otherwise constrain to one line
- touch target remains at least 44px
- shared reset does not break icon-only controls or switches

## Dynamic Layout Stability

### Reserve The Optional Slot

When helper copy should appear without moving neighboring cards, keep it in the layout:

```xml
<view class="theme-hint {{showThemeHint ? 'is-visible' : ''}}">
  <text>06:30-18:30 follows the light theme</text>
</view>
```

```css
.theme-hint {
  display: flex;
  min-height: 38rpx;
  align-items: center;
  opacity: 0;
  visibility: hidden;
  transition: opacity 160ms ease;
}

.theme-hint.is-visible {
  opacity: 1;
  visibility: visible;
}
```

Use `aria-hidden` or the framework equivalent when hidden content should not be exposed to accessibility services.

### Choose The Right Strategy

Use reserved space when:

- the content is short and bounded
- toggling should not move cards below
- the hidden space does not create a confusing gap

Use explicit height animation when:

- the content can expand significantly
- the product intentionally communicates expansion
- the project can measure the content height reliably

Use conditional mounting when:

- layout movement is expected and desirable
- the hidden content is expensive to keep mounted
- accessibility or focus behavior requires removal

Do not add arbitrary outer margin as the only fix. First stabilize the changing region; then tune card spacing for visual rhythm.

## Modal And Native-Layer Safety

### Layering Decision Tree

1. Identify whether the page contains `canvas`, `map`, `video`, `camera`, `textarea`, `<web-view>`, or another native surface.
2. If no native surface exists, use the normal fixed-backdrop stacking pattern.
3. If a native surface exists, hide or unmount it while the modal is open.
4. If the platform requires the content to remain visible, use the supported cover-layer component instead of a normal view.
5. Verify on a real device. Simulator stacking is not sufficient evidence.

### Normal Modal Backdrop

```css
.modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 999;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
  background: var(--surface-modal-overlay);
  isolation: isolate;
}

.modal-card {
  position: relative;
  z-index: 1;
  box-sizing: border-box;
  background: var(--surface-modal);
  border: 1px solid var(--border-modal);
  box-shadow: var(--shadow-modal);
}
```

The number `999` is only an application stacking convention. It does not solve native-layer overlap by itself.

### Hide Conflicting Surfaces

Bind native-surface visibility to the modal state:

```xml
<canvas hidden="{{showExitConfirm}}" class="timer-canvas"></canvas>
```

If the runtime still paints a placeholder, also hide the wrapper or switch to conditional mounting. Preserve state needed to restore the surface after the modal closes.

### Modal Surface Tokens

Define dedicated tokens for both themes:

- `--surface-modal`
- `--surface-modal-overlay`
- `--border-modal`
- `--shadow-modal`

Blocking dialogs should remain legible without relying on the page content behind them.

## Framework Notes

### Native WeChat Miniapp

- Reset the native `<button>` and its `::after` border.
- Use WXML class bindings to keep optional slots mounted.
- Treat native-component layering as a runtime concern.

### Taro React

- Apply the same reset to Taro `<Button>`.
- Verify the generated WeChat output, not only the H5 build.
- Keep platform-specific visibility handling behind the component boundary.

### uni-app

- Verify the compiled WeChat target because browser and app previews can hide native button and layer differences.
- Prefer class-based state styling over selectors that may compile inconsistently.

### WebView Shell

- Separate native-shell modals from H5 modals.
- For H5 content, use browser layout rules plus the WebView CSS compatibility gate.
- For shell content, use the native-layer rules in this reference.

## Acceptance Matrix

Record pass or fail with evidence:

| Criterion | Evidence |
| --- | --- |
| All affected text and icon-text controls are vertically centered | screenshots for default and changed states |
| Shared button reset does not regress sibling variants | audited control list plus screenshots |
| Conditional content does not move unrelated cards or controls | before/after positions or repeated-toggle recording |
| Modal fully obscures normal content in light and dark themes | modal-open screenshots |
| Native surfaces do not paint above the modal | real-device or Developer Tools evidence with the native surface mounted |
| Modal actions meet the same alignment and touch-target rules | modal action screenshots and style inspection |

Do not report generic `visual QA passed`. Name the states checked and attach the evidence path or blocker.
