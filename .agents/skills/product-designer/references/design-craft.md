# Design Craft — Visual Design, Interaction, Accessibility & Systems

The practical craft of product design: how to make things that look polished, feel intuitive, build trust, work for everyone, and scale across a product. This is the "how" of design — the tangible skills and knowledge every product designer needs.

---

## 1. Visual Design Foundations

### Typography

Good typography is 90% of good visual design. It communicates hierarchy, personality, trust, and reading comfort.

#### Key Principles

| Principle | What it means | How to apply |
|---|---|---|
| **Hierarchy** | Not all text is equal | Use size, weight, and color to signal importance. Headlines > subheads > body > captions |
| **Readability** | Text must be comfortable to read | Body text: 16-18px (web), 15-17px (mobile). Line height: 1.4-1.6. Line length: 50-75 characters |
| **Consistency** | Same type treatment = same meaning | Define a type scale and reuse it systematically |
| **Whitespace** | Space around text is as important as the text | Adequate margins and padding improve readability more than font choice |

#### Type Scale (Recommended 4pt Base)
```text
Caption:   12px / 16px line-height
Body:      16px / 24px line-height
Body Lg:   18px / 28px line-height
Subtitle:  20px / 28px line-height
H4:        24px / 32px line-height
H3:        32px / 40px line-height
H2:        40px / 48px line-height
H1:        48px / 56px line-height
```

#### Do's and Don'ts
- ✅ Use at most 2 typefaces unless the brand system truly requires more
- ✅ Use system fonts when performance and neutrality matter
- ❌ Don't use all caps for body text
- ❌ Don't justify text on web

### Color

Color creates hierarchy, communicates meaning, signals trust, and establishes brand.

#### Building a Color System

| Role | What it's for | Properties |
|---|---|---|
| **Primary** | Brand color, main CTAs | Distinctive, high contrast |
| **Secondary** | Supporting accent | Complementary to primary |
| **Neutral** | Text, surfaces, borders | Flexible across light/dark usage |
| **Semantic** | Success, warning, error, info | Meaningful and consistent |

#### Accessibility-first color
- **Text contrast:** 4.5:1 minimum for normal text, 3:1 for large text
- **Interactive elements:** 3:1 minimum against adjacent colors
- **Don't rely on color alone** — pair color with icons, text, pattern, or shape

#### Trust signals in color
- Use semantic colors consistently; changing meanings weakens confidence.
- In payments, settings, or consent flows, prefer calm, plain colors over aggressive marketing color treatment.
- Avoid false urgency through alarming reds or deceptive contrast games.

### Spacing & Layout

#### The 8px Grid
Use increments of 8px for margins, padding, and spacing. This creates rhythm and consistency.

```text
Spacing scale: 2, 4, 8, 12, 16, 20, 24, 32, 40, 48, 56, 64, 80, 96...
```

#### Layout best practices
- **Content width:** 640-720px for reading, 960-1200px for dashboards
- **Margins:** 16-24px on mobile, 24-80px on desktop
- **Grid:** Use 4, 6, or 12 columns depending on complexity
- **Breathing room:** If elements overlap in meaning or attention, hierarchy breaks

### Visual Hierarchy

The arrangement of elements to signal their importance. Users should know what to look at first, second, and third.

**How to create hierarchy:**
1. **Size** — Most important = largest
2. **Color / contrast** — More contrast = more attention
3. **Position** — First scan zone matters
4. **Whitespace** — More space around = more importance
5. **Weight** — Bold beats regular

**The squint test:** Squint at the design. Can you still identify the primary action and focal point?

### Personality and confidence in visuals

A polished UI does not need to be loud. Personality should reinforce the product's role, not distract from it.

Use visual style to answer:
- Should this feel calm or energetic?
- Should this feel precise, warm, serious, or playful?
- Is the current visual treatment helping trust or just adding noise?

Guidelines:
- Use restraint in high-stakes moments: billing, privacy, permissions, account deletion
- Use expressive brand elements where the user benefits from warmth, delight, or orientation
- Prefer confidence and clarity over novelty in product UI

---

## 2. Interaction Design Principles

### Hick's Law
The time it takes to make a decision increases with the number and complexity of choices.

- Reduce options on critical screens
- Use progressive disclosure for advanced settings
- Group related choices rather than presenting them flat

### Fitts' Law
The time to acquire a target depends on its size and distance.

- Make frequent actions larger and easier to reach
- Touch targets: at least 44×44px on mobile, 32×32px on desktop
- Place the primary action where the flow naturally ends

### Gestalt Principles

| Principle | What it means | Design application |
|---|---|---|
| **Proximity** | Nearby things feel related | Group controls and data intentionally |
| **Similarity** | Similar things are perceived as related | Reuse styles for repeated meaning |
| **Closure** | People fill in missing parts | Simple marks often outperform detailed icons |
| **Continuity** | The eye follows smooth paths | Align elements to support scan paths |
| **Figure-ground** | People separate foreground from background | Use contrast and layering to clarify interactivity |

### Cognitive Load

| Type | What it is | How to reduce |
|---|---|---|
| **Intrinsic** | Inherent task complexity | Break tasks into steps, chunk information |
| **Extraneous** | Design-generated effort | Remove clutter, use conventions, clarify wording |
| **Germane** | Effort spent learning | Support onboarding, repetition, and mastery |

**Goal:** Minimize extraneous load so users can spend effort on the real task.

### Micro-interactions

Small, functional animations and state changes that communicate behavior.

| Use case | Example | Principle |
|---|---|---|
| Button feedback | Button depresses on click | Immediate response |
| State transition | Card expands to detail view | Continuity and orientation |
| Progress | Loading bar fills | Reduces uncertainty |
| Error | Inline shake or highlight | Clear feedback |
| Attention | Subtle pulse on a new message | Noticeable without hijacking attention |

**Rule of thumb:** Micro-interactions should be fast, purposeful, and never block completion.

### Empty States, Error States & Loading

These are first-class design surfaces, not edge cases.

#### Empty states
- Explain what belongs here
- Give a clear next step
- Reduce first-use anxiety
- Use illustration or tone only if it supports orientation, not decoration alone

#### Error states
- Say what went wrong in plain language
- Say what the user can do next
- Avoid blaming the user when the system is at fault
- Preserve their data whenever possible

#### Loading states
- Prefer skeletons over generic spinners when structure is known
- For waits over a few seconds, indicate progress or expected duration
- Use loading to reassure, not just stall

### UX writing / microcopy fundamentals

Words are part of the interface, not labels attached afterward.

| Goal | Good microcopy does this |
|---|---|
| **Clarity** | Uses the user's language, not internal jargon |
| **Confidence** | Tells users what will happen next |
| **Recovery** | Explains errors and next steps plainly |
| **Trust** | Avoids manipulative or exaggerated language |
| **Brevity** | Says only what is useful in the moment |

Examples:
- ❌ "Submit"
- ✅ "Send request"

- ❌ "Something went wrong"
- ✅ "We couldn't save your changes. Try again or keep editing."

- ❌ "Continue"
- ✅ "Review pricing"

Use copy to reduce ambiguity, not to patch over confusing structure.

---

## 3. Trust, Safety, and Emotional Interaction Design

Trust is a craft problem. It is communicated through hierarchy, copy, defaults, timing, recovery, and user control.

### Consent and disclosure patterns

Good disclosure answers:
- what is happening
- why it is needed
- what changes if the user says yes
- how they can change their mind later

Bad disclosure hides cost, consequence, or data use behind vague words like "continue" or "optimize your experience."

### Destructive-action safeguards

For delete, irreversible edits, or account closure:
- use clear labels, not generic confirmations
- surface impact before the action
- offer undo where possible
- use confirmation prompts only when the action is truly risky
- avoid overwarning on low-risk actions; unnecessary friction weakens attention

### Confidence and explainability cues

Users trust interfaces that set accurate expectations.

Use these patterns:
- preview before commit
- summary before payment or submission
- confidence or source cues for AI-generated outputs
- visible status after an action succeeds or fails
- clear ownership of what the system did vs what the user did

### Fair choice architecture

A choice is unfair when one option is visually or behaviorally privileged in a manipulative way.

Red flags:
- giant accept button vs tiny decline text
- shame-based opt-outs
- confusing default settings
- hidden prices revealed too late
- forced continuity disguised as convenience

### Emotional calibration by moment

| Moment | Best tone |
|---|---|
| **First use** | welcoming, low-pressure, orienting |
| **Error** | calm, accountable, recovery-oriented |
| **Success** | affirming, not noisy |
| **Sensitive consent** | plain, exact, respectful |
| **High-stakes workflow** | steady, confidence-building |

A useful rule: delight is optional; reassurance is not.

---

## 4. Accessibility (a11y)

Accessibility is not a feature — it is a baseline design requirement. Inclusive products work better for everyone.

### WCAG guidelines (quick reference)

| Level | Conformance | Impact |
|---|---|---|
| **A** | Minimum | Covers basic needs |
| **AA** | Standard target | Required for most real products |
| **AAA** | Advanced | Aspirational in many contexts |

### Key WCAG 2.1 AA requirements

#### Perceivable
- Color contrast: 4.5:1 for normal text, 3:1 for large text
- Non-text contrast: 3:1 for UI components
- Text alternatives: alt text, labels, names
- Captions for video content

#### Operable
- Keyboard navigation for everything interactive
- Visible focus indicators
- Touch targets at least 44×44px on mobile
- No keyboard traps

#### Understandable
- Consistent navigation and behavior
- Clear error identification
- Predictable interactions and labels

#### Robust
- Semantic HTML where applicable
- ARIA only where necessary and meaningful

### Inclusive design practices
- Design for permanent, temporary, and situational constraints
- Let users reduce motion or sensory load
- Write in plain language by default
- Never use color as the only meaning channel

### Accessibility audit checklist (quick)

```text
□ Color contrast meets WCAG target
□ All interactive elements have visible focus states
□ All images have meaningful alt text
□ Icon-only buttons have aria-labels
□ Touch targets are large enough
□ Tab order follows visual order
□ Heading hierarchy is logical
□ Error messages are associated with inputs
□ Motion respects reduced-motion preferences
□ Screen reader navigation works without traps
```

---

## 5. Design Systems

A design system is a shared language for visual and interaction behavior across a product. It enables consistency, speed, and quality at scale.

### Layers of a design system

```text
                   Products
                      ↑
                Component Library
                      ↑
              Design Patterns (recipes)
                      ↑
               Design Tokens (atoms)
                      ↑
             Principles & Guidelines
```

#### 1. Principles & guidelines
- design values
- writing style guide
- accessibility standards
- trust and behavior norms

#### 2. Design tokens
```text
Colors:      --color-primary: #0066FF
Typography:  --font-body: 16px/1.5 'Inter', sans-serif
Spacing:     --space-md: 16px
Shadows:     --shadow-sm: 0 1px 3px rgba(0,0,0,0.1)
Radii:       --radius-sm: 4px
Motion:      --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1)
```

Tokens connect design and code through a shared vocabulary.

#### 3. Design patterns
Examples:
- search experience
- onboarding flow
- empty-state pattern
- settings layout
- destructive-action confirmation pattern
- consent / permission prompt pattern

#### 4. Component library
- **Atoms:** Button, Input, Label, Icon
- **Molecules:** FormField, SearchBar, ToggleRow
- **Organisms:** Navigation, DataTable, Modal

### Building a component: what to define

```text
Component: Button

Properties:
├── Variants:  Primary | Secondary | Ghost | Danger
├── Sizes:     sm | md | lg
├── States:    Default | Hover | Active | Disabled | Focus | Loading
├── Content:   Text | Icon + Text | Icon only
├── Usage:     When to use each variant
└── Behavior:  What happens on click, focus, keyboard, loading, error
```

### Advanced system guidance

#### Accessibility by default
Build focus, contrast, labels, and keyboard behavior into components from the start. Accessibility should not be added at the screen level only.

#### Behavior contracts
A component spec should document:
- visual states
- interaction states
- keyboard behavior
- screen-reader expectations
- empty / loading / error behavior where relevant

#### Variant discipline
Too many variants weaken the system. Add a variant only when it supports a recurring, meaningfully different use case.

#### Avoid manipulative defaults
System components should not encode dark patterns by default. For example, consent components should not assume pre-checked boxes or visually buried declines.

### Design system maturity model

| Stage | Characteristics | Next step |
|---|---|---|
| **1. None** | Every team designs from scratch | Audit patterns and create shared files |
| **2. Library** | Shared design components, limited code parity | Add tokens and implementation alignment |
| **3. System** | Tokens + components in design and code | Add docs, governance, contribution rules |
| **4. Platform** | Teams contribute, system scales | Add tooling, adoption metrics, theming |
| **5. Ecosystem** | Multi-product, mature governance | Extend documentation and feedback loops |

### Governance model

| Approach | How it works | Best for |
|---|---|---|
| **Centralized** | One team owns all components | Small teams, single product |
| **Federated** | Teams contribute with review | Larger orgs, many products |
| **Hybrid** | Core team owns foundations; product teams extend carefully | Most common at scale |

---

## 6. Information Architecture (IA)

Information architecture is how content and functionality are organized, labeled, and navigated.

### IA design process
1. Content audit
2. User research
3. Sitemap / tree
4. Navigation design
5. Labeling
6. Tree testing

### Common IA patterns

| Pattern | Use when | Example |
|---|---|---|
| **Hierarchical** | Simple nested content | Docs, company site |
| **Flat** | Few categories, low depth | Simple settings |
| **Hub and spoke** | Task-based multi-step experiences | Checkout, onboarding |
| **Faceted** | Many attributes and filters | Search, e-commerce |

### Navigation best practices
- Global nav: 5-7 items max in primary view
- Breadcrumbs: useful for deep hierarchies
- Search: prominent when content volume is high
- Footer: expanded navigation for long-scroll contexts

### Progressive disclosure in IA

Do not show every option at once if the user only needs a subset now.

Use progressive disclosure when:
- the beginner path is simple, but expert controls exist
- advanced settings are useful but not primary
- risky actions need explanation before commitment

---

## 7. Prototyping & Fidelity

### When to use each fidelity level

| Fidelity | What it is | Best for |
|---|---|---|
| **Low-fi** | Sketches, wireframes, grayscale structures | Early concept, flow, IA, shaping |
| **Mid-fi** | Clean layout, real-ish content, basic interaction | Usability testing, comprehension, stakeholder alignment |
| **High-fi** | Detailed UI, real content, rich interaction | Final validation, tone, trust, handoff |
| **Code** | Built in UI code | Realistic behavior, implementation preview |

**Rule of thumb:** Use the lowest fidelity that gets you the learning you need.

### Prototyping best practices
- Test early: low-fi reveals flow issues faster
- Don't polish a bad idea
- Test with real content whenever possible
- Design the non-happy states before claiming the flow is done
- Document interactions, not just screens

### Matching fidelity to the question

| Question | Appropriate fidelity |
|---|---|
| Is the concept worth exploring? | Low-fi |
| Can users find and complete the task? | Low to mid-fi |
| Do users understand the copy and consequences? | Mid-fi |
| Does this feel trustworthy, reassuring, or premium? | Mid to high-fi |
| Is this ready for engineering handoff? | High-fi or code |
