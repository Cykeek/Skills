# Platform-Specific Design — Deep Reference

This is the deep reference for platform-specific design patterns, guidelines, and best practices across mobile (iOS, Android), desktop, web, and responsive/adaptive contexts. Read this when designing for specific platforms or cross-platform experiences.

---

## 1. iOS (Apple Human Interface Guidelines)

### 1.1 Core Design Philosophy

- **Deference**: The interface stays out of the way. Content is king.
- **Clarity**: Text is legible, icons precise, adornments subtle. Purpose is immediately clear.
- **Depth**: Visual layers and realistic motion convey hierarchy and vitality.

### 1.2 Key iOS Conventions

| Pattern | iOS behavior | Notes |
|---|---|---|
| **Navigation** | Navigation bar (top), Tab bar (bottom) | Tab bar max 5 items. Title in nav bar. |
| **Back navigation** | Left-edge swipe gesture OR back button in nav bar | Never put a back button in the content area |
| **Search** | Search bar in nav bar (iOS 15+) or dedicated search screen | Supports scope bar and search suggestions |
| **Modals** | Slide up from bottom, dismiss by swipe down | Use for focused tasks that don't fit navigation hierarchy |
| **Context menu** | 3D Touch / Haptic Touch (long press) + peek and pop | Preview content without navigating to it |
| **Action sheets** | Slide up from bottom on iPhone; popover on iPad | For destructive actions or multiple choices |
| **Alerts** | Center-screen modal, 1-2 buttons max | Use sparingly — interrupts workflow |
| **Switches** | Label on left, toggle on right | Use for binary settings |
| **Activity View** | System share sheet | Share content, not custom share UI |
| **Swipe actions** | Primary action on left swipe, destructive on full swipe | List/table rows only |

### 1.3 iOS Bar Heights

```
Status bar:           20pt (44pt on iPhone X+)
Navigation bar:       44pt (standard), 96pt (large title, iOS 13+)
Tab bar:              49pt (49pt + safe area on X+)
Toolbar:              44pt (44pt + safe area on X+)
Search bar:           36pt
```

### 1.4 iOS Spacing Guidelines

- **Margin**: 16pt from screen edges
- **Card padding**: 16pt
- **Between elements**: 8pt minimum
- **Touch target**: 44×44pt minimum
- **Corner radius**: 6pt (system), 10pt (cards), 16pt+ (sheets)

### 1.5 iOS Typography

```
Large Title:  34pt bold
Title 1:      28pt bold
Title 2:      22pt bold
Title 3:      20pt semibold
Headline:     17pt semibold
Body:         17pt regular
Callout:      16pt regular
Subhead:      15pt regular
Footnote:     13pt regular
Caption 1:    12pt regular
Caption 2:    11pt regular
```
**System font**: SF Pro (sans-serif), SF Mono (monospace), New York (serif)

### 1.6 iOS Design Considerations

- **Safe areas**: Account for notch, home indicator, status bar, dynamic island. Never put interactive content in unsafe areas.
- **Keyboard avoidance**: Scroll content up when keyboard appears. Don't cover the active text field.
- **Dynamic Type**: Support system font size changes. Test with Accessibility → Larger Text options.
- **Dark mode**: All apps should support both light and dark appearances.
- **VoiceOver**: Every element needs an accessibility label. AssistiveTouch and Switch Control should work.
- **iPad**: Support Split View, Slide Over, and multi-window. Don't lock orientation unless necessary.
- **Reachability**: Primary actions should be in the lower half of the screen (thumb zone).

---

## 2. Android (Material Design 3)

### 2.1 Core Design Philosophy

- **Radical**: Bold, graphic, intentional. Color, edge-to-edge imagery, large typography.
- **Adaptive**: Responsive cross-platform. One design system for all screen sizes.
- **Human**: Movement with meaning. Light, surface, and motion build trust.

### 2.2 Key Android / Material 3 Conventions

| Pattern | Material 3 behavior | Notes |
|---|---|---|
| **Navigation** | Navigation bar (bottom, 3-5 items) + Navigation drawer (side) | Bottom nav for primary destinations; drawer for secondary |
| **Top app bar** | Top of screen, can scroll off | Supports navigation icon, title, actions, overflow menu |
| **FAB** | Floating action button, bottom-right | Primary action on screen. Can be extended with text label |
| **Bottom sheets** | Slide up from bottom. Standard or Modal | Standard = persistent; Modal = dismissible, blocking |
| **Snackbar** | Brief message at bottom, auto-dismiss | "Undo" action optional. Don't block interaction. |
| **Dialog** | Center card with 1-2 actions | For critical confirmations or non-blocking decisions |
| **Chips** | Compact elements for selection, filtering, or entry | Multiple types: input, filter, choice, action |
| **Segmented buttons** | Group of buttons for selecting options | Like tabs but for a single screen's content |

### 2.3 Material 3 Key Specs

```
Status bar:           24dp
Top app bar:          64dp (small), 152dp (medium), 412dp (large)
Bottom nav bar:       80dp
Navigation drawer:    Max 360dp
FAB:                  56dp (regular), 40dp (small), 96dp (extended)
Bottom sheet:         Peek height ~64dp, expanded = full screen
Side sheet:           Max 360dp (standard), 256-400dp (modal)

Touch target:         48×48dp minimum
Spacing:              16dp (screen edge), 24dp (between sections), 8dp (between related items)
Corner radius:        4dp (small), 16dp (medium), 28dp (large), 16dp (top for bottom sheets)
Elevation:            0-5dp (surface, 1dp, 3dp, 6dp, 8dp, 12dp)
```

### 2.4 Material 3 Typography

```
Display L:   57pt regular, -0.25 letter spacing
Display M:   45pt regular
Display S:   36pt regular, -0.10 letter spacing
Headline L:  32pt regular
Headline M:  28pt regular, +0.02 letter spacing
Headline S:  24pt regular
Title L:     22pt semibold
Title M:     16pt semibold, +0.15 letter spacing
Title S:     14pt semibold, +0.1 letter spacing
Body L:      16pt regular, 0.5 letter spacing, 1.5 line height
Body M:      14pt regular, 0.25 letter spacing, 1.5 line height
Body S:      12pt regular, 0.4 letter spacing, 1.5 line height
Label L:     14pt semibold, 0.1 letter spacing
Label M:     12pt semibold, 0.5 letter spacing
Label S:     11pt semibold, 0.5 letter spacing
```
**System font**: Roboto (Android), Noto (cross-platform)

### 2.5 Android Design Considerations

- **System navigation**: Gesture nav (iOS-like) or 3-button nav. Respect both.
- **Back navigation**: Hardware/gesture back button on Android. Never use in-app back button as primary.
- **Edge-to-edge**: Draw behind system bars on Android 15+. Handle insets properly.
- **Dynamic colors**: Material You theming — colors from wallpaper. Make sure text stays readable.
- **RTL support**: Many Android users use RTL languages. Design for both LTR and RTL.
- **Doze / App standby**: Network requests may be delayed. Handle offline gracefully.
- **Permissions**: Request permissions in context (when needed), not at install. Users can deny easily.
- **TalkBack**: Ensure accessibility labels and navigation for screen reader users.

---

## 3. Responsive & Adaptive Design

### 3.1 Responsive vs Adaptive

| Approach | What it means | Best for |
|---|---|---|
| **Responsive** | Same content reflows based on viewport | Content-heavy sites, articles, editorial |
| **Adaptive** | Different layouts for different breakpoints | Apps, dashboards, complex UIs |
| **Combined** | Responsive content + adaptive layout changes | Most products |

### 3.2 Common Breakpoints

```
Mobile:         320-480px (portrait), 480-767px (landscape)
Tablet:         768-1024px (portrait), 1024-1199px (landscape)
Desktop:        1280-1440px (standard), 1600-1920px (wide)
Ultrawide:      1920px+ (fluid with max-width constraint)
```

**Better approach**: Design for content, not devices. Define breakpoints where your content breaks, not at arbitrary device sizes.

### 3.3 Responsive Design Patterns

**Reorder**: Content stacks vertically on small screens, arranges horizontally on larger ones.

**Reveal**: Progressively show more content on larger screens (e.g., show 2-line preview on mobile, full table on desktop).

**Transform**: Change UI pattern entirely (e.g., tabs on mobile → sidebar on desktop; dropdown on mobile → inline on desktop).

**Remove**: Hide secondary content on small screens (non-critical modules, advanced features, less important data).

**Prioritize**: Reorder content to show the most important items first on mobile. What's secondary on desktop becomes hidden/behind a "more" link on mobile.

### 3.4 Navigation Responsive Patterns

| Desktop | Mobile | Pattern |
|---|---|---|
| Top nav (horizontal) | Hamburger menu | Most common |
| Sidebar nav | Bottom nav | App-like |
| Left nav | Hamburger | Complex hierarchy |
| Mega menu | Expandable sections | Ecommerce |

---

## 4. Desktop Design

### 4.1 Desktop Advantages

- **Larger screen**: Support multi-column, sidebars, panels, and split views
- **Keyboard + mouse**: Support keyboard shortcuts, hover states, right-click context menus
- **Window management**: Support resize, minimize, maximize. Remember window position
- **Multi-tasking**: Users often have other apps open. Support copy-paste, drag-and-drop between apps
- **Precision**: Mouse targeting allows for smaller elements (20×20px minimum vs 44px on mobile)

### 4.2 Desktop Patterns

- **Dashboard layout**: Navigation sidebar + content area + optional detail panel
- **Document/editor layout**: Toolbar on top, canvas/content in center, properties on right
- **Data table**: Filters on top, sortable columns, action column on right, pagination or infinite scroll
- **Wizard**: Step indicator at top, content in center, back/next/cancel at bottom
- **Split pane**: Resizable panels for comparison or master-detail views

### 4.3 Desktop-Specific Considerations

- **Hover states**: Essential for indicating interactivity. Every button, link, and interactive element needs a hover state.
- **Keyboard shortcuts**: Essential for power users. Document shortcuts visibly (in menus) and support standard OS shortcuts.
- **Right-click**: Don't hide primary actions in context menus, but add convenient shortcuts there.
- **Drag and drop**: Support for file uploads, reordering, linking items between panels.
- **Resize**: Fluid layouts that adapt to window resize. Test at 1024×768 minimum (still a common resolution for enterprise).
- **Scroll**: Content-heavy pages should support scroll, not pagination (for browsing). Paginate tables.

---

## 5. Cross-Platform Design

### 5.1 Platform-First vs Cross-Platform

| Approach | Description | Pros | Cons |
|---|---|---|---|
| **Native each platform** | Separate iOS and Android designs | Best platform experience | 2× design effort |
| **Cross-platform (same UI)** | One design, same behavior | Consistency, efficiency | May not feel native on either |
| **Shared core + platform tweaks** | Same flow and content; platform-specific controls and navigation | Best balance | Requires platform knowledge |

### 5.2 What to Keep Consistent
- Brand identity (colors, typography, logo, illustration style)
- Content and messaging
- Core user flows and task logic
- Information architecture (mostly)
- Accessibility standards

### 5.3 What to Adjust Per Platform
- Navigation pattern (tab bar vs bottom nav)
- UI component library (iOS UIKit vs Material components)
- Gesture handling (left-edge swipe on iOS, hardware back on Android)
- Typography (SF Pro vs Roboto)
- Iconography (filled vs outline tradition)
- Spacing and sizing (44pt vs 48dp touch targets)
- Modal presentations (sheet vs dialog)
- Platform-specific features (widgets, shortcuts, sharing, etc.)

---

## When to Read This File

Read `platform-design.md` when:
- Designing for iOS, Android, web, or desktop
- Creating cross-platform experiences
- Building responsive or adaptive layouts
- Ensuring platform convention compliance
- Reviewing designs for platform-specific issues

**Document reference**: iOS HIG, Material Design 3, responsive/adaptive patterns, desktop design, cross-platform strategy
**Last updated**: July 2026
