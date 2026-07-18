# Interaction Design — Deep Reference

This is the deep reference for interaction design: micro-interactions, transitions, animations, gestures, feedback systems, error handling, and state machines. Read this when designing user flows, interactions, animations, or when reviewing how an interface behaves.

---

## 1. The Anatomy of an Interaction

Every interaction follows a cycle (from Don Norman): **Goal → Plan → Specify → Perform → Perceive → Interpret → Compare → Goal**.

Simplified for UI design:
1. **Trigger** — What initiates the interaction (user action or system state)
2. **Action** — What the user does (click, tap, swipe, type)
3. **Feedback** — What the system shows in response
4. **Outcome** — What changed as a result
5. **Loops & modes** — What happens after (new state, repeat behavior, error recovery)

---

## 2. Micro-interactions (Dan Saffer's Framework)

Micro-interactions serve one purpose: accomplish one task or provide one piece of feedback.

### The 4-Part Structure

**1. Trigger** — How the micro-interaction starts
- *User-initiated*: Click, tap, swipe, keyboard shortcut
- *System-initiated*: Notification, alert, completion callback, error state

**2. Rules** — What happens during the interaction
- The logic that constrains the interaction
- What can and can't happen
- Determine boundaries, conditions, and data flow

**3. Feedback** — What the user sees, hears, or feels
- Visual: Color change, movement, size shift
- Audio: Click sound, confirmation chime, error buzz
- Haptic: Vibration, tactile response (mobile)
- Timing: When feedback appears, how long it lasts

**4. Loops & Modes** — What happens after the interaction
- *Loops*: Repeated behavior (pulsing notification dot, blinking cursor)
- *Modes*: What changes in the system state (e.g., after swiping to delete, "Undo" appears for 5 seconds then disappears)

### Common Micro-interaction Patterns

| Pattern | Trigger | Rule | Feedback | Loop/After |
|---|---|---|---|---|
| **Button press** | Tap/click | Press ≥ active state time | Visual state change (press → release) | Execute action, show result |
| **Toggle switch** | Tap/slide | Binary state: on ↔ off | Animated thumb movement, color change | State saved, visual confirms |
| **Pull to refresh** | Pull content below top | Threshold distance before release triggers | Visual indicator visible during pull | Spinner → new content |
| **Skeleton loading** | Content load begins | Phased reveal matching layout | Placeholder → content fade-in | Complete state |
| **Inline validation** | Focus leaves field (blur) | Check rules (format, required, length) | Error/success icon + message | Scroll to first error |
| **Swipe to delete** | Swipe horizontally on item | ≥ 50% of item width to commit | Item slides, "Delete" button reveals | Item slides away, undo option |
| **Like/favorite** | Tap icon | Toggle state (filled/unfilled) | Animation (scale, color, particle burst) | Count +/- 1 |
| **Drag and drop** | Long press + drag | Drop zone detection | Item lifts, ghost follows cursor | Reorder list or move item |

---

## 3. Motion & Animation

### 3.1 Animation Principles (from Disney, adapted for UI)

| Principle | UI application |
|---|---|
| **Easing** | Objects don't move at constant speed. Use ease-in-out for natural motion. Never use linear easing in UI. |
| **Anticipation** | A small backward movement before forward motion (e.g., pull-to-refresh, a button slightly compresses before expanding) |
| **Follow-through** | Parts continue moving after the main action stops (e.g., menu item bounces slightly after opening) |
| **Staging** | One action at a time — don't animate everything simultaneously |
| **Secondary action** | Support the main animation with smaller related ones (e.g., card expands + content fades in) |
| **Timing** | Duration communicates weight and importance (200ms = lightweight, 500ms = significant) |
| **Exaggeration** | Amplify animations in fun contexts, minimize in functional ones |

### 3.2 Duration & Timing

| Type | Duration | Notes |
|---|---|---|
| **Micro-interaction** (button press, toggle) | 100-200ms | Instant, feels responsive |
| **UI element reveal** (tooltip, dropdown) | 150-250ms | Fast enough to feel connected |
| **Card/modal enter/exit** | 200-300ms | Clear transition without delay |
| **Page transitions** | 300-500ms | Long enough to perceive path, short enough to not feel slow |
| **Loading animation** (looping) | 800-1200ms per loop | Calm and consistent, not frantic |
| **Complex motion sequences** | 500-800ms | For multi-step guided transitions |

**Key principle**: All UI animations should finish within 500ms unless they're conveying system status (loading, progress). Under 100ms is imperceptible as animation.

### 3.3 Easing Curves

| Curve | Equation feel | When to use |
|---|---|---|
| **Linear** | No easing, constant speed | **Never use in UI.** Looks robotic. |
| **Ease out** | Fast start, gradual stop | Elements entering the screen (material enters from user action) |
| **Ease in** | Slow start, fast stop | Elements leaving the screen (material exits) |
| **Ease in-out** | Gradual both ends | Elements moving between screens or within same space |
| **Spring** | Overshoots slightly, settles | Playful contexts, cards snapping, list reordering |

**Platform standard curves**:

Material Design (Android/Web):
- **Standard easing**: `cubic-bezier(0.4, 0.0, 0.2, 1)` — For elements within the screen
- **Deceleration curve**: `cubic-bezier(0.0, 0.0, 0.2, 1)` — Elements entering (ease out)
- **Acceleration curve**: `cubic-bezier(0.4, 0.0, 1.0, 1)` — Elements leaving (ease in)
- **Sharp curve**: `cubic-bezier(0.4, 0.0, 0.6, 1)` — Elements leaving that may return

Apple HIG (iOS/macOS):
- **Ease-in-out**: For most iOS transitions
- **Material spring**: `usingSpringWithDamping: 0.6, initialSpringVelocity: 1.0` for most UIKit animations

### 3.4 What to Animate (and What NOT To)

**DO animate**:
- Spatial transitions (cards expanding, pages moving) — communicates relationships
- State changes (toggle, active/inactive) — communicates what changed
- Focus (shift between elements) — guides attention
- Loading/progress — reduces perceived wait time
- Direct manipulation feedback (drag, resize) — makes interaction feel physical

**DON'T animate**:
- For decoration only — every animation should communicate something
- Large-scale page transitions that take >500ms
- Multiple competing movements simultaneously (causes motion sickness)
- Essential information that users need to read immediately
- For users with motion sensitivity (provide reduced-motion preference)

### 3.5 Reduced Motion (WCAG 2.1 SC 2.3.3)

Users with vestibular disorders can experience nausea and dizziness from motion in UI. Always:
- Respect `prefers-reduced-motion` media query
- Replace animations with opacity fades when motion is reduced
- Ensure no information is conveyed solely through animation
- Provide a setting to disable non-essential motion

**Implementation pattern**:
```css
@media (prefers-reduced-motion: reduce) {
  .animated-element {
    animation: none;
    transition: opacity 0.1s ease;
  }
}
```

---

## 4. Feedback Systems

### 4.1 Response Time Guidelines

| Time | User perception | Required feedback |
|---|---|---|
| **< 0.1s** | Instantaneous | No special feedback needed; result is immediate |
| **0.1-1s** | Caused by the action | Small delay is noticeable but feels part of the action. Show result or minimal loading indicator. |
| **1-10s** | Noticeable wait | Show progress indicator (spinner, skeleton, progress bar). Allow cancellation if possible. |
| **> 10s** | Interruption | Show progress bar with estimated time. Allow backgrounding and notification. Offer to email result. |

### 4.2 Types of Feedback

| Type | Use case | Duration | Example |
|---|---|---|---|
| **Visual confirmation** | Immediate action result | 0.2-0.5s | Button depresses then shows checkmark |
| **Toast/Snackbar** | Non-critical system message | 3-6s auto-dismiss | "Message sent" with optional undo |
| **Inline error** | Form validation, contextual | Persistent until resolved | Red border + error text below input |
| **Modal/dialog** | Critical, blocking information | User-dismissed only | "Are you sure you want to delete?" |
| **Notification** | Out-of-context system event | Depends on type | Push notification, badge, email |
| **Progress indicator** | Long operation | Until complete | Spinner, skeleton, progress bar |
| **Haptic (mobile)** | Touch confirmation | 0.1-0.5s | Light tap on button press |
| **Sound** | Confirmation or alert | 0.2-2s | Message sent confirmation chime |

### 4.3 Error Prevention vs Error Recovery

**Prevention strategies** (better than fixing):
- Disable unavailable buttons rather than showing an error
- Use input constraints (dropdown over text field, date picker over free text)
- Confirm destructive actions with explicit text entry
- Auto-save regularly to prevent data loss
- Gray out invalid options

**Recovery strategies** (when prevention fails):
- Undo: Most powerful recovery tool (Gmail's "Undo Send")
- Back/escape: Navigate away from error state
- "What happened and how to fix it" error messages
- Auto-recovery: Inline suggestions ("Did you mean X?")
- Save drafts/state for recovery after crash or timeout

---

## 5. Gesture Design

### 5.1 Gesture Types

| Gesture | Platform | Function | Pitfalls |
|---|---|---|---|
| **Tap** | All | Select, activate, submit | Most reliable gesture — always support |
| **Double-tap** | All | Zoom, like, quick action | Harder to discover; adds delay to single tap |
| **Long press** | Mobile | Reveal context menu, reorder | Not discoverable; conflicts with scroll |
| **Swipe** | Mobile | Delete, go back, dismiss | Direction matters (left vs right); conflicts with scroll |
| **Pinch/spread** | Mobile | Zoom in/out | Often interferes with scroll |
| **Drag** | All | Move, reorder, select range | Needs clear affordance |
| **Rotate** | Mobile | Rotate content, dial | Rarely used; low discoverability |
| **Edge swipe** | Mobile | Navigation (back), panel reveal | Conflicts with system gestures (iOS back swipe) |

### 5.2 Gesture Design Principles

1. **Tap should always be the fallback**: If a gesture is hidden, provide a visible tap-based alternative.
2. **Gestures shouldn't conflict with system gestures**: iOS back swipe, Android pull-down notification.
3. **Discovered gestures need onboarding**: Short tooltip or animation when the user first encounters the element.
4. **Thumb zone placement** (mobile): Primary actions in the middle-to-bottom third of screen; hard-to-reach actions at the top.
5. **Feedback for every gesture**: Show what's happening during the gesture (e.g., item lifts during drag, delete zone highlights during swipe).
6. **Accessibility**: Every gesture must have a non-gesture alternative (VoiceOver, keyboard, switch control).

### 5.3 Touch Target Guidelines

| Standard | Minimum size | Spacing |
|---|---|---|
| **Apple HIG** | 44×44pt | 8px minimum between targets |
| **Material Design** | 48×48dp | 8dp minimum between targets |
| **WCAG 2.2** | 24×24px (AA) | 24px minimum between targets |
| **Desktop cursor** | 20×20px minimum | 4px minimum between targets |

---

## 6. State Machines & UI States

Every interactive element has states. A complete design accounts for all of them.

### 6.1 The Standard State Model

**For components**:
```
Default → Hover → Active/Focus → Disabled → Loading → Success/Error
```

**For views/screens**:
```
Initial → Loading → Empty → Partial → Error → Success → Refreshing
```

### 6.2 State Checklist

For every component and screen, ensure these states are designed:

| State | What it means | What to design |
|---|---|---|
| **Default** | Ready, idle, waiting | Normal appearance |
| **Hover** (desktop) | Cursor is over the element | Visual feedback (color, elevation, underline) |
| **Active/Pressed** | User is currently interacting | Button depression, color shift |
| **Focus** | Element is keyboard focused | Focus ring, outline, highlight |
| **Disabled** | Element can't be interacted with | Reduced opacity, grayed out, no pointer cursor |
| **Loading** | Content/action is in progress | Spinner, skeleton, progress indicator |
| **Empty** | No data to show | Explanation + action to populate |
| **Error** | Something went wrong | Error message + recovery path |
| **Success** | Action completed successfully | Confirmation + what happens next |
| **Partial** | Some content loaded, some pending | Progressive loading, shimmer |
| **Offline** | No network connection | Notice + offline capabilities |
| **Edge case** | Unusual data state (overflow, missing) | Truncation, overflow indicators, fallback UI |

---

## 7. Interaction Cost Reduction

**Interaction cost** is the sum of physical effort + mental effort + waiting time to complete a task.

### 7.1 Reduce Physical Effort
- Minimize number of steps/clicks
- Use smart defaults and prefilled values
- Auto-advance to next field after input
- Batch operations (select all, delete multiple)
- Keyboard shortcuts and quick commands

### 7.2 Reduce Mental Effort
- Clear labels and signifiers
- Familiar patterns (follow conventions)
- Progressive disclosure (show complexity gradually)
- Recognition over recall (show, don't make them remember)
- Group related items (Gestalt proximity)

### 7.3 Reduce Waiting Time
- Optimistic UI (show result before server confirms)
- Skeleton screens (show layout before content)
- Background sync and prefetching
- Offline-first architecture
- Perceived performance (progress indicators, visual feedback)

---

## 8. Forms & Data Entry

Forms are often the most interactive part of an application. They deserve special attention.

### 8.1 Form Design Principles

- **Single-column is faster** than multi-column (users don't have to scan horizontally)
- **Top-aligned labels** are fastest to scan (eye moves straight down)
- **Inline validation** after blur (not during typing, not only on submit)
- **Group related fields** and use section headings for forms with 8+ fields
- **Match input type to content** (date picker for dates, dropdown for 5-20 options, radio for 5 or fewer, search/autocomplete for 20+)
- **Provide clear error messages** — what's wrong and how to fix it
- **Enable autofill** (autocomplete attribute) for saved data

### 8.2 Form Field Types & When to Use

| Field type | Best for | Avoid when |
|---|---|---|
| **Text input** | Short free-form text (name, email) | Structured data (dates, countries) |
| **Textarea** | Long free-form text (bio, comments) | Short fields |
| **Dropdown** | 5-20 options, mutually exclusive | 3 or fewer options (use radio); 20+ options (use autocomplete) |
| **Radio buttons** | 2-5 options, mutually exclusive | Many options (use dropdown) |
| **Checkboxes** | Multiple selection, binary choices | Single choice (use toggle) |
| **Toggle/switch** | Binary setting with immediate effect | Actions that need confirmation |
| **Search/autocomplete** | 20+ options, user knows what they want | Short, fixed lists |
| **Date picker** | Date input | Simple dates like birth year (use dropdown) |
| **Slider** | Precise values within a range | Quick, rough adjustments |
| **Color picker** | Color selection | Precise hex values (use text input) |

### 8.3 Form Validation

| Approach | When to validate | Pros | Cons |
|---|---|---|---|
| **On submit** | Only when form is submitted | Simple to implement | Users must fix multiple errors; frustrating |
| **On blur** | When field loses focus | Gives immediate field-level feedback | May show errors before user finishes typing |
| **On keystroke** | As user types | Feels responsive | Can be aggressive; high cognitive load |
| **Debounced on keystroke** | After user stops typing (300-500ms) | Best balance | More complex to implement |

**Best practice**: Validate on blur for most fields. Show success/error icon + message. Scrolling to the first error on submit is essential.

---

## When to Read This File

Read `interaction-design.md` when:
- Designing user flows or task sequences
- Creating micro-interactions (toggle, swipe, drag)
- Designing animations, transitions, or loading states
- Planning gesture-based interactions
- Setting up form validation and error handling
- Reviewing feedback systems and response times
- Reducing friction or cognitive load in an existing flow

**Document reference**: Interaction patterns, micro-interactions, animation, gestures, feedback systems, state management
**Last updated**: July 2026
