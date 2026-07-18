# Mobile App Design — Deep Reference (Minimal & Calm, Dribbble-Inspired)

This is the deep reference for designing minimal, calm mobile app interfaces inspired by the best Dribbble designers (2024-2026). Read this when designing mobile app screens, flows, navigation patterns, onboarding, or any mobile-native experience. **Unless the user explicitly requests a different visual style, default to minimal, calm, spacious design.**

Reference designers: Tran Mau Tri Tam, Taras Migulko, Outcrowd, Fireart Studio, George Kvasnikov, Rifayet Uday, Anton Aheichanka, Daniyal Mokhammad

---

## 1. The Minimal Mobile App Design Philosophy

Mobile design is uniquely constrained by screen size, thumb reach, attention span, and context of use. Every pixel and interaction must earn its place.

**Core principles**:
1. **Thumb-first design** — Primary actions belong in the easy-to-reach thumb zone (bottom and middle-right of screen). Put navigation and primary CTAs where thumbs naturally rest.
2. **Reduce cognitive load** — Mobile users are often distracted, on-the-go, or task-focused. Every extra step or confusing label causes abandonment. Clarity is speed.
3. **Progressive disclosure** — Show the essential, hide the advanced. Don't overwhelm users with every option up front. Surface secondary features on demand.
4. **Platform authenticity** — Respect iOS and Android conventions. Don't cross-platform patterns that feel foreign on either.
5. **Calm technology** — Notifications, animations, and feedback should be gentle and purposeful. A calm app respects the user's attention and doesn't demand it unnecessarily.

---

## 2. Mobile App Design Process

### Step 1: Map the User Flow

Before any visual design, define the flow:

```
Launch → Splash/Onboarding (first time only)
       → Home/Feed/Dashboard (the core screen)
       → Feature screens (drill-down)
       → Detail/Edit screens
       → Confirmation/Success states
       → Settings/Profile
```

### Step 2: Identify the Core Screen

Every app has one screen users spend the most time on. Design that screen first. For social apps, it's the feed. For productivity, the dashboard. For ecommerce, the product browse. Everything else supports that screen.

### Step 3: Apply Mobile-Specific Visual Language

---

## 3. Dribbble-Inspired Visual Language for Mobile Apps

### 3.1 Default Color Palettes

**Palette 1: Soft & Clean (default for most apps)**
```
Background:  #F8F9FB or #F5F6FA
Cards:       #FFFFFF
Text primary: #1A1D23
Text secondary: #8B93A5
Text muted:   #B0B7C3
Accent:       #5680E9 (calm blue)
Accent soft:  #EEF2FF (accent at 10% — for selection/highlight)
Destructive:  #E88D7A (soft coral, not aggressive red)
Success:      #7BC5A1 (sage green)
Warning:      #F3C86A (warm amber)
Dividers:     #E8ECF0 (1px)
Shadow:       rgba(0,0,0,0.04)
```

**Palette 2: Dark Mode (on explicit request only)**
```
Background:  #0F1117
Cards:       #1A1D28
Text primary: #EDEEF0
Text secondary: #9A9FB0
Accent:       #6B8DF7 (brighter for dark)
Dividers:     #2A2D3A
```

### 3.2 Typography for Mobile

**Type scale**:
```
Large title:  28-34px / 1.2 / 700
Title 1:      22-24px / 1.3 / 600-700
Title 2:      18-20px / 1.3 / 600
Headline:     16-17px / 1.4 / 600
Body:         15-16px / 1.5 / 400
Subhead:      14px / 1.4 / 500
Footnote:     13px / 1.4 / 400
Caption:      11-12px / 1.3 / 400
Button:       15-16px / 1 / 500-600
Tab bar:      10-11px / 1 / 500 (labels)
```

**System fonts (recommended for performance)**:
- iOS: SF Pro (system), SF Rounded (for playful)
- Android: Roboto (system), Noto Sans
- Cross-platform: Inter, Plus Jakarta Sans

For minimal apps, use system fonts — they're optimized for the platform, load instantly, and respect user accessibility settings (Dynamic Type, font size).

### 3.3 Spacing & Touch Targets

**Mobile spacing scale**:
```
Screen margin: 16-20px
Card padding: 16-20px
Between cards/items: 12-16px
Between related elements: 8-12px
Between sections: 24-32px
Bottom safe area: 20-34px (varies by device)
Top safe area: 44-60px (varies by device)
```

**Touch target sizes**:
```
Minimum (WCAG 2.2 AA): 24×24px
Recommended (Apple HIG): 44×44pt
Recommended (Material): 48×48dp
On desktop (web app): 20×20px minimum

Between touch targets: 8px minimum
For bottom tab bar items: 48×48px + label below
For table row taps: full row height (44-56px)
```

### 3.4 Mobile Navigation Patterns

**Bottom Tab Bar (3-5 items)**:
```
┌──────────────────────────────────────────────┐
│                                              │
│           (Content area)                      │
│                                              │
│                                              │
├──────┬──────┬──────┬──────┬──────┤           │
│  🏠  │ 🔍  │ ➕  │ 🔔  │ 👤  │           │ ← 48-56px height
│ Home │ Search│ New  │ Notif│ Profile│        │ ← 10-11px label
└──────┴──────┴──────┴──────┴──────┘           │
```
- 3-5 items maximum. No nesting below tabs.
- Active state: accent-colored icon + semibold label
- Inactive: muted gray icons + regular label
- Badge: unread count (red dot or number on notification tab)

**Top Navigation Bar (Navigation Bar / Top App Bar)**:
```
┌──────────────────────────────────────────────┐
│ ← Back      Screen Title          [Action]   │ ← 44-56px (device-dependent)
└──────────────────────────────────────────────┘
```
- Left: back arrow (or close "X" for modals)
- Center: screen title (16-17px, semibold)
- Right: 1-2 action icons (no text labels)
- iOS: large title option (34px, bold) collapses to standard title on scroll

**Gesture navigation**:
| Gesture | Function | Platform convention |
|---|---|---|
| **Swipe back** | Navigate to previous screen | iOS (edge swipe) + Android (back gesture) |
| **Swipe to delete** | Remove item from list | iOS (full/partial swipe) + Android |
| **Pull to refresh** | Reload content | Both platforms |
| **Long press** | Context menu, reorder | iOS Haptic Touch, Android |
| **Tap status bar** | Scroll to top | iOS convention |

---

## 4. Mobile App Screen Patterns

### 4.1 Onboarding (First-time experience)

**Minimal onboarding principles**:
- **Show value, not features**: Don't explain what the app does — show the benefit
- **3-4 screens maximum**: Beyond 4, users drop off
- **Skip button always visible**: Let users dismiss and explore on their own
- **Progress dots**: Show "Screen 2 of 4" at the bottom
- **One message per screen**: Headline + one sentence + illustration

**Standard onboarding flow**:
```
┌──────────────────────────────┐      ┌──────────────────────────────┐
│                              │      │                              │
│      [Illustration]          │      │      [Illustration]          │
│                              │      │                              │
│   Headline: The benefit      │  →   │   Headline: The solution     │
│   Sub: One line explaining   │      │   Sub: How it works simply   │
│                              │      │                              │
│                  [Skip]      │      │                  [Skip]      │
│   ○ ● ○ ○    [Continue →]   │      │   ○ ○ ● ○    [Continue →]   │
└──────────────────────────────┘      └──────────────────────────────┘

┌──────────────────────────────┐      ┌──────────────────────────────┐
│                              │      │                              │
│      [Illustration]          │      │   Final screen:              │
│                              │      │   "Ready to get started?"    │
│   Headline: Social proof     │  →   │                              │
│   Sub: "Join 10k+ users"     │      │   ┌──────────────────────┐   │
│                              │      │   │ Create Account       │   │
│                  [Skip]      │      │   └──────────────────────┘   │
│   ○ ○ ○ ●    [Continue →]   │      │   ┌──────────────────────┐   │
└──────────────────────────────┘      │   │ Sign In              │   │
                                       └──────────────────────┘   │
                                          [Maybe later] optional    │
                                       └──────────────────────────────┘
```

### 4.2 Home / Feed Screen

**Standard minimal feed layout**:
```
┌──────────────────────────────┐
│ 9:41                         │ ← status bar
├──────────────────────────────┤
│ Logo          🔔 👤          │ ← navigation bar
├──────────────────────────────┤
│                              │
│ ┌────────────────────────┐  │
│ │ Search "Find..."       │  │ ← search bar, 40-44px, 12px radius
│ └────────────────────────┘  │
│                              │
│ ┌────┬────┬────┬────┐      │ ← category/tab scroll (horizontal)
│ │All │Cat1│Cat2│Cat3│ ...  │
│ └────┴────┴────┴────┘      │
│                              │
│ ┌────────────────────────┐  │
│ │ Card title/subtitle    │  │ ← content cards
│ │ Description text...    │  │
│ │ [Image or icon]        │  │
│ └────────────────────────┘  │
│                              │
│ ┌────────────────────────┐  │
│ │ Card title/subtitle    │  │
│ │ Description text...    │  │
│ └────────────────────────┘  │
│                              │
├──────────────────────────────┤
│ 🏠  🔍  ➕  🔔  👤        │ ← bottom tab bar
└──────────────────────────────┘
```

### 4.3 Detail Screen

**Standard detail screen layout**:
```
┌──────────────────────────────┐
│ ← Back        Title     ⋮   │ ← nav bar with action menu
├──────────────────────────────┤
│                              │
│ ┌────────────────────────┐  │
│ │   Hero Image / Media   │  │ ← 16:9 or 4:3 aspect ratio
│ └────────────────────────┘  │
│                              │
│  Title / Name                 │ ← 22-24px, bold
│  Subtitle / Meta             │ ← 14px, secondary
│                              │
│  ★ ★ ★ ★ ☆  24 reviews       │ ← rating row
│                              │
│  ─────  Description  ─────   │ ← section header
│  Body text that describes    │ ← 15-16px, 1.5 line-height
│  the item in detail...       │
│                              │
│  ─────  Details  ─────       │
│  Info row 1           Value  │
│  Info row 2           Value  │
│                              │
│  ─────  Related  ─────       │
│  ┌──┐ ┌──┐ ┌──┐            │ ← horizontal scroll of related items
│  └──┘ └──┘ └──┘            │
│                              │
├──────────────────────────────┤
│   [$49.99]  [Add to Cart  →] │ ← sticky bottom action bar
└──────────────────────────────┘
```

### 4.4 Settings / Profile Screen

**Standard settings layout**:
```
┌────────────────────────────────┐
│ ← Back       Settings          │
├────────────────────────────────┤
│  ┌──────────────────────────┐  │
│  │  [Avatar]  Name          │  │ ← profile preview card
│  │            View profile >│  │
│  └──────────────────────────┘  │
│                                │
│  Account                       │ ← section header (13px, uppercase, secondary)
│  ┌──────────────────────────┐  │
│  │ 👤 Edit Profile        > │  │ ← setting rows: 44-48px height
│  │ 🔔 Notifications       > │  │    icon (20-22px) + label (15-16px)
│  │ 🔒 Privacy             > │  │    14px secondary description (optional)
│  └──────────────────────────┘  │
│                                │
│  Preferences                   │
│  ┌──────────────────────────┐  │
│  │ 🌙 Dark Mode      [⚪] │  │ ← toggle row
│  │ 🌐 Language         EN > │  │ ← selection row
│  │ 📱 Appearance           > │  │
│  └──────────────────────────┘  │
│                                │
│  Support                       │
│  ┌──────────────────────────┐  │
│  │ ❓ Help Center          > │  │
│  │ 💬 Contact Us           > │  │
│  │ ⭐ Rate the App         > │  │
│  └──────────────────────────┘  │
│                                │
│  Version 2.4.1                 │ ← 12px, muted, centered
└────────────────────────────────┘
```

**Settings screen design rules**:
- Icons: 20-22px outline, consistent stroke, muted color
- Labels: 15-16px, primary text
- Description: 12-13px, secondary, shown below label when needed
- Chevron: ">" at the right, 12px, secondary, indicates drill-down
- Toggles: right-aligned, green accent (iOS) or blue (Android)
- Dividers between groups only (not between every row)
- Destructive actions (Logout, Delete): at the bottom in red text

### 4.5 List Screen

**Standard list row anatomy**:
```
┌──────────────────────────────────┐
│ ┌────┐                          │
│ │ 📸 │  Primary text            │ ← 48-56px row height
│ │ 48 │  Secondary text          │    icon/avatar 40-48px
│ └────┘                          │    primary: 15-16px, primary text
│                                 │    secondary: 12-13px, secondary
│                          ▶ │    │ ← optional chevron or action
├──────────────────────────────────┤ ← divider (full width, 1px, 30% opacity)
│ ┌────┐                          │
│ │ 📸 │  Primary text            │
│ └────┘                     ▶ │  │
└──────────────────────────────────┘
```

### 4.6 Modal / Bottom Sheet

**Standard bottom sheet**:
```
┌──────────────────────────────────┐
│ ──── (drag handle) ────          │ ← 4px wide, 30px, centered
│                                  │
│  Title                           │ ← 17-18px, semibold
│                                  │
│  ┌──────────────────────────┐   │
│  │ Option 1                 │   │ ← 48-52px rows
│  ├──────────────────────────┤   │    icon (20px) + label (16px)
│  │ Option 2                 │   │
│  ├──────────────────────────┤   │
│  │ ❌ Destructive option    │   │ ← red text for destructive
│  └──────────────────────────┘   │
│                                  │
│  [Cancel]                        │ ← text button, centered
└──────────────────────────────────┘
```
- Peek height: ~50% of screen
- Drag down to dismiss
- Tap backdrop to dismiss
- Never stack multiple sheets

---

## 5. Mobile-Specific Component Patterns

### Bottom Action Bar (Sticky CTA)

Used on detail screens, checkout, or any screen with a primary action.

```
┌──────────────────────────────────┐
│  Content area...                  │
│                                  │
│  (scrollable)                     │
│                                  │
├──────────────────────────────────┤ ← subtle top border
│ $49.99    [Add to Cart →]       │ ← price left, button right
└──────────────────────────────────┘ ← 64-80px height with safe area
```
- Always includes top divider to separate from content
- Height includes bottom safe area (20-34px)
- Button: full-width or sized to content

### Toggle / Switch

```
Off:  ┌──────┐                       On:  ┌──────────┐
      │  ○    │                           │    ●    │  ← 31×51pt (iOS)
      └──────┘                           └──────────┘
      Gray bg, white dot                  Accent bg, white dot
      (iOS: green when on)
```

### Search Bar

```
Standard:
┌──────────────────────────────────────┐
│ 🔍  Search                          │ ← 36-40px height, 10-12px radius
└──────────────────────────────────────┘  #E8ECF0 bg or white with border

On focus (expanded):
┌──────────────────────────────────────┐
│ ← Cancel     🔍  Search...    ✕     │ ← cancel button appears left
└──────────────────────────────────────┘  on iOS, or right on Android
```

### Pull to Refresh

- Trigger: pull content below its top boundary
- Threshold: ~64px pull distance
- Visual: Circular spinner or custom animation
- Release: content refreshes, spinner stays until complete
- Feedback: subtle haptic on iOS

### Skeleton Loading (Mobile)

- Same dimensions as final content (no layout shift)
- Rounded gray rectangles matching the shape of final content
- Shimmer animation (1.5s ease-in-out)
- For feeds: 3-5 skeleton rows
- For detail: skeleton image + skeleton text lines

---

## 6. Mobile Interaction Patterns

### 6.1 Feedback & Loading

| Action | Feedback | Timing |
|---|---|---|
| **Button tap** | Visual state change (press → release) + optional haptic | < 100ms |
| **Page transition** | Slide (iOS push), fade (Android) | 300-350ms |
| **Pull to refresh** | Spinner animation + content load | Until complete |
| **Swipe to delete** | Item slides, "Delete" button reveals | Gesture-driven |
| **Success** | Toast/snackbar at bottom, auto-dismiss | 3-4 seconds |
| **Error** | Inline toast or modal (if blocking) | Until dismissed |
| **Background activity** | Activity indicator (small) | Until complete |

### 6.2 Error Handling on Mobile

- **Network error**: Inline toast "No internet connection" + auto-retry when connection returns
- **API error**: Gentle alert within the affected screen — never a full-screen error for a section failure
- **Form error**: Inline below the field, red text, "Please enter a valid email"
- **Empty state**: Illustration + "Nothing here yet" + action button
- **Timeout**: "Taking longer than expected" + try again button

### 6.3 Keyboard Avoidance

- Scroll content up when keyboard appears (never cover the active field)
- "Return" key advances to the next field on forms
- "Done" button above keyboard on iOS number pads
- Tap outside keyboard to dismiss

---

## 7. Mobile Design States

### Empty State
```
┌──────────────────────────────┐
│                              │
│                              │
│       [Gentle illustration]  │ ← 120-160px, 2-3 colors
│                              │
│   No items yet               │ ← 16-18px, semibold
│   Get started by adding      │ ← 14px, secondary, 1 line
│   your first item.          │
│                              │
│   ┌──────────────────────┐  │
│   │  Add your first item  │  │ ← CTA button
│   └──────────────────────┘  │
│                              │
│                              │
└──────────────────────────────┘
```

### Loading State
- Skeleton screens for predictable layouts (list, feed, profile)
- Centered spinner for unpredictable content
- Never show blank screen with just a spinner

### Error State (Section-Level)
```
┌──────────────────────────────┐
│ ⚠️ Couldn't load feed       │ ← 14px, primary
│   Pull down to retry        │ ← 12px, secondary
└──────────────────────────────┘
```
Inline within the failed section. No modal dialogs for section-level errors.

---

## 8. Mobile-Specific Anti-Patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| **Hamburger menu for primary navigation** | Hidden, low discoverability, requires two taps | Use bottom tab bar for 3-5 primary destinations |
| **Tiny touch targets (< 44px)** | Fitts' Law — hard to tap, causes errors | Minimum 44×44pt, 48×48dp recommended |
| **Full-screen modals for simple choices** | Heavy, blocks context, requires loading | Use bottom sheet (lightweight, contextual) |
| **No keyboard dismissal** | Frustrating, keyboard blocks content | Tap outside to dismiss, scroll to dismiss |
| **Hidden gestures for primary actions** | No affordance, users won't discover them | Always provide a visible button alternative |
| **Overlapping navigation patterns** (tab bar + hamburger + bottom sheet) | Confusing mental model, unpredictable | One primary navigation pattern, consistent everywhere |
| **Splash screens that last > 2 seconds** | Users think app crashed or is slow | Brand splash < 1s, skeleton loading for content |
| **Push notifications for every event** | Notification fatigue, user turns off all | Batch non-critical, only push important updates |
| **No haptic feedback on key interactions** | Feels flat, lacks physical confirmation | Light haptic on button press, success feedback |

---

## 9. iOS vs Android Platform Considerations

| Element | iOS | Android |
|---|---|---|
| **Navigation** | Back swipe gesture + nav bar back button | Back gesture + hardware/software back button |
| **Title style** | Large title (34px) collapsing to standard (17px) | Regular title (20px) always visible |
| **Tab bar** | Bottom, 3-5 items, translucent | Bottom, 3-5 items, solid or translucent |
| **Search** | Search bar in nav bar (iOS 15+) or dedicated | Search bar or search icon that expands |
| **Modals** | Slide up from bottom, swipe to dismiss | Dialog or bottom sheet |
| **Action sheets** | Slide up from bottom | Bottom sheet or dialog |
| **Settings** | Toggles: green when on | Toggles: blue/purple accent |
| **Typography** | SF Pro (system) | Roboto (system) |
| **Safe areas** | Notch, Dynamic Island, Home Indicator | Status bar, gesture bar, camera punch-hole |

**Cross-platform rule**: Maintain consistent brand, content, and interaction logic. Adapt navigation, controls, and spacing to each platform's conventions. A well-designed app feels native on both platforms without being identical.

---

## When to Read This File

Read `mobile-app-design.md` when:
- Designing mobile app screens (onboarding, home, detail, settings, lists, sheets)
- Choosing navigation patterns (tab bars, gestures, search)
- Setting mobile typography, spacing, and touch targets
- Creating mobile-specific states (loading, empty, error)
- Adapting designs for iOS vs Android conventions
- **Default direction**: Start with minimal, calm, spacious design (Palette 1: Soft & Clean). Only deviate if the user explicitly requests a different visual style.

**Document reference**: Dribbble-inspired minimal mobile app design patterns, components, navigation, and platform-specific best practices
**Influenced by**: Tran Mau Tri Tam, Taras Migulko, Outcrowd, Fireart Studio, George Kvasnikov, Rifayet Uday, Anton Aheichanka, Apple HIG, Material Design 3
**Last updated**: July 2026
