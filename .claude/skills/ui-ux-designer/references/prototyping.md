# Prototyping — Deep Reference

This is the deep reference for prototyping methods, fidelity levels, prototyping tools, and design handoff. Read this when creating prototypes, deciding fidelity level, or preparing designs for handoff.

---

## 1. What Is a Prototype?

A prototype is a tangible representation of a design idea, created to answer a specific question. The fidelity should match the question.

**Charles Eames**: "A prototype is the first full-scale and usually functional form of a new type or design." — In UX, prototypes don't have to be full-scale or functional. They just need to answer the question.

---

## 2. Fidelity Levels

### 2.1 No Fidelity — Paper & Pen

| Attribute | Details |
|---|---|
| **Time to create** | 2-30 minutes |
| **Best for** | Early ideation, team alignment, quick exploration |
| **Cost to change** | Seconds |
| **What it tests** | Concept, flow, content structure |

**Best practices**:
- Use fat markers (prevents getting into details)
- Draw screens on sticky notes for easy rearrangement
- "Wizard of Oz" prototype: hand-act the "animations" by sliding paper
- Great for co-creation: give stakeholders a marker and have them sketch

### 2.2 Low Fidelity — Wireframes (Greyscale, Boxes, Lines)

| Attribute | Details |
|---|---|
| **Time to create** | 1-4 hours |
| **Best for** | Layout, structure, hierarchy, flow |
| **Cost to change** | Minutes |
| **What it tests** | Content placement, navigation, information architecture |

**Tools**: Excalidraw, Balsamiq, Figma (wireframe mode), hand-drawn scanned

**Best practices**:
- No color, no real images, no detailed typography
- Use "lorem ipsum" or gray rectangles for content
- Focus on one thing: layout or flow, not both
- Annotate behaviors with arrows and notes

**What NOT to test with wireframes**:
- Visual hierarchy driven by color
- Emotional response to the design
- Typographic readability
- Interactive feel

### 2.3 Mid Fidelity — Clickable Wireframes / Grey-box Prototypes

| Attribute | Details |
|---|---|
| **Time to create** | 4-20 hours |
| **Best for** | Navigation, interaction flow, task completion testing |
| **Cost to change** | Hours |
| **What it tests** | User flow, comprehension, task success |

**Tools**: Figma, Sketch + InVision, Adobe XD, Balsamiq

**Best practices**:
- Use consistent spacing (roughly aligned, not pixel-perfect)
- Use real content (no lorem ipsum for testing)
- Connect screens with basic interactions (click to next screen)
- Cover the happy path + 1-2 error states

**What NOT to test with mid-fi**:
- Visual polish / design quality
- Micro-interactions
- Emotional delight

### 2.4 High Fidelity — Realistic Mockups

| Attribute | Details |
|---|---|
| **Time to create** | 20-80 hours |
| **Best for** | Visual design validation, stakeholder buy-in, handoff |
| **Cost to change** | Days |
| **What it tests** | Visual hierarchy, brand feeling, trust, detailed usability |

**Tools**: Figma, Sketch, Framer, ProtoPie, Principle

**Best practices**:
- Use real design tokens (spacing, color, typography from design system)
- Design every state (default, hover, active, disabled, loading, empty, error, success)
- Include motion / transitions
- Use real data (not fake placeholder content)

**What NOT to do with hi-fi**:
- Don't spend time on hi-fi before answering flow / structure questions
- Don't use hi-fi prototypes as production code specs (too much translation required)

### 2.5 Functional Prototypes / Code Prototypes

| Attribute | Details |
|---|---|
| **Time to create** | 20-200 hours |
| **Best for** | Micro-interactions, complex interactions, technical feasibility, advanced user testing |
| **Cost to change** | Hours to days |
| **What it tests** | Realistic interaction feel, performance, actual behavior |

**Tools**: HTML/CSS/JS, Framer, SwiftUI, ProtoPie, Principle

**When to choose code prototypes**:
- Testing micro-interactions that can't be faked in Figma
- Complex animations with physics or gesture tracking
- Technical feasibility proof (can this even be built?)
- When stakeholder or engineer buy-in requires "real" behavior

---

## 3. Prototyping Decision Tree

```
What question are we trying to answer?
│
├── "Is this the right concept / direction?"
│   → Low-fi wireframes / sketches
│
├── "Does the flow make sense?"
│   → Clickable mid-fi prototype
│
├── "Can users complete the task?"
│   → Mid-fi or hi-fi (with real content)
│
├── "Does the visual design work?"
│   → Hi-fi mockup (static)
│
├── "How does the animation feel?"
│   → Functional prototype or hi-fi with animation tools
│
├── "Will users trust this?"
│   → Hi-fi prototype for trust testing
│
├── "Which version performs better?"
│   → A/B test with hi-fi or functional prototype
│
└── "Can we build this?"
    → Functional / code prototype for feasibility
```

---

## 4. Interactive Prototyping Tools Comparison

| Tool | Fidelity | Interaction complexity | Learning curve | Platform | Price |
|---|---|---|---|---|---|
| **Figma** | Low-High | Medium (basic transitions, smart animate) | Low | Web, Mac, Win | Free tier + paid |
| **ProtoPie** | Mid-High | Very high (sensors, conditional logic, variables) | Medium | Mac, Win | Paid |
| **Principle** | Mid-High | High (timeline-based, springs, drag) | Medium | Mac only | Paid |
| **Framer** | Mid-High | High (code extends, React-based) | Medium-High | Web, Mac, Win | Free tier + paid |
| **Axure RP** | Low-Mid | Very high (logic, variables, conditionals) | Medium-High | Mac, Win | Paid |
| **UXPin** | Low-High | Medium (branching, conditional logic) | Medium | Web | Paid |
| **HTML/CSS/JS** | Max | Max (real code) | High | Any | Free |

---

## 5. Testing with Prototypes

### 5.1 Preparation

- Define the test goal (what decision will this inform?)
- Write task scenarios, not instructions
- Recruit 5 users per round
- Decide: moderated vs unmoderated, in-person vs remote

### 5.2 What to Test at Each Level

| Fidelity | What you can reliably test | What you can't |
|---|---|---|
| **Paper** | Concept comprehension, flow logic | Visual appeal, interactive feel |
| **Low-fi wireframes** | Navigation, content structure, hierarchy | Brand emotion, trust |
| **Mid-fi clickable** | Task completion, findability, comprehension | Visual polish, delight |
| **Hi-fi mockup** | Visual hierarchy, brand perception, trust | Interaction feel, performance |
| **Code prototype** | Real interaction, performance, micro-behaviors | Production scalability |

### 5.3 The 5-User Rule

Jakob Nielsen's famous finding: 5 users per round finds ~85% of usability issues. After 5, you see diminishing returns.

**What this means**:
- Run multiple rounds (test → fix → test again) rather than one round with 15 users
- 5 users × 3 rounds > 15 users once
- Plan for iterative testing, not one-shot validation

---

## 6. Design Handoff

### 6.1 What a Good Handoff Includes

- **Design files**: Organized, layered, named consistently
- **Specifications**: Measurements, spacing, color, typography values
- **States**: All states for every component
- **Responsive behavior**: How it adapts to different screen sizes
- **Edge cases**: Empty states, error states, loading states, overflow behavior
- **Accessibility notes**: Keyboard navigation, focus order, ARIA roles, contrast info
- **Assets**: Export-ready icons, images, and illustrations (SVGs preferred)
- **Annotations**: Notes on behavior, not just "what it looks like"

### 6.2 Handoff Checklist

- [ ] Design files are organized and componentized
- [ ] All states designed (default, hover, active, focus, disabled, loading, empty, error, success)
- [ ] Responsive behavior specified (breakpoints, reflow rules)
- [ ] Error states and error messages written
- [ ] Empty states designed with content
- [ ] Loading states designed (skeleton or spinner)
- [ ] Edge cases considered (truncation, overflow, missing data)
- [ ] Color values specified (hex, token names)
- [ ] Typography specified (font, size, weight, line height, letter spacing)
- [ ] Spacing values specified (margins, padding, gaps, token names)
- [ ] Icons exported in SVG format
- [ ] Images optimized and exported at correct resolutions
- [ ] Interactive behaviors annotated (hover, toggle, transition, animation)
- [ ] Keyboard navigation and focus order documented
- [ ] Accessibility notes included (ARIA labels, roles, alt text, contrast)
- [ ] Design system components used where possible, new ones flagged

### 6.3 Common Handoff Mistakes

| Mistake | Solution |
|---|---|
| Different spacing in design vs code | Use design tokens (shared reference) |
| Missing error/loading/empty states | Design all states before calling it done |
| Ambiguous responsive behavior | Design at 2-3 breakpoints, document rules |
| Handing off pixel-perfect but untested designs | Test before handoff, not after |
| No failure path design | What happens when things break? Design it |
| Over-specifying layouts (exact pixel positions) | Use auto-layout / constraints that adapt |

---

## When to Read This File

Read `prototyping.md` when:
- Deciding what fidelity level to prototype at
- Choosing a prototyping tool for a specific need
- Preparing for a usability testing session
- Planning a design handoff to development
- Building a design-to-development workflow

**Document reference**: Prototyping methods, fidelity levels, tools comparison, handoff best practices
**Last updated**: July 2026
