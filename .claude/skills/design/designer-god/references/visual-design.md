# Visual Design — Deep Reference

This is the deep reference for visual design craft: typography, color, spacing, layout, hierarchy, iconography, and imagery. Read this when creating or critiquing the visual layer of a design — choosing colors, setting up grids, styling type, or refining visual polish.

---

## 1. Typography

Typography is 90% of visual design. Most of what users perceive as "good design" is actually well-crafted typography.

### 1.1 Type Classification

| Category | Characteristics | Best for | Examples |
|---|---|---|---|
| **Serif** | Small lines (serifs) at end of strokes | Long-form reading, authority, tradition, editorial | Georgia, Merriweather, Playfair Display, Times New Roman |
| **Sans-serif** | No serifs, clean lines | UI text, body copy, modern/clean brands | Inter, SF Pro, Roboto, Open Sans, Helvetica |
| **Slab serif** | Heavy, blocky serifs | Headlines, emphasis, bold personality | Roboto Slab, Rockwell, Museo Slab |
| **Display/Decorative** | Highly stylized, unique | Logos, headlines, short text only | Lobster, Pacifico, Bebas Neue |
| **Monospace** | Fixed-width characters | Code, data, tables, technical content | JetBrains Mono, Fira Code, Consolas |

### 1.2 Typeface Selection

**Rule of thumb**: Use 1-2 typefaces max. If 1, use a variable-weight family (regular, medium, semibold, bold). If 2, use one for headings and one for body.

**Pairing strategies**:
- Contrast pairing: Serif heading + sans-serif body (or vice versa) — creates visual interest through contrast
- Same-family pairing: Same typeface, different weights — clean and harmonious
- Superfamily pairing: A typeface with both serif and sans-serif versions (e.g., Roboto + Roboto Slab, Source Sans + Source Serif)

**System fonts** (for performance-critical UI):
- **macOS/iOS**: SF Pro (sans-serif), SF Mono (monospace), New York (serif)
- **Windows**: Segoe UI (sans-serif), Cascadia Code (monospace)
- **Android**: Roboto (sans-serif), Noto (sans-serif/serif), Droid Sans Mono (monospace)
- **Web safe**: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif

### 1.3 Type Scale

A modular type scale creates consistent, harmonious size progression. Common ratios:

| Ratio | Example value | Feel |
|---|---|---|
| **Minor Second** (1.067) | 14, 15, 16, 17, 18px | Subtle; very small steps — conservative |
| **Major Second** (1.125) | 14, 16, 18, 20, 23px | Gentle; good for dense UI |
| **Minor Third** (1.200) | 14, 17, 20, 24, 29px | Pleasant; recommended for most UI |
| **Major Third** (1.250) | 14, 18, 22, 28, 34px | Noticeable steps; good for editorial |
| **Perfect Fourth** (1.333) | 14, 19, 25, 33, 44px | Dramatic; good for marketing pages |
| **Golden Ratio** (1.618) | 14, 23, 37, 60, 97px | Very dramatic; use carefully |

**Recommended baseline scale** (4pt system, Minor Third ratio):
```
text-xs:    12px / 16px   — Captions, badges, timestamps
text-sm:    14px / 20px   — Secondary text, metadata
text-base:  16px / 24px   — Body text
text-lg:    18px / 28px   — Large body, intro paragraphs
text-xl:    20px / 28px   — Subtitle, small heading
text-2xl:   24px / 32px   — H4 heading
text-3xl:   30px / 36px   — H3 heading
text-4xl:   36px / 40px   — H2 heading
text-5xl:   48px / 48px   — H1 heading
text-6xl:   60px / 56px   — Large hero heading
text-7xl:   72px / 64px   — Display heading
```

### 1.4 Readability Best Practices

| Parameter | Recommendation | Why |
|---|---|---|
| **Body size (web)** | 16-18px | Minimum readable for most users; 16px is WCAG recommended minimum |
| **Body size (mobile)** | 15-17px | Slightly smaller due to closer viewing distance |
| **Line height** | 1.4-1.6 (body), 1.1-1.3 (headings) | Tighter for headings, looser for body to improve readability |
| **Line length (measure)** | 50-75 characters (optimal), 45-85 (acceptable) | Lines too long are hard to scan; lines too short feel choppy |
| **Paragraph spacing** | 0.5-1× line height | Visually separates paragraphs without excessive gaps |
| **Letter spacing** | 0 (body), 0.01-0.05em (caps) | Tight for body; loosen slightly for ALL CAPS readability |
| **Font weight** | 400 (regular) for body, 600-700 for headings | Heavy body text looks chunky; light headings lack hierarchy |

### 1.5 Text Alignment

- **Left-aligned**: Default for UI, web, most reading. Most readable because of consistent starting point.
- **Center-aligned**: Use sparingly for short text blocks — headings, buttons, quotes. Longer center-aligned text is hard to read.
- **Right-aligned**: Useful for tables (numbers align to the right), right-aligned labels in some form designs. Rarely use for body text.
- **Justified**: Avoid on web. Variable spacing causes "rivers" of white space. Books use it because print gives precise control.

---

## 2. Color

### 2.1 Color Theory Basics

**Hue**: The pure color (red, blue, green, etc.)
**Saturation/Chroma**: The intensity of the color (vivid vs muted)
**Lightness/Value**: How light or dark the color is
**Temperature**: Warm (reds, oranges, yellows) vs Cool (blues, greens, purples)

**Color harmony types**:
- **Monochromatic**: One hue with varying saturation/lightness — simple, elegant, safe
- **Analogous**: Adjacent on the color wheel — harmonious, subtle, natural
- **Complementary**: Opposite on the color wheel — high contrast, energetic, use carefully
- **Split-complementary**: Base color + two adjacent to its complement — less tense than pure complement
- **Triadic**: Three evenly spaced colors — vibrant, requires balanced application
- **Tetradic**: Four colors (two complementary pairs) — complex, for advanced color systems

### 2.2 Building a UI Color System

A robust UI color system has these roles:

**Primary color** (1-3 shades):
- Brand color, main CTAs, selected states
- Most applications of primary color
- Define 50-900 scale (light to dark)

**Secondary/Accent color** (1-3 shades):
- Supporting actions, secondary CTAs, highlights
- Should harmonize with primary (complementary or analogous)

**Neutral/Neutral colors** (8+ shades):
- Text colors (900 = darkest, 50 = lightest)
- Background/surface colors
- Border, divider, disabled colors
- The most-used palette in the system

**Semantic colors** (4 categories × 3-5 shades each):

| Color | Meaning | UI use |
|---|---|---|
| **Green** | Success, confirm, complete | Success messages, check marks, progress complete |
| **Red** | Error, destructive, critical | Error messages, required fields, delete actions |
| **Orange/Amber** | Warning, caution | Warning messages, low quota, expiring items |
| **Blue** | Information, neutral update | Info messages, notifications, help links |

**Dark mode considerations**:
- Reduce saturation on dark backgrounds (highly saturated colors on dark backgrounds vibrate)
- Use tinted surfaces instead of pure black backgrounds (#121212 is better than #000000)
- Text should not be pure white (#E0E0E0 is better than #FFFFFF)
- Elevation = lighter surfaces (while light mode = elevation = darker shadows)
- Test all semantic colors on dark backgrounds — they may need separate values

### 2.3 Color Accessibility

**Minimum contrast ratios (WCAG 2.2)**:
- Normal text (< 18px, < 14px bold): **4.5:1** (AA)
- Large text (≥ 18px or ≥ 14px bold): **3:1** (AA)
- Enhanced text: **7:1** (AAA for normal, 4.5:1 for large)
- Non-text elements (icons, UI components): **3:1** against adjacent colors
- Focus indicators: **3:1** against adjacent colors

**Contrast calculation**: Luminance of lighter color + 0.05) ÷ (luminance of darker color + 0.05)

**Color blindness considerations**:
- 8% of men have some form of color blindness
- **Deuteranopia** (green-blind, most common): Avoid red/green differentiation
- **Protanopia** (red-blind): Avoid red/green differentiation
- **Tritanopia** (blue-yellow, rare): Avoid blue/yellow differentiation
- **Solutions**: Use icons + text + patterns + color to convey information. Never rely on color alone.

**Tools**: WebAIM Contrast Checker, Stark plugin, Axe dev tools, Color Blindness Simulator

### 2.4 Color Psychology & Cultural Context

| Color | Western associations | Eastern associations | UI applications |
|---|---|---|---|
| **Red** | Danger, passion, excitement, love | Luck, prosperity (China), purity (India) | Errors, CTAs (use carefully), sale/badge |
| **Blue** | Trust, stability, calm, security | Immortality (China), sadness (Korea) | Banking, tech, healthcare, informational |
| **Green** | Growth, nature, health, money | Trust (China), love (India) | Success, financial, environmental, medical |
| **Yellow** | Caution, optimism, warmth | Sacred (China), courage (Japan) | Warnings, highlights, children's products |
| **Orange** | Energy, creativity, affordability | Happiness (Japan), courage (India) | Secondary CTAs, recreation, food |
| **Purple** | Luxury, royalty, creativity | Wealth, power (Thailand) | Premium brands, creativity tools, beauty |
| **White** | Clean, pure, minimal | Mourning (China, India) | Backgrounds, negative space, medical |
| **Black** | Power, elegance, sophistication | Wealth (Japan), evil (India) | Text base, luxury, dark mode |

---

## 3. Spacing & Grid Systems

### 3.1 The 8px Grid System

The industry-standard approach to spacing. All spacing values are multiples of 8px (with 4px for tight spaces).

**Standard spacing scale**:
```
spacing-0:   0px
spacing-0.5: 4px    — Icons, very tight
spacing-1:   8px    — Small padding, gap between closely related items
spacing-1.5: 12px   — Padding inside cards, between form label and input
spacing-2:   16px   — Default padding, card padding, section spacing (base unit)
spacing-3:   24px   — Section spacing, large card padding
spacing-4:   32px   — Large section padding, page section gap
spacing-5:   40px   — Page margins (mobile), hero spacing
spacing-6:   48px   — Page margins (tablet), major sections
spacing-7:   56px   — Page margins (desktop narrow)
spacing-8:   64px   — Page margins (desktop wide), hero margins
spacing-9:   80px   — Wide gutters, special layouts
spacing-10:  96px   — Extra large spacing
spacing-11:  128px  — Maximum spacing
```

**Spacing relationships**:
- Related items: 8-12px apart
- Unrelated items: 20-32px apart
- Sections: 40-80px apart
- Page padding: 16-24px (mobile), 24-80px (desktop)

### 3.2 Layout Grid

**Column structures by breakpoint**:
```
Mobile (< 768px):   4-column grid, gutter 16px
Tablet (768-1199):  8-column grid, gutter 20-24px
Desktop (1200+):    12-column grid, gutter 20-24px
Wide (1600+):       12-column grid, gutter 24-32px
```

**Content width guidelines**:
```
Reading-focused:    640-720px max-width
Standard content:   960-1140px max-width
Dashboard/layout:   1200-1440px max-width
Full-width canvas:  100% (with max margin constraints)
```

**Vertical rhythm**:
All vertical spacing (margin-top, margin-bottom) should be a multiple of the baseline grid (4px or 8px). This creates consistent vertical rhythm so every element aligns to the grid regardless of content height.

### 3.3 Responsive Breakpoints (Tailwind-style)

```
xs:   0px     — Extra small devices (portrait phones)
sm:   640px   — Small devices (landscape phones)
md:   768px   — Medium devices (tablets)
lg:   1024px  — Large devices (desktop)
xl:   1280px  — Extra large devices (wide desktop)
2xl:  1536px  — Ultra wide screens
```

---

## 4. Visual Hierarchy

### 4.1 Creating Hierarchy

**Six tools for establishing hierarchy**:

1. **Size** — Larger = more important. Headlines > subheads > body > captions.
2. **Color and contrast** — Higher contrast = more important. Dark text on light background draws the eye first.
3. **Weight** — Bold = more important than regular. Variable weight family allows nuanced hierarchy.
4. **Position** — Top-left (in LTR languages) is perceived as most important. Center can also anchor attention.
5. **Spacing** — More space around = more importance. Elements with breathing room feel elevated.
6. **Texture/shape** — Textured, bordered, shadowed elements draw more attention than flat ones.

### 4.2 The Squint Test

Squint at your design so details blur and only large shapes and contrast remain. What you see:
- Can you still tell where the most important element is?
- Are there clear groupings that suggest relationships?
- Does anything feel chaotic or uniformly gray?

If the primary action isn't visible when squinting, the hierarchy needs work.

### 4.3 The 3-Second Test

Show the design for exactly 3 seconds. What should a user remember? If the answer isn't clear (page purpose, primary action, content organization), hierarchy needs improvement.

### 4.4 F-Pattern vs Z-Pattern

| Pattern | Use | Scanning behavior |
|---|---|---|
| **F-pattern** | Text-heavy, data-dense (articles, search results, lists) | Users scan horizontally across the top, then scan down the left side, then scan horizontally again |
| **Z-pattern** | Visual/sparse content (landing pages, marketing sites, splash screens) | Users scan top-left to top-right, then diagonally to bottom-left, then to bottom-right |

**Design accordingly**: Place critical information along the scan path. Put your CTA at the end point of the scan.

---

## 5. Iconography

### 5.1 Icon Style Guide

| Style | Characteristics | Best for |
|---|---|---|
| **Outline (stroke)** | Clean, minimal lines, consistent stroke weight | Modern interfaces, low visual weight needed |
| **Filled** | Solid shapes, bold | Navigation bars, tabs, selected states |
| **Two-tone** | Outline + accent color fill | Product features, illustrations, onboarding |
| **Duotone** | Two colors, often photo-based | Featured areas, editorial, hero sections |
| **Glyph** | Simplified silhouette | Universal symbols, wayfinding, signage |
| **Illustrated** | Detailed, artistic | Empty states, onboarding, brand moments |

### 5.2 Icon Grid Sizes

Standard icon grid (all in px with consistent padding):
```
16×16  — Inline text icons, badges, small indicators
20×20  — Compact toolbar, annotation icons
24×24  — Default icon size, most common
32×32  — Navigation icons, toolbars
40×40  — List item icons, feature icons
48×48  — App icons, large action buttons
64×64  — Feature spotlights, category icons
96×96  — Empty states, large indicators
```

### 5.3 Icon Best Practices

- **Test comprehension**: An icon a designer understands may not be understood by users. Test icons in context.
- **Always label navigation icons**: Especially on first encounter. On mobile bottom nav, always use icon + label.
- **Consistent visual language**: Same stroke weight, corner radius, 45°/90° angle usage, fill style across the entire system.
- **Consider RTL**: Ensure icons work in both LTR and RTL layouts. For example, a "back" arrow should flip in RTL.
- **Accessibility**: Always provide alt text for icons. Never use icons as the only way to convey information.
- **Touch target**: Ensure the tap area is 44×44px minimum even if the icon is smaller.

---

## 6. Imagery & Photography

### 6.1 Image Selection Principles

- **Purpose**: Every image should serve a purpose — illustrate a concept, evoke an emotion, or communicate information.
- **Diversity and inclusion**: Represent diverse people, cultures, abilities, and contexts authentically.
- **Avoid stock photo clichés**: Overly staged, generic handshake/headset photos undermine credibility. Use authentic, specific imagery.
- **Performance**: Optimize images aggressively. Use WebP/AVIF formats. Implement lazy loading. Provide responsive image sizes.
- **Legal**: Always use properly licensed images with model releases for people.

### 6.2 Illustration Style

When using illustrations:
- Match the brand personality (playful vs serious, minimalist vs detailed)
- Use consistent style across all illustrations (same line weights, color palette, character proportions)
- Consider dark mode variants
- Use illustrations strategically — empty states, onboarding, error pages, marketing moments

---

## When to Read This File

Read `visual-design.md` when:
- Creating a new visual design or refining an existing one
- Choosing colors, typefaces, or spacing for a project
- Building or modifying a visual design system
- Reviewing visual polish, hierarchy, or consistency
- Designing for accessibility (color contrast, readability)
- Debating font size, line height, or layout decisions

**Document reference**: Visual design craft — typography, color, layouts, hierarchy, iconography
**Last updated**: July 2026
