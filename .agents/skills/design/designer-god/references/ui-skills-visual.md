# Visual Design Craft, Color and Typography Reference

Advanced visual properties, typography setups, color system rules (including OKLCH), shadows, layout balance, visual rhythm, and distinctive aesthetics (Swiss, Minimalist, Brutalist).

---

## Beautiful Shadows (`mengto/beautiful-shadows`)

npx skills add https://github.com/MengTo/Skills --skill beautiful-shadows

---

## Better Colors (`jakubkrehel/better-colors`)


### OKLCH Colors

OKLCH is a perceptually uniform color space where the numbers actually mean what you think they mean. Most color problems in CSS (broken palettes, failing contrast, hue drift) come from using color spaces that don't match how we see. OKLCH fixes the model so the tools work. To explore interactively, visit [oklch.fyi](https://oklch.fyi).

#### Quick Reference

| Category | When to use | Reference |
| --- | --- | --- |
| Conversion | Hex/rgb/hsl to oklch | [color-conversion.md](color-conversion.md) |
| Palettes | Generate scales, multi-hue, dark mode | [palette-generation.md](palette-generation.md) |
| Contrast | APCA/WCAG checks, fixing failing contrast | [accessibility-contrast.md](accessibility-contrast.md) |
| Gamut & Tailwind | P3 fallbacks, `@theme` scales, gamut clamping | [gamut-and-tailwind.md](gamut-and-tailwind.md) |

#### Why OKLCH

- **Perceptual uniformity.** Equal L steps = equal brightness. `oklch(0.5 ...)` is visually mid. HSL's `lightness: 50%` varies wildly by hue.
- **Stable hue.** HSL blue shifts toward purple as lightness changes. OKLCH hue stays constant across the full lightness range.
- **Independent chroma.** Chroma is an absolute measure of colorfulness that doesn't depend on lightness. HSL saturation does.
- **Finite gamut.** Not every oklch value maps to a displayable sRGB color. High-chroma values at certain hues will clip; gamut awareness is required.

#### OKLCH Syntax

```
oklch(L C H)
oklch(L C H / alpha)
```

| Channel | Range | Description |
| --- | --- | --- |
| L (Lightness) | 0–1 | 0 = black, 1 = white. Perceptually uniform. |
| C (Chroma) | 0–~0.4 | Colorfulness. 0 = gray. Max depends on L and H. |
| H (Hue) | 0–360 | Hue angle in degrees. |
| alpha | 0–1 | Optional transparency. Slash syntax. |

```css
oklch(0.637 0.237 25.331)
oklch(0.8 0.05 200 / 0.5)
```

**Formatting:** L and C use 3 decimal places, H uses up to 3. Drop trailing zeros. Format `-0` as `0`. Browser support: Baseline 2023, 96%+ global coverage.

#### Key Thresholds

| Rule | Value |
| --- | --- |
| Light/dark boundary | L > 0.6 = light background → use dark text |
| Lightness gap (light bg) | Foreground L < 0.35 when background L > 0.9 |
| Lightness gap (dark bg) | Foreground L > 0.9 when background L < 0.25 |
| Hue drift threshold | > 10° spread across palette steps = visible drift |
| APCA body text | \|Lc\| >= 75 minimum, >= 90 preferred |
| APCA non-body text | \|Lc\| >= 60 minimum |
| WCAG 2 normal text | 4.5:1 AA, 7:1 AAA |
| Contrast fix | Adjust L only; chroma has negligible effect |

#### Review Output Format

Always present color changes as a markdown table with **Before** and **After** columns. Include **every color that was changed**, not just a subset. Never list findings as separate "Before:" / "After:" lines outside of a table.

| Before | After |
| --- | --- |
| `color: #3b82f6` | `color: oklch(0.623 0.188 259.815)` |
| Same absolute C across hues | Same C% of each hue's max chroma |
| No sRGB fallback for P3 color | `@media (color-gamut: p3)` wrapper |

This keeps feedback scannable and diff-friendly. Each row is a self-contained change the developer can act on independently.

#### Common Mistakes

| Issue | Fix |
| --- | --- |
| Hex/rgb/hsl color in new code | Convert to `oklch()` |
| HSL palette ramp with hue drift | Rebuild with constant oklch hue |
| Failing contrast (check foreground vs its background using APCA) | Adjust oklch L channel, keep C and H |
| High chroma without gamut check | Clamp to max chroma for the L/H in sRGB |
| Same absolute C across different hues | Use same C% (percentage of max) for consistent vividness |
| P3 color without sRGB fallback | Add `@media (color-gamut: p3)` pattern |
| Dark mode with hand-picked colors | Derive from light palette by reversing L mapping |
| Hex in Tailwind v4 `@theme` | Convert to oklch values |
| Alpha with comma syntax | Use slash: `oklch(L C H / alpha)` |

#### Reference Files

- [color-conversion.md](color-conversion.md): Supported formats, conversion examples, bulk conversion rules, what to leave alone
- [palette-generation.md](palette-generation.md): Scale convention, generation algorithm, multi-hue palettes, dark mode, why not HSL
- [accessibility-contrast.md](accessibility-contrast.md): APCA and WCAG 2 thresholds, fixing contrast with L, lightness gap guide, hue drift detection
- [gamut-and-tailwind.md](gamut-and-tailwind.md): sRGB vs P3, gamut clamping, CSS fallback patterns, Tailwind v4 @theme and migration


---

## Better Typography (`jakubkrehel/better-typography`)


### Great typography

Good typography is mostly restraint. A sensible scale, comfortable spacing and enough contrast beat any clever effect. A label, a table cell, a marketing headline and an article paragraph should not share one set of rules. Apply these principles when building or reviewing anything with text in it.

**Match the project's styling system.** Before suggesting or writing any fix, check how the codebase styles things and express every change in that system: Tailwind utilities in a Tailwind project, plain declarations in CSS, CSS Modules, styled-components or StyleX. The [cheat sheet](css-cheat-sheet.md) maps each declaration to its Tailwind equivalent. Never introduce a second styling approach just to apply a typography fix.

#### Quick Reference

| Category | When to use | Reference |
| --- | --- | --- |
| Choosing fonts | Font categories, pairing, formats, typeface anatomy | [choosing-fonts.md](choosing-fonts.md) |
| Variable fonts & OpenType | Axes, weights, tabular numbers, stylistic sets | [variable-fonts-and-opentype.md](variable-fonts-and-opentype.md) |
| Spacing & sizing | Type scale, heading hierarchy, line-height, letter-spacing, text trimming | [spacing-and-sizing.md](spacing-and-sizing.md) |
| Wrapping & punctuation | Measure, wrapping, truncation, smart punctuation, RTL | [wrapping-and-punctuation.md](wrapping-and-punctuation.md) |
| Details & accessibility | Underlines, selection, forms, decorative text, contrast | [details-and-accessibility.md](details-and-accessibility.md) |
| CSS cheat sheet | Quick lookup of every property covered, with Tailwind equivalents | [css-cheat-sheet.md](css-cheat-sheet.md) |

#### Core Principles

### 1. Serve the Right Format

Use `.woff2` (Brotli compression, broadly supported) on the web. `.woff` is a fallback only for very old browsers; `.ttf` and `.otf` are raw desktop formats with no web compression. How the files are loaded is the project's own concern, this skill does not prescribe it.

### 2. Properties Over Raw Tags

When a CSS property exists, use it. `font-weight: 650` instead of `font-variation-settings: "wght" 650`, `font-optical-sizing: auto` instead of `"opsz"`, `font-variant-numeric: tabular-nums` instead of `font-feature-settings: "tnum" 1`. Properties keep working when a non-variable fallback renders. Reserve the raw-tag properties for custom axes (`"GRAD" 80`) and niche features (`"ss01" 1`) that have no property of their own.

### 3. No Fake Weights

When a weight or style is not loaded, the browser synthesizes it. That is a safety mechanism, not a feature. Set `font-synthesis: none` so missing files fail visibly instead of rendering a faked bold or italic.

### 4. Fewer Fonts, Sizes and Weights

Rarely use more than three fonts. Weight and size define hierarchy, but overusing them hurts readability quickly. Pair for contrast, not similarity: a serif headline with a sans body reads as deliberate, two near-identical sans-serifs read as a mistake.

### 5. Use a Type Scale with Semantic Names

Define a small set of sizes and deviate from it as little as possible. Hard-coded sizes without a system break down at scale. For solo projects, default names like `text-sm` work fine as long as the usage rules are clear. On a team, name sizes by use (`text-body-sm`), not by size, so the rules stay consistent.

### 6. Heading Sizes Descend with Level

Map each heading level used on a page to a descending step of the type scale: a lower level must never render larger than a higher one on the same page. Adjacent levels may share a size toward the small end of the scale as long as weight or spacing keeps them distinct. Pick the tag from the document outline and control the size with CSS; never skip levels or reach for an `h4` because it "looks right".

### 7. Line-Height by Role

Headings tighter, around `1.1`. Body copy `1.5` to `1.6`. Prefer unitless values so line-height scales with the font size; fixed values like `24px` do not.

### 8. Letter-Spacing by Size

Large headings often look better with slightly negative letter-spacing. Small uppercase labels need a little positive letter-spacing so letters do not feel crowded. Body copy at reading sizes needs neither.

### 9. Cap the Measure

Long lines make it hard for the eye to find the next line. Cap long-form text around 60–75 characters per line. Any unit works: `65ch` measures characters directly, and a pixel or rem cap is just as good: at a `16px` body size the range lands roughly between `560px` and `680px` depending on the font, so Tailwind's `max-w-xl` or `max-w-2xl` fit. What matters is that a cap exists and the resulting line length sits in range.

### 10. Wrap Deliberately

`text-wrap: balance` distributes text evenly across lines: use it on headings. `text-wrap: pretty` avoids leaving a single short word on the final line: use it on descriptions. Skip both in long-form text: browsers ignore `balance` past a few lines anyway, and evening out a whole paragraph wastes space and makes it harder to read. `overflow-wrap: break-word` where long words, links or IDs could escape the container. `white-space: nowrap` on labels and badges where a line break looks broken.

### 11. Tabular Numbers on Changing Values

Digits have different widths by default, so timers, counters and prices shift layout as they update. Apply `font-variant-numeric: tabular-nums` to any value that changes.

### 12. Truncate Without Losing Content

Single line: `text-overflow: ellipsis` with `overflow: hidden` and `white-space: nowrap`. Multiple lines: `line-clamp`. Truncation hides content, so if the missing text matters, keep the full value reachable in a tooltip or expanded view.

### 13. Write Copy Naturally, Style with CSS

Store text in natural case and control presentation with `text-transform`, so redesigns never require rewriting copy. Use smart punctuation: curly quotes in prose (straight quotes in code), an en dash for ranges like `2010–2020`, an em dash to set off a thought, the single ellipsis character, `&nbsp;` to keep values like `16 px` together and `&shy;` to control where long words may break.

### 14. Underlines from the Font

Default underlines sit wherever the browser decides. Pull position and thickness from the font's own metrics with `text-underline-position: from-font` and `text-decoration-thickness: from-font`, or tune manually with `text-decoration-thickness`, `text-underline-offset` and `text-decoration-skip-ink`. `text-decoration-style` draws the line dotted, dashed or wavy; a dotted underline is a common hint that a word carries extra information, like an abbreviation or a defined term. Unless the only thing animating is a color change, build the underline as a separate element instead of using `text-decoration`: color is the only part of a real underline that animates reliably.

### 15. Inputs at 16px on Mobile

iOS Safari zooms the whole page when an input's text is smaller than `16px`. Keep input text at `16px` on mobile viewports (`text-base sm:text-sm`). Avoid the `maximum-scale=1` viewport meta: Safari ignores it for pinch zoom, but every other browser honors it and blocks zooming, which fails WCAG.

### 16. Size and Contrast Floors

Body text `16px` (the web default and the right reading size). UI text can go smaller: `14px` for inputs and menus (inputs still need `16px` on mobile, see principle 15), `13px` for captions, rarely below `12px`. WCAG AA: `4.5:1` contrast for regular text, `3:1` for large text (roughly `24px` and up).

### 17. Font Smoothing on the Root

On macOS text renders heavier than intended. Apply `-webkit-font-smoothing: antialiased` and `-moz-osx-font-smoothing: grayscale` (both covered by Tailwind's `antialiased`) once on the root layout so they cover all text.

### 18. Logical Properties for Direction

To support right-to-left content, use direction-agnostic properties: `margin-inline-start` instead of `margin-left`, `text-align: start` instead of `left`. Set `lang` so browsers pick the right quotes and hyphenation, and `dir="rtl"` where needed.

### 19. Style the Selection, Disable It Where It Distracts

`::selection` is a subtle way to embed brand in the reading experience; keep the combination legible. Use `user-select: none` on button labels where copying is unlikely and selection feels distracting, and make sure `cmd+A` only grabs text the user expects to copy. In cross-platform apps that feel closer to native, disable selection for the interface and keep it only on content worth copying.

#### Review Output Format

Always present changes as a markdown table with **Before** and **After** columns. Include every change you made, not just a subset. Never list findings as separate "Before:" / "After:" lines outside of a table. Group changes by principle using a heading above each table, and keep each row focused on a single diff. Write every **After** snippet in the styling system the project already uses.

### Example

#### Tabular numbers
| Before | After |
| --- | --- |
| `<span>{price}</span>` on live price | `<span className="tabular-nums">{price}</span>` |
| `font-feature-settings: "tnum" 1` | `font-variant-numeric: tabular-nums` |

#### Line-height and measure
| Before | After |
| --- | --- |
| `leading-none` on body paragraph | `leading-normal` (body needs `1.5`–`1.6`) |
| Full-width article column | `max-w-2xl` (~65 characters per line at `16px`) |

Rows should cite the specific file and property when it is not obvious from the snippet. If a principle was reviewed but nothing needed to change, omit that table entirely.

#### Common Mistakes

| Mistake | Fix |
| --- | --- |
| `.ttf`/`.otf` served on the web | Convert to `.woff2` |
| `font-variation-settings: "wght"` for weight | `font-weight` (works with non-variable fallbacks) |
| `font-feature-settings: "tnum" 1` | `font-variant-numeric: tabular-nums` |
| Browser-faked bold or italic | Load the file, set `font-synthesis: none` |
| Hard-coded one-off font sizes | Use the type scale |
| `h3` rendered larger than `h2` on the same page | Map heading levels to descending scale steps |
| Heading tag picked for its size, skipping levels | Level from the document outline, size via CSS |
| `line-height: 24px` on scalable text | Unitless value (`1.5`) |
| Full-width paragraphs | Cap around 60–75 characters per line |
| Orphan on the last line of a paragraph | `text-wrap: pretty` |
| Lopsided two-line heading | `text-wrap: balance` |
| Numbers cause layout shift | `tabular-nums` |
| Truncated text with no way to read it | Tooltip or expanded view for the full value |
| `UPPERCASE` typed into copy | Natural case + `text-transform` |
| Justified text in an interface | `text-align: start`; reserve justify for specific editorial layouts |
| Underline cuts through descenders | `text-decoration-skip-ink: auto`, `from-font` metrics |
| Inputs below `16px` zoom on iOS | `text-base sm:text-sm` |
| `margin-left` in RTL-capable UI | `margin-inline-start` |
| Selectable button labels in native-feel UI | `user-select: none`, keep selection on real content |
| Extra-info hint with no visual cue | Dotted underline via `text-decoration-style: dotted` |
| Tailwind classes dropped into a CSS-in-JS codebase (or the reverse) | Express the fix in the styling system the project already uses |

#### Review Checklist

- [ ] Web fonts are `.woff2`
- [ ] `font-weight` / `font-variant-*` used instead of raw axis and feature tags
- [ ] `font-synthesis: none` set; no faked weights or styles
- [ ] Sizes come from the type scale, no one-off values
- [ ] Heading sizes descend with level (`h1` ≥ `h2` ≥ `h3`…), levels stay visually distinct, none skipped
- [ ] Headings ~`1.1` line-height, body `1.5`–`1.6`, unitless
- [ ] Large headings have slightly negative tracking, small uppercase labels positive
- [ ] Long-form text capped around 60–75 characters per line
- [ ] Headings use `text-wrap: balance`, body uses `text-wrap: pretty`
- [ ] Changing numbers use `tabular-nums`
- [ ] Truncated content is reachable in full somewhere
- [ ] Copy stored in natural case, presentation via `text-transform`
- [ ] Underlines use `from-font` or tuned thickness, offset and skip-ink
- [ ] Inputs are `16px`+ on mobile viewports
- [ ] Text sizes and contrast meet the floors (`16px` body, `4.5:1` / `3:1`)
- [ ] `antialiased` applied once on the root layout
- [ ] Directional properties are logical (`inline-start`, `start`)
- [ ] Any styled `::selection` stays legible


---

## Better UI (`jakubkrehel/better-ui`)


### Details that make interfaces feel better

Great interfaces rarely come from a single thing. It's usually a collection of small details that compound into a great experience. Apply these principles when building or reviewing UI code.

Typography (text wrapping, font smoothing, tabular numbers, spacing) is covered by the `better-typography` skill; use that for anything text-related.

#### Quick Reference

| Category | When to Use |
| --- | --- |
| [Surfaces](surfaces.md) | Border radius, optical alignment, shadows, image outlines, hit areas |
| [Animations](animations.md) | Interruptible animations, enter/exit transitions, icon animations, scale on press |
| [Performance](performance.md) | Transition specificity, `will-change` usage |

#### Core Principles

### 1. Concentric Border Radius

Outer radius = inner radius + padding. Mismatched radii on nested elements is the most common thing that makes interfaces feel off.

### 2. Optical Over Geometric Alignment

When geometric centering looks off, align optically. Buttons with icons, play triangles, and asymmetric icons all need manual adjustment.

### 3. Shadows Over Borders

Layer multiple transparent `box-shadow` values for natural depth. Shadows adapt to any background; solid borders don't.

### 4. Interruptible Animations

Use CSS transitions for interactive state changes: they can be interrupted mid-animation. Reserve keyframes for staged sequences that run once.

### 5. Split and Stagger Enter Animations

Don't animate a single container. Break content into semantic chunks and stagger each with ~100ms delay.

### 6. Subtle Exit Animations

Use a small fixed `translateY` instead of full height. Exits should be softer than enters.

### 7. Contextual Icon Animations

Animate icons with `opacity`, `scale`, and `blur` instead of toggling visibility. Use exactly these values: scale from `0.25` to `1`, opacity from `0` to `1`, blur from `4px` to `0px`. If the project has `motion` or `framer-motion` in `package.json`, use `transition: { type: "spring", duration: 0.3, bounce: 0 }`; bounce must always be `0`. If no motion library is installed, keep both icons in the DOM (one absolute-positioned) and cross-fade with CSS transitions using `cubic-bezier(0.2, 0, 0, 1)`; this gives both enter and exit animations without any dependency.

### 8. Image Outlines

Add a subtle `1px` outline with low opacity to images for consistent depth. The color must be pure black in light mode (`oklch(0 0 0 / 0.1)`) and pure white in dark mode (`oklch(1 0 0 / 0.1)`), never a near-black like slate, zinc, or any tinted neutral. A tinted outline picks up the surface color underneath it and reads as dirt on the image edge.

### 9. Scale on Press

A subtle `scale(0.96)` on click gives buttons tactile feedback. Always use `0.96`. Never use a value smaller than `0.95`: anything below feels exaggerated. Add a `static` prop to disable it when motion would be distracting.

### 10. Skip Animation on Page Load

Use `initial={false}` on `AnimatePresence` to prevent enter animations on first render. Verify it doesn't break intentional entrance animations.

### 11. Never Use `transition: all`

Always specify exact properties: `transition-property: scale, opacity`. Tailwind's `transition-transform` covers `transform, translate, scale, rotate`.

### 12. Use `will-change` Sparingly

Only for `transform`, `opacity`, `filter`, the properties the GPU can composite. Never use `will-change: all`. Only add when you notice first-frame stutter.

### 13. Minimum Hit Area

Interactive elements need a 44×44px hit area for touch or mobile contexts. In desktop interfaces, use at least 40×40px. Extend with a pseudo-element if the visible element is smaller. Never let hit areas of two elements overlap.

#### Common Mistakes

| Mistake | Fix |
| --- | --- |
| Same border radius on parent and child | Calculate `outerRadius = innerRadius + padding` |
| Icons look off-center | Adjust optically with padding or fix SVG directly |
| Hard borders between sections | Use layered `box-shadow` with transparency |
| Jarring enter/exit animations | Split, stagger, and keep exits subtle |
| Animation plays on page load | Add `initial={false}` to `AnimatePresence` |
| `transition: all` on elements | Specify exact properties |
| First-frame animation stutter | Add `will-change: transform` (sparingly) |
| Tiny hit areas on small controls | Extend with a pseudo-element to 44×44px for touch/mobile, or at least 40×40px in desktop UI |

#### Review Output Format

Always present changes as a markdown table with **Before** and **After** columns. Include every change you made, not just a subset. Never list findings as separate "Before:" / "After:" lines outside of a table. Group changes by principle using a heading above each table, and keep each row focused on a single diff so the reader can scan the whole list quickly.

### Example

#### Concentric border radius
| Before | After |
| --- | --- |
| `rounded-xl` on card + `rounded-xl` on inner button (`p-2`) | `rounded-2xl` on card (`8 + 8 = 16`), `rounded-lg` on inner button |
| `border-radius: 16px` on both nested surfaces | Outer `24px`, inner `16px` with `8px` padding |

#### Scale on press
| Before | After |
| --- | --- |
| `<button className="...">` | Added `active:scale-[0.96] transition-transform` |
| `scale(0.9)` on press | Raised to `scale(0.96)`; anything below `0.95` feels exaggerated |

Rows should cite the specific file and the specific property that changed when it isn't obvious from the snippet. If a principle was reviewed but nothing needed to change, omit that table entirely: empty tables add noise.

#### Review Checklist

- [ ] Nested rounded elements use concentric border radius
- [ ] Icons are optically centered, not just geometrically
- [ ] Shadows used instead of borders where appropriate
- [ ] Enter animations are split and staggered
- [ ] Exit animations are subtle
- [ ] Images have subtle outlines
- [ ] Buttons use scale on press where appropriate
- [ ] AnimatePresence uses `initial={false}` for default-state elements
- [ ] No `transition: all`, only specific properties
- [ ] `will-change` only on transform/opacity/filter, never `all`
- [ ] Interactive elements have 44×44px hit areas for touch/mobile, or at least 40×40px in desktop UI

#### Reference Files

- [surfaces.md](surfaces.md): Border radius, optical alignment, shadows, image outlines
- [animations.md](animations.md): Interruptible animations, enter/exit transitions, icon animations, scale on press
- [performance.md](performance.md): Transition specificity, `will-change` usage


---

## Industrial Brutalist UI (`leonxlnx/brutalist-skill`)

npx skills add https://github.com/Leonxlnx/taste-skill --skill industrial-brutalist-ui

---

## Container Lines (`mengto/container-lines`)

npx skills add https://github.com/MengTo/Skills --skill container-lines

---

## Design Taste Frontend (`mengto/design-taste-frontend`)

npx skills add https://github.com/MengTo/Skills --skill design-taste-frontend

---

## Gpt Taste (`mengto/gpt-taste`)

npx skills add https://github.com/MengTo/Skills --skill gpt-taste

---

## Gpt Taste (`leonxlnx/gpt-tasteskill`)

npx skills add https://github.com/Leonxlnx/taste-skill --skill gpt-taste

---

## High End Visual Design (`mengto/high-end-visual-design`)

npx skills add https://github.com/MengTo/Skills --skill high-end-visual-design

---

## Make Interfaces Feel Better (`jakubkrehel/make-interfaces-feel-better`)

npx skills add https://github.com/jakubkrehel/make-interfaces-feel-better --skill make-interfaces-feel-better

---

## Minimalist UI (`leonxlnx/minimalist-skill`)

npx skills add https://github.com/Leonxlnx/taste-skill --skill minimalist-ui

---

## Oklch Skill (`jakubkrehel/oklch-skill`)

npx skills add https://github.com/jakubkrehel/oklch-skill --skill oklch-skill

---

## Progressive Blur (`mengto/progressive-blur`)

npx skills add https://github.com/MengTo/Skills --skill progressive-blur

---

## High End Visual Design (`leonxlnx/soft-skill`)

npx skills add https://github.com/Leonxlnx/taste-skill --skill high-end-visual-design

---

## Stitch Design Taste (`mengto/stitch-design-taste`)

npx skills add https://github.com/MengTo/Skills --skill stitch-design-taste

---

## Stitch Design Taste (`leonxlnx/stitch-skill`)

npx skills add https://github.com/Leonxlnx/taste-skill --skill stitch-design-taste

---

## Swiss Design (`zeke/swiss-design`)

npx skills add https://github.com/zeke/swiss-design-skill --skill swiss-design

---

## Design Taste Frontend (`leonxlnx/taste-skill`)

npx skills add https://github.com/Leonxlnx/taste-skill --skill design-taste-frontend

---
