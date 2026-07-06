# Editor Types & UI — Reference

## Classic Editor vs. Wix Studio vs. Editor X

| Feature | Classic Editor | Wix Studio | Editor X (Legacy) |
|---------|---------------|------------|-------------------|
| Layout System | Absolute positioning | CSS Grid + Flexbox | CSS Grid + Flexbox |
| Responsive Design | Manual (separate mobile view) | True responsive, breakpoints | True responsive, breakpoints |
| Complexity | Low to Medium | Medium to High | Medium to High |
| Best For | Beginners, simple sites | Professionals, agencies | (Being migrated to Studio) |
| Custom CSS | Limited (via Velo) | Built-in per element | Built-in per element |
| Design Tokens | No | Yes | Limited |
| Components | No | Yes (reusable) | No |
| Velo Support | Full | Full | Full |
| Mobile Editor | Separate mobile view | Breakpoint-based | Breakpoint-based |
| Status | Active | Active (primary) | Legacy (no new features) |

---

## Classic Editor — Quick Reference

### Interface
- **Top bar**: Wix Logo, Site Name, Preview, Publish, Upgrade
- **Left panel**: Add (+), Pages, Design, App Market, Media, Blog, Store, Bookings
- **Canvas**: Drag-and-drop with absolute positioning
- **Right panel**: Element settings (Layout, Design, Animate) when element selected

### Adding Elements
**Path:** Left Panel → Add (+) → Choose category

Categories: Text, Image, Gallery, Button, Video, Music, Box, Shape, Interactive (accordions, tabs, slides), Form, Social, More (countdown, progress bars, chat), Embed (HTML iFrame), Menu

### Strips (Sections)
Full-width horizontal containers — the primary structural unit.
- **Add**: Add panel → Strip → choose layout, or right-click between sections → Add Section
- **Settings**: Background (color, gradient, image, video, slideshow), Height (auto/fixed), Width (full/constrained), Columns
- **Mobile**: Columns auto-stack on mobile (left→right becomes top→bottom)

### Header & Footer
- Site-wide on all pages unless overridden
- **Hide on specific pages**: Page Settings → Show Header/Show Footer toggles
- Header modes: Always visible (sticky), Scrolls with page, Fade in on scroll

### Page Management
**Path:** Left Panel → Pages
- Add Page, Rename, Duplicate, Delete, Set Homepage
- Page Settings: SEO, permissions, custom URL

**Page Types:** Regular, Blank, Dynamic (CMS-connected), Router (Velo routing)

### Mobile Editor (Classic)
**Separate editor** — desktop changes don't auto-apply to mobile.
- **Access**: Top bar → phone icon
- Elements can be hidden on mobile (right-click → Hide on Mobile)
- Elements can be repositioned independently
- Text sizes adjustable per device
- Column stacking: multi-column strips auto-stack

**Common mobile fixes:**
| Problem | Fix |
|---------|-----|
| Elements overlapping | Switch to mobile editor, manually rearrange |
| Element too wide | Select in mobile editor, resize |
| Hidden elements still taking space | Use "Hide on Mobile" (not just visibility) |

### Layers Panel
- **Access**: Right-click canvas → Layers
- Shows z-order of all page elements
- Drag to reorder z-index

---

## Wix Studio — Quick Reference

### Key Differences from Classic
- True responsive design with CSS Grid/Flexbox
- Breakpoints (Desktop 1280px+, Tablet 768-1279px, Mobile 320-767px, Custom)
- Design tokens (reusable color/font/spacing/shadow/border variables)
- Reusable Components with variants and slots
- Custom CSS per element in Inspector panel
- Stack & Grid layout containers
- AI Layout Assistant (sparkle icon → describe layout → AI builds it)

### Layout Types
1. **Stack (Flexbox)** — vertical/horizontal, gap control, wrapping
2. **Grid** — CSS Grid, define rows/columns with px/%, fr units
3. **Fixed** — Absolute positioning within container
4. **AI Layout** — Describe what you want, AI auto-creates the layout

Set on container: Right-click → Set Layout → Stack / Grid / Fixed

### Breakpoints
| Breakpoint | Range |
|-----------|-------|
| Desktop | 1280px+ |
| Tablet | 768 – 1279px |
| Mobile | 320 – 767px |
| Custom | Any width |

- Changes at a breakpoint cascade downward (affects that breakpoint + narrower)
- **Breakpoint syncing**: Toggle to sync specific properties across breakpoints
- **Breakpoint presets**: Save custom breakpoint configs for reuse
- **Common mistake**: Editing on desktop and expecting mobile to auto-update — it won't

### Design Tokens
**Access:** Left Panel → Design Tokens (or Design Library)

**Categories:** Color, Font, Spacing, Border, Shadow, Border Radius

**Create token:** (+) → Name (e.g., `--color-primary`) → Set value → Apply in Inspector

**Enhanced features:**
- Token modes (light/dark mode sets)
- Token inheritance (tokens referencing other tokens)
- Responsive tokens (different values per breakpoint)
- Token sharing (export/import between sites)

### Components
Reusable design blocks (like Figma/React components).

**Create:** Build design → Right-click → Create Component → Name it

**Use:** Left Panel → Components → drag to page

**Properties:** Custom inputs per instance (text, images, colors, toggles, dropdowns, numbers, files, rich text)

**Variants (2024+):** Multiple style variants per component (e.g., primary/secondary button)
- Switch between variants in Inspector
- Variant switching controllable via Velo

**Slots (2024+):** Placeholder areas within components for custom content (like React `children`)

**Detach:** Right-click instance → Detach from Component → becomes independent

### Custom CSS per Element
**Access:** Select element → Inspector Panel → scroll to "Custom CSS"

**Supported:** Most standard CSS. Wix blocks dangerous/layout-breaking properties.

**CSS Variable usage:**
```css
color: var(--color-primary);
font-family: var(--font-heading);
margin: var(--spacing-md);
width: calc(var(--spacing-md) * 2);
background-color: hsl(var(--hue), 80%, 50%);
```

**Pseudo-selectors:**
```css
:host:hover { transform: translateY(-2px); }
:host:focus-within { outline: 2px solid var(--color-primary); }
:host([data-variant="primary"]) { }  /* attribute-based variants */
```

**Style variants via data attributes:**
```html
<div data-variant="outline">Button</div>
```
```css
[data-variant="outline"] { border: 2px solid var(--color-primary); background: transparent; }
```

---

## Editor X (Legacy)

- **Status**: No new features; being migrated to Wix Studio
- New Editor X sites can no longer be created
- Existing sites continue to function
- Functionally similar to Studio (same CSS Grid/Flex, breakpoints, Velo)
- Migration to Studio requires rebuilding (no auto-conversion)
- Content collections, Velo code, CMS data can be reused

---

## Common Keyboard Shortcuts (Both Editors)

| Shortcut | Action |
|---------|--------|
| Ctrl+C / Cmd+C | Copy |
| Ctrl+V / Cmd+V | Paste |
| Ctrl+D / Cmd+D | Duplicate |
| Ctrl+Z / Cmd+Z | Undo |
| Ctrl+Y / Cmd+Y | Redo |
| Delete / Backspace | Delete element |
| Ctrl+A / Cmd+A | Select all |
| Ctrl+G / Cmd+G | Group |
| Esc | Deselect / exit edit mode |
