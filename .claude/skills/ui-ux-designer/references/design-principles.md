# Design Principles — Deep Reference

This is the deep reference for design principles, cognitive psychology laws, and heuristics frameworks. Read this when you need to ground design decisions in established principles, evaluate interfaces against recognized heuristics, or explain *why* a design works or doesn't work.

---

## 1. Gestalt Principles of Visual Perception

The Gestalt principles describe how the human brain naturally organizes visual elements into groups or unified wholes. They are the foundation of visual communication design.

### 1.1 Proximity

**Principle**: Objects that are close together are perceived as more related than objects that are far apart.

**Practical application**:
- Group related controls and information together using spacing (not boxes)
- Use consistent spacing intervals to signal relationships
- The space between elements *is* the relationship — closer = more related

**Example**: In a contact form, the label should be closer to its input field than to the neighboring field's label. This makes it immediately clear which label belongs to which input.

### 1.2 Similarity

**Principle**: Elements that share visual characteristics (color, shape, size, orientation) are perceived as related.

**Practical application**:
- Use consistent color for all interactive links
- Same icon style = same type of action
- Same card style = same type of content
- Changes in visual treatment signal changes in meaning or function

**Example**: All clickable text should share the same color (typically blue and underlined). If one link is styled differently, users may not recognize it as clickable.

### 1.3 Common Region

**Principle**: Elements within a bounded area are perceived as a group.

**Practical application**:
- Cards, section backgrounds, and borders create containment
- Dropdown menus should appear above every other element to signal they're separate from the background content
- Modals should overlay with a scrim to separate foreground (interaction) from background (context)

**Example**: A pricing table where each plan is inside a card. Users immediately perceive each card as a group of features belonging to one plan.

### 1.4 Closure

**Principle**: The mind tends to perceive complete forms even when parts are missing.

**Practical application**:
- Loading spinners (continuous circle segments that the mind completes)
- Progress indicators showing incomplete steps as outlines and completed steps as filled
- Icon design — simplified shapes that the brain fills in as complete objects
- Minimalist logo design

**Example**: The IBM logo is composed of horizontal stripes — our brain fills in the letterforms.

### 1.5 Figure-Ground

**Principle**: Elements are perceived as either the focus (figure) or the background (ground). The relationship between them determines what draws attention.

**Practical application**:
- Make primary actions distinct from surrounding content
- Use drop shadows and elevation to lift interactive elements
- Modal overlays darken/lighten the background to push it into the "ground", pulling the modal into "figure"
- Cards with shadow elevation separate themselves from the page background

**Example**: A floating action button (FAB) with a drop shadow appears to float above the content — the brain interprets it as a foreground element worthy of attention.

### 1.6 Continuity

**Principle**: The eye follows lines, curves, and aligned elements — preferring smooth, continuous paths over abrupt changes.

**Practical application**:
- Aligned form fields guide the eye downward/forward through the form
- Stepped progress bars guide the eye left to right (or top to bottom)
- Horizontal product rows guide the eye across, suggesting "more in this direction"
- Navigation menus with items on the same horizontal axis feel connected

**Example**: A multi-step checkout form with a horizontal progress bar at the top. The bar's continuous line signals "you're on a path, keep going."

### 1.7 Common Fate

**Principle**: Elements moving together are perceived as related, regardless of their individual visual characteristics.

**Practical application**:
- Animated transitions where elements move in sync (e.g., list items appearing together)
- Hover effects that reveal a group of actions together
- Accordion panels that expand/collapse related content as a group
- Slide-in menus where all items enter with the same motion

**Example**: In a card grid where hovering a card reveals a set of action buttons appearing simultaneously, users perceive all those buttons as related controls for that card.

---

## 2. Cognitive Psychology Laws

### 2.1 Fitts's Law

**Original definition**: The time to acquire a target is a function of the distance to the target and the size of the target.

**Formula**: T = a + b × log₂(D/W + 1), where D = distance to target, W = width of target, a and b are constants.

**UI implications**:
- **Make primary actions large**: The bigger the target, the faster and easier it is to acquire. Primary CTAs should be the largest clickable elements on screen.
- **Place primary actions close**: Reduce the distance to frequently used controls. The corner of the screen is infinitely large (the cursor stops at the edge), so place menus and critical UI along edges.
- **Put destructive actions in hard-to-reach places**: Delete, remove, or dangerous actions should be smaller and require more deliberate movement.
- **Follow the infinite edge principle**: Screen edges and corners act as oversized targets because the cursor physically can't go past them. The Windows Start menu and Mac menu bar leverage this.
- **Mobile considerations**: Fitts's Law applies to thumbs too — make frequently tapped targets large (minimum 44-48px) and place them within easy thumb reach.

**Classic example**: The Mac menu bar is at the very top of the screen, making it an "infinite height" target — you can slam the cursor up without overshooting.

### 2.2 Hick's Law

**Original definition**: Decision time increases logarithmically with the number of choices available.

**Formula**: RT = a + b × log₂(n), where n = number of choices, a and b are constants.

**UI implications**:
- **Limit choices per screen**: Too many options cause analysis paralysis. 3-5 primary choices is a good range for most interfaces.
- **Use progressive disclosure**: Show the most common/default options first, then reveal advanced/complex options on demand (expandable sections, "Advanced settings" links).
- **Group and categorize**: When many options are necessary, group them into meaningful categories. Navigation with 20 items → 4 categories × 5 items each.
- **Prioritize**: Not all choices are equal. The most frequent or important action should be visually prominent (also supports Fitts's Law).
- **The paradox of choice**: More options can lead to less satisfaction even after a choice is made (Barry Schwartz).

**Classic example**: Google's homepage has ~3 visible options (search box, "Google Search" button, "I'm Feeling Lucky"). Compare to Yahoo's cluttered portal page. Google won because it reduced choice to the essential action.

### 2.3 Jakob's Law (Jakob Nielsen)

**Principle**: Users spend most of their time on *other* websites, so they expect your site to work the same way as all the other sites they already know.

**UI implications**:
- **Follow platform conventions**: Shopping cart icon in the top-right corner, logo in the top-left links to home, search in the top-center or top-right. Don't innovate on established patterns.
- **Met expectations = trust**: When users find familiar patterns, they feel competent and confident. Novel patterns require learning — and many users won't bother.
- **Respect mental models**: Users have already developed mental models from dominant platforms. If your CRM looks nothing like Salesforce, expect friction.
- **Innovate on the problem, not the pattern**: Don't put the cart icon in the bottom-left just to be different. Be different where it matters — solve a real problem better than competitors.
- **The innovator's trap**: Many redesigns fail because they change too many conventions at once. If users can't find the search box because you styled it as a circle behind a long-press gesture, you've violated Jakob's Law.

**Classic example**: Amazon's checkout flow has been refined over decades but still follows the same basic pattern: cart → shipping → payment → review → confirm. Changing this established flow would confuse millions of users.

### 2.4 Miller's Law

**Original research**: The average person can hold 7 ± 2 items in their working memory (George Miller, 1956). More recent research suggests the number is closer to 4 ± 1.

**UI implications**:
- **Chunk information**: Group related items into chunks of 5-9 (or better, 3-5). Phone numbers are chunked (555-123-4567 instead of 5551234567).
- **Break complex tasks into steps**: Wizards and multi-step forms keep each screen manageable (3-5 options per step).
- **Navigation limits**: Top navigation works well with 5-7 items. Beyond that, use mega-menus or category grouping.
- **Progressive disclosure**: Show summary first, details on demand. An accordion with 10 items grouped into 3 categories is more usable than a flat list of 10.
- **Reduce short-term memory load**: Don't make users remember information from one screen to the next. Show context — e.g., "You entered: name@email.com" on the confirmation screen.

**Design application**: A settings page with 50 options is overwhelming. Group into 5-7 categories (Account, Privacy, Notifications, Appearance, Language, Billing, About). Within each category, limit to manageable groups.

### 2.5 Serial Position Effect (Primacy & Recency)

**Principle**: Users best remember the first items (primacy) and last items (recency) in a sequence.

**UI implications**:
- **Put most important items first or last**: In navigation, dropdown menus, and lists, the first and last positions carry the most weight.
- **Structure content with the most important information at the top**: Journalistic inverted pyramid — lead with the conclusion.
- **Use "bottom of page" for critical actions**: The "Submit" or "Buy" button is often remembered because it's the last action.
- **Progress bars at both ends**: Show progress at the top (where first seen) and a summary at the bottom (where last seen).

**Example**: In a hamburger menu, the most important items should be at the top (Home, Profile) and the bottom (Settings, Logout) — middle items get less attention.

### 2.6 Doherty Threshold

**Principle**: Productivity soars when a system and its user interact at a pace that ensures neither has to wait on the other (< 400ms response time).

**UI implications**:
- **Optimize perceived performance**: Show instant feedback for user actions — button state change within 50ms, content load within 200ms.
- **Skeleton screens over spinners**: Skeleton screens make content feel faster because they give a sense of progress and structure.
- **Optimistic UI**: For predictable operations (e.g., sending a message), show the result immediately and reconcile in the background.
- **Pre-load the next likely action**: Predict the user's next move and pre-load resources.
- **Dead time is productivity poison**: Any wait over 1 second breaks the flow state.

**Example**: Twitter showing your tweet instantly in the timeline while the server processes it in the background. The user feels the system is instantaneous.

### 2.7 Parkinson's Law (in UX)

**Principle**: Work expands to fill the time available. In UX: if a task takes 5 minutes in the interface but feels like 30, users will perceive the product as slow and frustrating.

**UI implications**:
- **Perceived time is real time**: A 3-second load with no feedback feels like 10 seconds. A 3-second load with a skeleton screen + progress bar feels like 2 seconds.
- **Reduce semantic distance**: The gap between what the user wants to express and what the interface requires them to do. More clicks ≠ more work. More *thinking* = more work.
- **Reduce interaction cost**: Every click, scroll, swipe, and decision adds to perceived time. Remove unnecessary steps.

### 2.8 Tesler's Law (Law of Conservation of Complexity)

**Principle**: Every system has irreducible complexity that must be placed somewhere. The question is not "can we eliminate complexity?" but "who bears it?"

**UI implications**:
- **Put complexity on the system side**: The product and engineers should absorb complexity so the user doesn't have to.
- **Automate what can be automated**: Auto-save, smart defaults, prefilled forms, intelligent suggestions.
- **Design for the 80% case**: Make the common path dead simple. The 20% of complex cases can use advanced features.
- **Smart defaults**: Pre-select the most common choice. Users can override, but most won't need to.

**Classic example**: iPhone vs early smartphones. Early smartphones exposed all complexity to the user (file systems, settings, task killers). The iPhone absorbed most complexity — just tap an app and it works.

---

## 3. Nielsen's 10 Usability Heuristics (Expanded)

### 3.1 Visibility of System Status

The system should always keep users informed about what is going on, through appropriate feedback within reasonable time.

**Implementation checklist**:
- [ ] Does every user action produce a system response?
- [ ] Are there progress indicators for operations taking >1 second?
- [ ] Is the user's current location clearly indicated (breadcrumbs, nav active state)?
- [ ] Are multi-step processes showing progress (step 3 of 5)?
- [ ] Are system status changes communicated (online/offline/away)?

**Examples**: Gmail's "Sending..." → "Sent" animation; LinkedIn's profile strength meter; a checkout progress bar reading "2. Shipping (step 2 of 4)".

### 3.2 Match Between System and the Real World

The system should speak the users' language, with words, phrases, and concepts familiar to the user, rather than system-oriented terms. Follow real-world conventions.

**Implementation checklist**:
- [ ] Are labels written in the user's vocabulary, not technical jargon?
- [ ] Are icons and symbols based on real-world metaphors the user understands?
- [ ] Do menu items and buttons use natural language?
- [ ] Are information displays organized in a natural and logical order?

**Examples**: A shopping cart icon (not "inventory container"). A "trash" icon for deletion. "Forgot password?" (not "Credential recovery"). Calendar shows days, weeks, months (not timestamps).

### 3.3 User Control and Freedom

Users often choose system functions by mistake and will need a clearly marked "emergency exit" to leave the unwanted state without having to go through an extended dialogue.

**Implementation checklist**:
- [ ] Is there an "undo" for every irreversible action?
- [ ] Can users cancel any operation in progress?
- [ ] Are there clearly marked exits on dialogs and overlays?
- [ ] Can users go back in multi-step flows?
- [ ] Is there a "home" button or equivalent escape hatch?

**Examples**: Gmail's "Undo Send" toast. An "X" button on every modal. A "Back to results" link on product detail pages. A "Cancel subscription" flow that's as easy as subscribing.

### 3.4 Consistency and Standards

Users should not have to wonder whether different words, situations, or actions mean the same thing. Follow platform conventions.

**Implementation checklist**:
- [ ] Does the same action always produce the same result?
- [ ] Are the same words used for the same concepts throughout?
- [ ] Do visual treatments (color, size, iconography) carry consistent meaning?
- [ ] Are platform conventions followed (e.g., iOS settings gear icon → top-right)?
- [ ] Is there only one visual language (or clearly separated modes)?

**Example**: If "Save" is a blue button on one screen, it should be a blue button on every screen. If swiping dismisses an item in one list, the same gesture should work the same way in all lists.

### 3.5 Error Prevention

Even better than good error messages is a careful design that prevents a problem from occurring in the first place.

**Implementation checklist**:
- [ ] Are destructive actions confirmed before execution?
- [ ] Are unavailable options disabled (not hidden)?
- [ ] Are form inputs constrained appropriately (date pickers, dropdowns, character limits)?
- [ ] Does the design check for an prevent common input errors (e.g., email format)?
- [ ] Are checkpoints and saves provided in long workflows?

**Example**: A "Delete account" button that brings up a confirmation dialog requiring the user to type "DELETE" before proceeding. A date picker instead of a free-text date field.

### 3.6 Recognition Rather Than Recall

Minimize the user's memory load by making objects, actions, and options visible. The user should not have to remember information from one part of the dialogue to another.

**Implementation checklist**:
- [ ] Are all required options visible at the point of decision?
- [ ] Are recent items or frequently used items surfaced for easy access?
- [ ] Does the interface show context rather than requiring users to remember it?
- [ ] Are autocomplete, autosuggest, and history available for search inputs?
- [ ] Are icon labels visible (not just icon-only buttons)?

**Example**: Dropdown menus present choices visually rather than requiring users to remember an exact command name. "Recent files" on the File menu. Showing "You entered: john@example.com" on the confirmation screen.

### 3.7 Flexibility and Efficiency of Use

Accelerators — unseen by the novice user — may often speed up the interaction for the expert user such that the system can cater to both inexperienced and experienced users.

**Implementation checklist**:
- [ ] Are keyboard shortcuts available for power users?
- [ ] Are there customization options for frequently used features?
- [ ] Can users create macros, favorites, presets, or templates?
- [ ] Do expert users have paths to bypass novice-optimized workflows?
- [ ] Can commonly performed tasks be batched or automated?

**Examples**: Gmail keyboard shortcuts (e — archive, r — reply). VS Code command palette. Browser bookmarks. Photoshop custom workspaces. MacOS Spotlight search.

### 3.8 Aesthetic and Minimalist Design

Dialogues should not contain information that is irrelevant or rarely needed. Every extra unit of information in a dialogue competes with the relevant units of information and diminishes their relative visibility.

**Implementation checklist**:
- [ ] Does every visual element serve a purpose?
- [ ] Can any text be removed without losing meaning?
- [ ] Are non-essential decorative elements eliminated?
- [ ] Is the primary action obvious on every screen?
- [ ] Has 50% of the words been cut? (Then cut half of what's left.)

**Example**: Google's homepage — a search box, two buttons, and a logo. Nothing else. Every pixel earns its place. Compare to the cluttered search portals of the late 90s.

### 3.9 Help Users Recognize, Diagnose, and Recover from Errors

Error messages should be expressed in plain language (no codes), precisely indicate the problem, and constructively suggest a solution.

**Implementation checklist**:
- [ ] Are error messages in plain language (not "Error 403" but "You don't have access to this page")?
- [ ] Do error messages explain what went wrong AND how to fix it?
- [ ] Are form validation errors shown inline, next to the relevant field?
- [ ] Do error states preserve what the user already entered?
- [ ] Are recovery steps clear and actionable?

**Examples**: "Password must be at least 8 characters with one number" (not "Invalid password"). Form fields that show the error in red text below the specific field. A broken link that says "This page was moved or deleted. Try searching for what you're looking for."

### 3.10 Help and Documentation

Even though it is better if the system can be used without documentation, it may be necessary to provide help and documentation. Any such information should be easy to search, focused on the user's task, list concrete steps, and not be too large.

**Implementation checklist**:
- [ ] Is the interface self-explanatory enough that most users never need help?
- [ ] Is help searchable and scannable?
- [ ] Does documentation focus on user tasks and goals?
- [ ] Are tooltips, context-sensitive help, and in-app guidance available?
- [ ] Are help resources available at the point of need?

**Example**: A tooltip on a "Save draft" button: "Your changes are saved automatically." A "What's this?" link next to an unfamiliar term. A support article that reads as a step-by-step guide, not a feature spec.

---

## 4. The Masters' Design Principles

### 4.1 Dieter Rams — 10 Principles of Good Design

1. **Good design is innovative** — The possibilities for innovation are not exhausted. Technological development is always offering new opportunities for innovative design.
2. **Good design makes a product useful** — A product is bought to be used. It must satisfy certain criteria, not only functional but also psychological and aesthetic.
3. **Good design is aesthetic** — The aesthetic quality of a product is integral to its usefulness. Products we use every day affect our personal well-being.
4. **Good design makes a product understandable** — It clarifies the product's structure. Better still, it can make the product talk.
5. **Good design is unobtrusive** — Products fulfilling a purpose are like tools. They are neither decorative objects nor works of art. Their design should be both neutral and restrained.
6. **Good design is honest** — It does not make a product more innovative, powerful, or valuable than it really is.
7. **Good design is long-lasting** — It avoids being fashionable and therefore never appears antiquated. Unlike fashionable design, it lasts many years.
8. **Good design is thorough down to the last detail** — Nothing must be arbitrary or left to chance. Care and accuracy in the design process show respect towards the user.
9. **Good design is environmentally friendly** — Design makes an important contribution to the preservation of the environment. It conserves resources and minimizes physical and visual pollution.
10. **Good design is as little design as possible** — Less, but better — because it concentrates on the essential aspects.

**UI application**: Ruthlessly edit interfaces. Every component, color, and interaction should be there for a reason. Strive for simplicity and clarity. Don't add features just to differentiate — differentiate by being better.

### 4.2 Don Norman — The Design of Everyday Things

**Six fundamental principles:**

1. **Affordances** — The relationship between an object and a person. A button affords pushing. A handle affords pulling. A slider affords sliding. In UI: a button that looks pressable affords clicking.
2. **Signifiers** — Signals that indicate where the action should take place. Affordances are what's possible; signifiers communicate where. A "Click here" button with a 3D bevel is a signifier.
3. **Mapping** — The relationship between controls and their effects. Good mapping: press the left arrow → car turns left. Bad mapping: press the up arrow → car turns left.
4. **Feedback** — Communicating the result of an action. Must be immediate, informative, and appropriate.
5. **Constraints** — Limiting the range of possible actions to guide users toward correct use. Physical constraints (USB only fits one way), logical constraints (grayed-out button), cultural constraints (red = stop).
6. **Conceptual models** — The mental model users build of how a system works. Good design helps users develop accurate conceptual models.

**UI application**: Make interactive elements look interactive (affordance + signifier). Ensure clear mapping between controls and their effects. Provide immediate feedback. Use constraints to prevent errors.

### 4.3 Steve Krug — Don't Make Me Think

**Key principles:**

1. **Don't make me think** — A page should be self-evident. Users shouldn't have to work to figure out what's what. If they have to think about it (even for a second), it adds friction.
2. **Users don't read, they scan** — They glance at content, looking for words/phrases that match their task. Make scanning easy: clear headings, short paragraphs, highlighted keywords.
3. **Create clear visual hierarchies** — The more important something is, the more prominent it should be. Logically related things should be visually related.
4. **Get rid of half the words, then get rid of half of what's left** — Happy talk (self-congratulatory introductions) must die. Instructions must die when they can be replaced by better design.
5. **The law of navigation** — Users should never be more than one click away from what they want (but clicks don't really count — *thinking* counts).
6. **Omit needless words** — Every word on the screen competes for the user's attention.

**UI application**: Write scan-friendly copy. Reduce text by 75%. Make the primary action obvious. Test with users — if they hesitate, the design needs work.

### 4.4 John Maeda — Laws of Simplicity

1. **Reduce** — The simplest way to achieve simplicity is through thoughtful reduction.
2. **Organize** — Organization makes a system of many appear fewer.
3. **Time** — Savings in time feel like simplicity.
4. **Learn** — Knowledge makes everything simpler.
5. **Differences** — Simplicity and complexity need each other.
6. **Context** — What lies in the periphery of simplicity is definitely not peripheral.
7. **Emotion** — More emotions are better than fewer.
8. **Trust** — In simplicity we trust.
9. **Failure** — Some things can never be simple.
10. **The one** — Simplicity is about subtracting the obvious, and adding the meaningful.

**UI application**: "Subtract the obvious, add the meaningful" is one of the most powerful design quotes. Before adding a new feature, ask: what can we remove? Before adding a new element, ask: does this *add meaningful value* or just clutter?

### 4.5 Ben Shneiderman — Eight Golden Rules of Interface Design

1. **Strive for consistency** — Sequences of actions, terminology, color, layout, and fonts should be consistent throughout.
2. **Enable frequent users to use shortcuts** — Accelerators, abbreviations, function keys, macros.
3. **Offer informative feedback** — Every user action should have feedback. For frequent actions, feedback can be modest; for infrequent actions, it should be substantial.
4. **Design dialogs to yield closure** — Sequences of actions should have a beginning, middle, and end. Informative feedback at completion.
5. **Offer error prevention and simple error handling** — Prevent errors when possible; when they occur, offer simple constructive instructions.
6. **Permit easy reversal of actions** — Undo makes users feel confident to explore.
7. **Support internal locus of control** — Users should feel they are in charge of the system, not the other way around.
8. **Reduce short-term memory load** — Displays should be simple, page density should be low.

---

## 5. Design Ethics Principles

### 5.1 The Trustworthy Design Framework (Cennydd Bowles)

- **Consent**: Is user agreement genuine, informed, and revocable?
- **Clarity**: Is the system's purpose, behavior, and data use understandable?
- **Control**: Can users customize, limit, or opt out of system behaviors?
- **Recovery**: Can users reverse actions, recover from errors, and delete data?
- **Benefit**: Is the value exchange clear and balanced?

### 5.2 Ethical Design Checklist

- [ ] Would a reasonable user describe this flow as honest?
- [ ] Are choices presented without manipulation (no dark patterns)?
- [ ] Is opt-out as easy as opt-in?
- [ ] Is data collection minimal, transparent, and necessary?
- [ ] Are there clear paths to delete accounts and data?
- [ ] Does the design work for people with disabilities?
- [ ] Does the design account for diverse cultural contexts?
- [ ] Are automated/AI decisions explainable?

---

## When to Read This File

Read `design-principles.md` when:
- Evaluating or critiquing an existing design
- Explaining *why* a design decision works or doesn't work
- Choosing between design alternatives
- Needing to ground recommendations in established psychological principles
- Designing forms, navigation, layouts, or interactive controls
- Writing or reviewing accessibility and ethical considerations

**Document reference**: Principals, laws, and heuristics for UI/UX design evaluation
**Last updated**: July 2026
