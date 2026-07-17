# Design Systems — Deep Reference

This is the deep reference for building, maintaining, and evolving design systems. Read this when creating design tokens, structuring component libraries, setting up design system governance, or documenting component behavior.

---

## 1. What Makes a Design System

A design system is not a UI kit. It's not a component library. It's not a style guide. It is **all three, plus governance, plus people, plus process**.

### The Three Pillars

| Pillar | What it is | Ownership |
|---|---|---|
| **Guidelines** | Principles, patterns, voice & tone, usage rules | Design |
| **UI Components** | Reusable coded components + Figma components | Engineering + Design |
| **Assets** | Icons, illustrations, imagery, fonts | Design |

### The System Maturity Model (Nathan Curtis)

**Level 1: Ad Hoc**
- Teams build everything independently
- No shared components, no pattern library
- Every team reinvents the wheel
- Inconsistent user experience

**Level 2: Aware**
- Someone creates an inventory of common patterns
- Teams know what should be shared but don't enforce it
- Some shared Sketch/Figma symbols exist but aren't coded
- Documentation is sparse or outdated

**Level 3: Catalyzed**
- A core set of components exists in a shared library
- One or two dedicated people maintain it (part-time)
- Basic guidelines exist for top 20 components
- Teams are onboarded but contribute inconsistently

**Level 4: Managed**
- Full design token system (primitive → semantic → component)
- Versioned releases with changelogs
- Dedicated design + engineering leadership
- Contribution process with design reviews
- Accessibility is part of the component spec

**Level 5: Systemic**
- Design and engineering co-own the system
- Cross-product consistency (multi-brand support)
- Figma components reflect code reality (or vice versa)
- Design tools (Figma variables, component properties) are fully leveraged
- Automated testing for accessibility and visual regression
- System evolves based on usage data and user feedback

---

## 2. Design Token Architecture

Design tokens are the atomic values that define the visual language.

### 2.1 Token Hierarchy

```
┌─────────────────────────────┐
│     Primitive Tokens        │  — Raw values (color #0066FF, spacing 16px)
├─────────────────────────────┤
│     Semantic Tokens         │  — Maps primitives to purpose (color-primary)
├─────────────────────────────┤
│     Component Tokens        │  — Component-specific (button-primary-bg)
├─────────────────────────────┤
│     Theme/Context Tokens     │  — Override for dark/high-contrast modes
└─────────────────────────────┘
```

### 2.2 Token Naming Convention

Use a consistent, descriptive naming system:

**Pattern**: `{category}-{property}-{variant}-{state}`

Examples:
```
color-bg-primary-default
color-text-inverse-hover
spacing-inset-md
shadow-elevation-sm
border-radius-input-sm
typography-size-body-lg
```

**Token category types**:
```
color       — Backgrounds, text, borders, icons
spacing     — Margin, padding, gap, inset
typography  — Font family, size, weight, line height, letter spacing
shadow      — Box shadows, elevation
border      — Width, radius, style
opacity     — Disabled, overlay, muted
z-index     — Stacking order
animation   — Duration, easing
breakpoint  — Responsive breakpoints
size        — Width, height constraints
```

### 2.3 Primitive Tokens

Raw values with no semantic meaning. These are the building blocks.

```json
{
  "blue-50": "#E8F0FE",
  "blue-100": "#D2E3FC",
  "blue-200": "#A8C7FA",
  "blue-300": "#76A9FA",
  "blue-400": "#3B82F6",
  "blue-500": "#1A73E8",
  "blue-600": "#1557B0",
  "blue-700": "#0F3B78",
  "blue-800": "#0A2540",
  "gray-50": "#F8F9FA",
  "gray-100": "#F1F3F4",
  ...
  "spacing-1": "4px",
  "spacing-2": "8px",
  "spacing-3": "12px",
  "spacing-4": "16px",
  "spacing-5": "20px",
  "spacing-6": "24px",
  "spacing-8": "32px",
  "spacing-10": "40px",
  "spacing-12": "48px",
  "spacing-16": "64px",
  ...
  "font-size-xs": "12px",
  "font-size-sm": "14px",
  "font-size-base": "16px",
  "font-size-lg": "18px",
  "font-size-xl": "20px",
  "font-size-2xl": "24px",
  ...
}
```

### 2.4 Semantic Tokens

Map primitives to contexts. These are the tokens designers and developers actually reference.

```json
{
  "color-primary-default": "{blue-500}",
  "color-primary-hover": "{blue-600}",
  "color-primary-active": "{blue-700}",
  "color-primary-soft": "{blue-50}",
  
  "color-bg-primary": "{white}",
  "color-bg-secondary": "{gray-50}",
  "color-bg-tertiary": "{gray-100}",
  
  "color-text-primary": "{gray-900}",
  "color-text-secondary": "{gray-700}",
  "color-text-disabled": "{gray-400}",
  "color-text-inverse": "{white}",
  
  "color-border-default": "{gray-200}",
  "color-border-focus": "{blue-400}",
  "color-border-error": "{red-500}",
  
  "spacing-gap-xs": "{spacing-2}",
  "spacing-gap-sm": "{spacing-3}",
  "spacing-gap-md": "{spacing-4}",
  "spacing-gap-lg": "{spacing-6}",
  
  "shadow-sm": "0 1px 2px rgba(0,0,0,0.05)",
  "shadow-md": "0 4px 6px rgba(0,0,0,0.07)",
  "shadow-lg": "0 10px 15px rgba(0,0,0,0.1)",
  
  "radius-sm": "4px",
  "radius-md": "8px",
  "radius-lg": "12px",
  "radius-full": "9999px"
}
```

### 2.5 Theming with Tokens

For dark mode or brand theming, override semantic tokens:

```json
// Light theme (default)
{
  "color-bg-primary": "{white}",
  "color-text-primary": "{gray-900}"
}

// Dark theme
{
  "color-bg-primary": "{gray-900}",
  "color-text-primary": "{gray-50}"
}

// High-contrast theme
{
  "color-bg-primary": "{white}",
  "color-text-primary": "{black}"
}
```

---

## 3. Component Architecture

### 3.1 Component Classification

| Type | Description | Examples | Composition |
|---|---|---|---|
| **Primitives** | Atomic building blocks | Button, Input, Icon, Text | Do not contain other components |
| **Patterns** | Multi-primitive compositions | SearchBar (Input + Icon + Button) | Compose primitives |
| **Templates** | Layout-level compositions (no content) | PageHeader, CardGrid, DataTable | Compose patterns |
| **Features** | Business-logic components | AccountSummary, ProductCard | Compose patterns + templates + data |

### 3.2 Component Design Rules

**1. Single Responsibility**
- A Button does on thing: trigger an action. Don't make Buttons that look like links, don't add form submission logic to an icon.

**2. Every State Must Be Designed**
| State | Definition | Example |
|---|---|---|
| **Default** | Normal, ready state | Primary button filled |
| **Hover** | Cursor over the element | Slight darkening |
| **Active/Pressed** | Mouse down on element | Even darker + slight scale down |
| **Focus Visible** | Keyboard focus | 2px focus ring at 3:1 contrast |
| **Disabled** | Cannot interact | 40% opacity, no pointer cursor |
| **Loading** | Action in progress | Spinner replacing text |
| **Success** | Action completed | Checkmark flash, then revert or proceed |
| **Error** | Action failed | Error state styling |
| **Skeleton** | Content loading (composite) | Gray placeholder shapes |

**3. State Contracts (Document Behavior)**
```
Button:
- Disabled: 40% opacity, no hover/focus/active styles
- Disabled: cannot receive keyboard focus
- Disabled: tabindex="-1" or disabled attribute
- Loading: icon changes to spinner, text hidden
- Loading: disabled during loading state
```

**4. Composition over Props Bloat**
```jsx
// ❌ Bad: Too many props on one component
<Button variant="primary" size="lg" iconPosition="right" isLoading hasDropdown isDestructive />

// ✅ Good: Composable primitives
<ButtonGroup>
  <Button variant="primary" icon={Icon.Save}>Save</Button>
  <SplitButton variant="primary">
    <Button>Save</Button>
    <Dropdown items={[saveAs, saveCopy]} />
  </SplitButton>
</ButtonGroup>
```

### 3.3 Component Documentation Template

Every component should document:

```
# [Component Name]

## Purpose
[One-sentence description of what this component does]

## When to use
[Scenarios where this component is the right choice]

## When not to use
[Scenarios where a different component should be used — and which one]

## Anatomy
[Visual breakdown of the component's parts with labels]

## States
[All states listed with visual examples]

## Behavior
[Interaction details: click, keyboard, animation, screen reader]

## Accessibility
[ARIA roles, keyboard navigation, focus management, labels]

## Responsive behavior
[How it adapts across breakpoints]

## Content guidelines
[Character limits, text case, wording patterns]

## Related components
[Links to similar or complementary components]
```

---

## 4. Design System Governance

### 4.1 Roles & Responsibilities

| Role | Responsibilities |
|---|---|
| **Design System Lead** | Vision, roadmap, prioritization, stakeholder buy-in |
| **Component Designer** | Visual design, interaction, states, documentation |
| **Component Engineer** | Implementation, API design, performance, testing |
| **Designer (consumer)** | Use system correctly, request changes, contribute patterns |
| **Engineer (consumer)** | Implement using system, report bugs, contribute fixes |

### 4.2 Contribution Process

1. **Request** — Anyone identifies a gap or improvement
2. **Triage** — System team reviews. Is this solving one team's problem or a general pattern? Is it in scope?
3. **Design review** — Designer creates component proposal. Reviewed by system team for consistency and scalability.
4. **Engineering review** — API, accessibility, performance, and code quality review.
5. **Beta** — Component released as experimental/alpha. Used by 1-2 teams with close monitoring.
6. **Stable** — Production release. Fully documented. Breaking changes require deprecation cycle.

### 4.3 Versioning & Release

Follow semantic versioning:
- **Major**: Breaking changes (component renamed, API changed, token removed)
- **Minor**: New components, new features, non-breaking additions
- **Patch**: Bug fixes, accessibility improvements, documentation updates

**Deprecation cycle**:
1. Add deprecation notice in documentation and code
2. Keep old version for 2 minor releases
3. Provide migration guide and codemod
4. Remove in next major release

---

## 5. Design Tools & Code Sync

### 5.1 Token Management in Figma

- Use **Figma variables** for design tokens (primitive + semantic collections)
- Create **modes** for themes (light, dark, high-contrast)
- Bind component properties to variables (not hardcoded values)
- Use scopes to restrict where variables can be applied

### 5.2 Component Management

- Use **variants** for component states (hover, focused, disabled, etc.)
- Use **component properties** for text, boolean, and instance swap controls
- Create **component documentation** within Figma (description, usage notes)
- Use **slots** for flexible content injection

### 5.3 Code–Design Alignment

- Single source of truth: Tokens should be defined once and consumed by both Figma and code
- Use tools like **Style Dictionary** to transform tokens into platform-specific formats
- Write **Code Connect** files to link Figma components to code snippets
- Run visual regression tests to catch unintended visual changes

---

## 6. Design System Anti-patterns

| Anti-pattern | Description | Solution |
|---|---|---|
| **Component bloat** | One component with 50+ props handling every edge case | Compose smaller components; use slots |
| **Copy-paste system** | Consumers copy the component and modify it locally | Reduce friction to request changes; better documentation |
| **Design system as a blocker** | Every change must go through the system team | Empower contributors; clear contribution process |
| **Premature abstraction** | Abstracting too early before patterns are proven | Build 2-3 real implementations before abstracting |
| **Documentation rot** | Docs outdated the day they're written | Treat docs as part of the release; update alongside code |
| **Accessibility afterthought** | Adding a11y at the end (or not at all) | Ship components only when all states + a11y are complete |
| **No deprecation process** | Breaking changes surprise consumers | Clear versioning + migration guide + deprecation warnings |

---

## When to Read This File

Read `design-systems.md` when:
- Building a new design system from scratch
- Auditing and evolving an existing design system
- Defining token architecture and naming conventions
- Creating component documentation and behavior specs
- Setting up design system governance and contribution processes
- Making decisions about tools and code synchronization

**Document reference**: Design tokens, component architecture, system governance, tooling
**Last updated**: July 2026
