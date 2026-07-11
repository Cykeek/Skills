# Accessibility (WCAG) — Deep Reference

This is the deep reference for web accessibility standards, inclusive design practices, and assistive technology considerations. Read this when auditing designs for accessibility, planning inclusive features, or ensuring WCAG compliance.

---

## 1. WCAG 2.2 Overview

WCAG 2.2 has 4 principles: **Perceivable, Operable, Understandable, Robust** (POUR). Each has guidelines, and each guideline has testable success criteria at levels A (minimum), AA (recommended minimum), and AAA (enhanced).

### Compliance Levels
- **Level A**: Must be satisfied. Minimum level of accessibility. Without these, some users cannot access content at all.
- **Level AA**: Should be satisfied. Removes significant barriers. This is the legal standard for most countries (Section 508, EN 301 549, ADA).
- **Level AAA**: May be satisfied for specific content. Highest level. Not required for full compliance as some content types cannot satisfy all AAA criteria.

---

## 2. Perceivable (Information must be presentable to users)

### 2.1 Text Alternatives (Guideline 1.1)

**1.1.1 Non-text Content (A)**

All non-text content must have a text alternative that serves the equivalent purpose.

**Implementation guide**:
- **Informative images**: Provide alt text describing the information the image conveys
- **Decorative images**: Use empty alt text (`alt=""`) or CSS background images
- **Functional images** (icons that link/button): Alt text describes the function, not the image (e.g., "Search" not "magnifying glass")
- **Complex images** (charts, graphs): Provide both alt text and a longer description (e.g., data table nearby)
- **CAPTCHAs**: Provide multiple modalities (visual + audio)
- **SVG icons**: Use `<title>` for simple icons, `role="img"` with `aria-label` for interactive ones

**Examples**:
```
✅ Good: <img src="chart.png" alt="Bar chart showing Q3 sales increased 23% from Q2">
✅ Icon: <button aria-label="Search"><svg>...</svg></button>
✅ Decorative: <img src="background-pattern.jpg" alt="">
❌ Bad: <img src="chart.png" alt="Chart">
❌ Bad: <img src="button.png" alt="Click here">
```

### 2.2 Time-based Media (Guideline 1.2)

| Criteria | Level | Requirement |
|---|---|---|
| **1.2.1 Audio-only / Video-only** | A | Transcript for audio; text/audio description for video |
| **1.2.2 Captions (prerecorded)** | A | Captions for all prerecorded video with audio |
| **1.2.3 Audio description / Media alternative** | A | Audio description or full text alternative for video |
| **1.2.4 Captions (live)** | AA | Real-time captions for live video broadcasts |
| **1.2.5 Audio description (prerecorded)** | AA | Audio description for all prerecorded video content |

### 2.3 Adaptable (Guideline 1.3)

Content must make sense when presented differently (e.g., by a screen reader).

**1.3.1 Info and Relationships (A)**
- Use semantic HTML (`<nav>`, `<main>`, `<aside>`, `<header>`, `<footer>`, `<section>`, `<article>`)
- Headings must form a logical hierarchy (h1 → h2 → h3, never skip levels)
- Tables: use `<th>` for headers, `scope` attribute, `<caption>` for title
- Lists: use `<ul>` / `<ol>` / `<dl>` for list content
- Form inputs: always associate `<label>` with input via `for` attribute or nesting

**1.3.2 Meaningful Sequence (A)**
- Content should make sense in code order even without CSS
- Tab order should match visual order

**1.3.3 Sensory Characteristics (A)**
- Don't rely on shape, size, visual location, or sound alone to convey information
- "Click the button on the right" → "Click the 'Submit' button"

**1.3.4 Orientation (AA)**
- Content not locked to portrait or landscape unless essential (e.g., piano app)
- Must work in both orientations

**1.3.5 Identify Input Purpose (AA)**
- Use `autocomplete` attribute for common form fields (name, email, address, phone)
- Enables browser autofill and password managers
- Full list: https://www.w3.org/TR/WCAG22/#input-purposes

### 2.4 Distinguishable (Guideline 1.4)

**1.4.1 Use of Color (A)**
- Color must not be the only way to convey information
- Always pair color with text, icon, pattern, or underline
- ✅ Links are blue + underlined
- ❌ Red text alone to indicate required fields
- ❌ Green/red dots alone to indicate status

**1.4.2 Audio Control (A)**
- Auto-playing audio must have pause/stop/mute control
- Any audio lasting > 3 seconds must have a control mechanism

**1.4.3 Contrast (Minimum) (AA)**
- Text contrast: **4.5:1** minimum for normal text (< 18px or < 14px bold)
- Large text: **3:1** minimum (≥ 18px or ≥ 14px bold)
- Logos and decorative text are exempt

**1.4.4 Resize Text (AA)**
- Text can be resized to 200% without loss of content or functionality
- Responsive text (no horizontal scroll at 200%)

**1.4.5 Images of Text (AA)**
- Use actual text, not images of text, unless the visual presentation is essential (logo, brand)

**1.4.10 Reflow (AA)** — NEW in WCAG 2.1
- Content works in 320px width without horizontal scrolling
- Requires responsive design, not just pinch-zoom

**1.4.11 Non-text Contrast (AA)** — NEW in WCAG 2.1
- UI components and graphical objects: **3:1** contrast against adjacent colors
- Covers icons, buttons, form controls, focus indicators, charts

**1.4.12 Text Spacing (AA)** — NEW in WCAG 2.1
- No loss of content when user overrides:
  - Line height: 1.5× font size
  - Paragraph spacing: 2× font size
  - Letter spacing: 0.12× font size
  - Word spacing: 0.16× font size

**1.4.13 Content on Hover or Focus (AA)** — NEW in WCAG 2.1
- Tooltips/popups that appear on hover must be:
  - Dismissible (can close without moving focus)
  - Hoverable (cursor can move onto the tooltip without it disappearing)
  - Persistent (doesn't disappear on its own while hovered/focused)

---

## 3. Operable (UI and navigation must be usable)

### 3.1 Keyboard Accessible (Guideline 2.1)

**2.1.1 Keyboard (A)**
- All functionality must be operable via keyboard
- No keyboard traps (focus can be moved away from any element)
- This includes: links, buttons, forms, media controls, drag-and-drop

**2.1.2 No Keyboard Trap (A)**
- Focus can move away from any component using standard keyboard navigation
- Never trap focus in a modal without a clear escape (Escape key, close button)

**2.1.4 Character Key Shortcuts (A)** — NEW in WCAG 2.1
- If a single character key shortcut exists, user must be able to:
  - Turn it off
  - Remap it (with modifier key)
  - Activate only on focus
- Prevents accidental activation from typing

### 3.2 Enough Time (Guideline 2.2)

**2.2.1 Timing Adjustable (A)**
- Any time limit must allow user to turn off, adjust (×10), or extend it
- Exceptions: real-time events, essential time limits (exam)

**2.2.2 Pause, Stop, Hide (A)**
- Moving, blinking, scrolling, or auto-updating content must have pause/stop/hide controls if:
  - Starts automatically AND
  - Lasts > 5 seconds AND
  - Is presented in parallel with other content

**2.2.6 Timeouts (AAA)**
- Warn users about data loss due to inactivity
- Show how long the session stays active before timeout
- Recommended: provide a way to extend the session

### 3.3 Seizures and Physical Reactions (Guideline 2.3)

**2.3.1 Three Flashes or Below Threshold (A)**
- Content must not flash more than 3 times per second
- Below general flash threshold (red flash threshold also applies)

### 3.4 Navigable (Guideline 2.4)

**2.4.1 Bypass Blocks (A)**
- Skip links to bypass repeated content (navigation menus)
- Typically hidden skip-to-main-content link at page top

**2.4.2 Page Titled (A)**
- Each page has a descriptive, unique title
- `<title>` reflects page purpose and context

**2.4.3 Focus Order (A)**
- Focusable elements receive focus in a meaningful sequence
- Tab order matches visual reading order

**2.4.4 Link Purpose (In Context) (A)**
- Purpose of each link can be determined from link text alone or from link text + context
- Avoid "Click here", "Read more", "Learn more" without context

**2.4.5 Multiple Ways (AA)**
- More than one way to find content (search, navigation, sitemap, links)
- Exceptions: pages in a linear process (checkout steps are exempt)

**2.4.6 Headings and Labels (AA)**
- Headings and labels describe topic or purpose clearly
- Descriptive, not clever or vague

**2.4.7 Focus Visible (AA)**
- Keyboard focus indicator must be visible
- Never use `outline: none` without providing an alternative focus style
- Focus ring: minimum 2px thick, 3:1 contrast with adjacent colors

**2.4.11 Focus Not Obscured (Minimum) (AA)** — NEW in WCAG 2.2
- When an element receives focus, it must not be entirely hidden by other content (e.g., sticky headers, cookie banners)
- The focused element must be fully visible or at least partially visible

**2.4.12 Focus Not Obscured (Enhanced) (AAA)** — NEW in WCAG 2.2
- Focused element must be fully visible, not partially obscured

**2.4.13 Focus Appearance (AAA)** — NEW in WCAG 2.2
- Focus indicator must be:
  - At least as thick as a 2px border
  - Contrast ratio of at least 3:1 between same pixels in focused and unfocused states

### 3.5 Input Modalities (Guideline 2.5) — NEW in WCAG 2.1

**2.5.1 Pointer Gestures (A)**
- All functionality using path-based or multi-point gestures must have a single-point alternative
- Swipe → button; pinch → +/- button; multi-finger → single tap

**2.5.2 Pointer Cancellation (A)**
- Prevent accidental activation. Down-event should not execute action.
- Use "up" event (mouseup, touchend) not "down" event (mousedown, touchstart) for primary actions

**2.5.3 Label in Name (A)**
- Accessible name of a component must include the visible text label
- If button says "Search", `aria-label="Search"` not `aria-label="Find"`

**2.5.4 Motion Actuation (A)** — NEW in WCAG 2.1
- Functionality triggered by device motion (shake, tilt) must have a UI alternative
- Users who can't move the device must still access the feature

**2.5.7 Dragging Movements (AA)** — NEW in WCAG 2.2
- All dragging functionality must have a single-point alternative (tap, click, keyboard)
- Drag-and-drop must also work with select + move (no dragging required)

**2.5.8 Target Size (Minimum) (AA)** — NEW in WCAG 2.2
- Target size: **24×24px** minimum
- Exceptions: inline links, essential targets, legal documents
- Previously WCAG 2.1 had this at AAA; WCAG 2.2 moved it to AA

---

## 4. Understandable (Information and operation must be understandable)

### 4.1 Readable (Guideline 3.1)

**3.1.1 Language of Page (A)**
- Page language declared in `<html lang="en">`
- Language must match the default content language

**3.1.2 Language of Parts (AA)**
- Language changes within content must be identified
- `<span lang="fr">Bonjour</span>` within an English page

### 4.2 Predictable (Guideline 3.2)

**3.2.1 On Focus (A)**
- No unexpected context changes when an element receives focus
- Focusing a dropdown shouldn't submit the form

**3.2.2 On Input (A)**
- No unexpected context changes when input changes
- Changing a dropdown selection shouldn't automatically navigate unless clearly communicated

**3.2.3 Consistent Navigation (AA)**
- Navigation repeats in the same order on every page
- Consistent positioning and labeling across pages

**3.2.4 Consistent Identification (AA)**
- Same functionality is identified the same way across pages
- E.g., "Search" is always in the same place with the same icon + label

**3.2.6 Consistent Help (A)** — NEW in WCAG 2.2
- If a page has help mechanisms (chat, contact info, FAQ link), place them in the same relative order on every page

### 4.3 Input Assistance (Guideline 3.3)

**3.3.1 Error Identification (A)**
- When an input error is detected, identify which field has the error
- Describe the error in text (not just red border)

**3.3.2 Labels or Instructions (A)**
- Labels or instructions provided when content requires user input
- Required fields indicated clearly
- Format hints provided (e.g., "MM/DD/YYYY")

**3.3.3 Error Suggestion (AA)**
- Suggestions provided for fixing detected errors
- "Password must be at least 8 characters" (not "Invalid password")

**3.3.4 Error Prevention (Legal, Financial, Data) (AA)**
- For transactions, legal agreements, or data deletion:
  - Reversible (undo possible)
  - Checked (user reviews before finalizing)
  - Confirmed (explicit confirmation required)

**3.3.7 Accessible Authentication (A)** — NEW in WCAG 2.2
- Authentication does not rely on cognitive function tests (recalling password, solving puzzles)
- Exceptions: object recognition, personal content identification, or alternative authentication methods
- Supports password managers (autofill) as a compliant path

**3.3.8 Accessible Authentication (Enhanced) (AAA)** — NEW in WCAG 2.2
- No cognitive function test at all, even with alternatives

---

## 5. Robust (Content must work with assistive technologies)

### 5.1 Compatible (Guideline 4.1)

**4.1.1 Parsing (A)**
- Elements have complete start/end tags
- Elements are nested according to specifications
- No duplicate attributes (especially `id`)
- **Note**: This was deprecated in WCAG 2.2 but maintained for backward compatibility

**4.1.2 Name, Role, Value (A)**
- All UI components have programmatically determinable name, role, and value
- Custom components must implement appropriate ARIA roles, states, and properties

**4.1.3 Status Messages (AA)** — NEW in WCAG 2.1
- Status messages must be announced by screen readers without receiving focus
- Use `role="status"` (polite), `role="alert"` (assertive), `aria-live="polite"`, or `aria-live="assertive"`
- Examples: "5 results found", "Item added to cart", search count updates

---

## 6. ARIA (Accessible Rich Internet Applications)

### 6.1 ARIA Landmarks

Use landmark roles to help screen reader users navigate:

```html
<header role="banner">
<nav role="navigation" aria-label="Main">
<main role="main">
<form role="search" aria-label="Search">
<aside role="complementary">
<footer role="contentinfo">
```

**Rule**: Use native HTML semantic elements first (`<nav>`, `<main>`, `<header>`, `<footer>`). Add `role` only when HTML5 semantic elements can't convey the role.

### 6.2 Key ARIA Patterns

| Pattern | Role | States/properties |
|---|---|---|
| **Tabs** | `tablist`, `tab`, `tabpanel` | `aria-selected`, `aria-controls`, `aria-labelledby`, `tabindex` |
| **Accordion** | `button` (trigger) | `aria-expanded`, `aria-controls`, `aria-labelledby` |
| **Modal** | `dialog` | `aria-modal="true"`, `aria-labelledby`, `aria-describedby`, `role="document"` |
| **Alert** | `alert` | `role="alert"` (assertive live region) |
| **Progress** | `progressbar` | `aria-valuenow`, `aria-valuemin`, `aria-valuemax`, `aria-label` |
| **Error** | — | `aria-invalid="true"`, `aria-describedby` (error message ref) |
| **Menu** | `menubar`, `menu`, `menuitem` | `aria-haspopup`, `aria-expanded` |
| **Tooltip** | `tooltip` | Controlled by `aria-describedby` on trigger |

### 6.3 ARIA Live Regions

| Role/Attribute | Announcement behavior | Use case |
|---|---|---|
| `aria-live="polite"` | Announces when idle | Dynamic content updates, chat messages, search results |
| `aria-live="assertive"` | Announces immediately | Alerts, critical status changes, error banners |
| `role="status"` | Polite live region | Status messages, loading states |
| `role="alert"` | Assertive live region | Error messages, important warnings |
| `aria-atomic="true"` | Announce entire region (not just changed parts) | For screen readers to read whole content instead of partial changes |

### 6.4 ARIA Best Practices

- **First rule of ARIA**: Don't use ARIA if you can use native HTML semantics
- **No ARIA is better than bad ARIA**: Incorrect ARIA can be worse than no ARIA
- **Use ARIA to supplement, not replace**: Fix HTML structure first, then add ARIA if needed
- **Test with real screen readers**: Automated tools find ~30% of issues
- **Keep it simple**: Complex ARIA patterns are hard to implement correctly

---

## 7. Inclusive Design Practices

### 7.1 The Disability Spectrum

| Disability type | Permanent | Temporary | Situational |
|---|---|---|---|
| **Vision** | Blind | Cataract recovery | Bright sunlight, shattered glasses |
| **Hearing** | Deaf | Ear infection | Noisy environment |
| **Motor** | Missing limb | Arm injury | Holding a baby |
| **Cognitive** | ADHD, dyslexia | Concussion | Sleep deprivation, distraction |

**Design implication**: Inclusive design doesn't just serve people with permanent disabilities — it serves everyone at different times.

### 7.2 Inclusive Design Principles (Microsoft Inclusive Design Toolkit)

1. **Recognize exclusion**: Exclusion happens when we solve problems using our own biases. Design with diverse needs from the start.
2. **Solve for one, extend to many**: Designing for a person with a permanent disability often results in a better experience for everyone.
3. **Learn from diversity**: Human diversity reveals constraints that make products better for all.

### 7.3 Testing with Assistive Technology

**Recommended screen readers for testing**:
- **VoiceOver** (macOS/iOS) — Built-in, no installation needed
- **NVDA** (Windows) — Free, widely used by developers
- **JAWS** (Windows) — Most widely used by blind users in enterprise
- **TalkBack** (Android) — Built into Android

**Testing protocol**:
1. Turn off monitor (test with screen reader only)
2. Complete typical user tasks
3. Note any confusion, missing labels, dead ends
4. Test with keyboard only (no mouse)
5. Test with voice control

---

## 8. Accessibility Audit Checklist

### Quick Audit (15-minute high-level scan)

- [ ] Page has a descriptive `<title>` and proper language attribute
- [ ] All images have appropriate alt text (or `alt=""` for decorative)
- [ ] Skip link present and functional
- [ ] Tab order follows visual order
- [ ] Focus indicator visible (minimum 2px, 3:1 contrast)
- [ ] Color contrast passes 4.5:1 body / 3:1 large text
- [ ] All form inputs have associated labels
- [ ] Headings form a logical hierarchy
- [ ] Links are distinguishable (not just color)
- [ ] No content flashes more than 3 times/second
- [ ] Pages work at 200% zoom without content loss
- [ ] Content reflows at 320px width
- [ ] Auto-playing media can be paused
- [ ] Forms have clear error identification
- [ ] Touch targets ≥ 24×24px (AA WCAG 2.2)

### Deep Audit (per screen/component)

- [ ] All interactive elements keyboard accessible
- [ ] No keyboard traps (modal focus trap must have escape)
- [ ] Screen reader announces all content correctly
- [ ] Custom components have proper ARIA roles/states
- [ ] Dynamic content is announced via live regions
- [ ] Dragging has single-point alternative
- [ ] Motion actuation has UI alternative
- [ ] Authentication supports password managers
- [ ] Status messages announced without focus change
- [ ] Tooltips persist, dismissible, hoverable
- [ ] Reduced motion respected (`prefers-reduced-motion`)
- [ ] Color + text/icon used together (not color alone)

---

## When to Read This File

Read `accessibility.md` when:
- Auditing or designing for WCAG compliance
- Planning accessibility remediation
- Designing components with proper ARIA attributes
- Setting up keyboard navigation and focus management
- Writing accessible labels, error messages, and alt text
- Testing with assistive technology
- Planning inclusive design strategy

**Document reference**: WCAG 2.2 A/AA compliance, ARIA, inclusive design, accessibility testing
**Last updated**: July 2026
