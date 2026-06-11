# adaptive-design-guidance Specification

## Purpose
Define how the design skill preserves established project systems and applies fallback guidance only when a repository lacks reusable conventions.
## Requirements
### Requirement: Existing design systems take precedence
The design skill SHALL inspect and reuse existing project tokens, component primitives, units, build conversion, and visual conventions before introducing fallback guidance.

#### Scenario: Project already has tokens
- **WHEN** a miniapp repository defines established color, spacing, typography, radius, or component tokens
- **THEN** the skill preserves and extends that system instead of requiring a new token file or unrelated migration

### Requirement: Bundled values are fallback examples
The design skill MUST label bundled colors, spacing scales, typography values, ratios, and component styles as optional starting points for projects without an established system.

#### Scenario: Project has no design foundation
- **WHEN** no reusable design tokens or component conventions exist
- **THEN** the skill may propose a minimal fallback system appropriate to the product context

### Requirement: Platform rules are configuration-aware
The design skill SHALL condition unit conversion, line height, advanced CSS, and framework-specific guidance on the actual build configuration and runtime support.

#### Scenario: Taro conversion is disabled or customized
- **WHEN** a project does not use default Taro px transformation
- **THEN** the skill does not assume px values will convert to rpx

#### Scenario: Compact control text
- **WHEN** text is inside a button, chip, tab, or other compact control
- **THEN** the skill permits a compact explicit line height while still requiring visual centering
