---
title: Anti-Slop Design Law
description: The definitive reference for avoiding AI-generated design slop. Contains specific patterns to avoid, verification checklists, and premium design patterns that signal genuine craft.
---

# Anti-Slop Design Law

**This is the definitive reference for avoiding AI-generated design slop.** Read this before starting any design work, keep it in mind while working, and verify against every point before shipping.

---

## Core Principle

**AI slop = Generic, low-effort, look-the-same AI output.** Avoid it by making real, deliberate choices. Every element on screen should exist because you decided it belongs there, not because it's a default.

---

## Specific Slop Patterns to Avoid

### Typography & Fonts

| Pattern | Why It's Slop | Better Approach |
|---------|---------------|-----------------|
| **Fraunces + Work Sans** pairing | Overused default "elegant" combo | Choose a distinctive display face + true neutral body |
| **Space Grotesk** for headlines | Default "techy SaaS" voice | License or self-host a characterful grotesque (Fontshare: Pally, Gambarino, Sentient, Tanker) |
| **Cormorant Garamond** | Default "luxury" serif used everywhere | Use a distinctive editorial serif with conviction |
| **Sora** | Default "AI/deep-tech" heading font | Reach for character, not trend |
| **Syne** | Default "edgy/creative" display font | Pick a face with real point of view |
| **Archivo** (all caps) | Default "streetwear/sporty" display | Use a distinctive licensed face |
| **Inter** as body everywhere | The most common slop font | System-ui is genuinely neutral and safe |
| **JetBrains Mono** everywhere | Default for all code + labels | Use mono only for actual data (timestamps, codes, prices) |
| **Young Serif** | Free Google display serif default | Choose a face with real character |
| **Default Google Fonts rotation** | Nearly every free Google font reads as slop when it carries the brand | **Hard rule:** The signature typeface must be licensed/self-hosted and chosen with conviction |

**Two hard rules on fonts:**
1. Stop cycling Google fonts hunting for the "safe one." The face carrying identity must be genuinely distinctive — usually a licensed or self-hosted typeface used with conviction.
2. Do not reuse a font (or the same serif-headline-plus-clean-sans pairing) you already used on another project. A recognizable house pairing repeated across briefs is itself a tell.

### Color & Gradients

| Pattern | Why It's Slop | Better Approach |
|---------|---------------|-----------------|
| **Purple / blue-to-purple gradients** | Single most recognizable slop color move | Pick a real, considered palette with color theory |
| **Glowy gradients (any adjacent hues)** | Reads as machine-made | Use tonal shifts, not saturated gradient pops |
| **Cool blue-charcoal dark mode** (`#0c0e15` family) | Default "serious dark product" base | Warm it, neutralize it, or push to a genuinely chosen hue (green-black, warm charcoal, oxblood-black) |
| **Pastel candy gradients** (butter-yellow → peach → strawberry-milk) | "AI startup landing" default | Single considered tone or crafted image |
| **Drifting soft-blend gradient blobs** (multiply + blur aurora) | Generic "soft gradient orbs" template | Authored directional light, crafted illustration, or grained gradient |
| **Radial glow halo behind object** | Centered symmetric bloom reads as slop | Real directional source with falloff |
| **Saturated accent color everywhere** | Template spray-paint | Tonal accents: value-shifted, desaturated tints |
| **The slop gray** (`#f3f4f6`, `#eceef2`, `#e7ecf3`) | Default UI-kit neutral = non-decision | Pick a real brand-specific surface tone |
| **Cream/beige "editorial" background** | New default "tasteful premium" = safe non-choice | Pick a real, specific background color for the brand |

### Layouts & Compositions (The Tells)

| Pattern | Why It's Slop | Better Approach |
|---------|---------------|-----------------|
| **The default hero stack** (kicker → headline → subline → 2 buttons) | On a million homepages | Break the axis, split/offset pieces, let signature artifact carry space |
| **Split hero** (text left + panel right) | Most over-shipped hero skeleton | Change axis, drop pieces, put content somewhere other than tidy left stack |
| **Three-tier pricing block** (Free/Pro/Enterprise with highlighted middle) | Entire layout is a preset | Design pricing from the brief, not the template |
| **The pre-footer CTA banner** (full-width gradient slab + headline + buttons) | Fixed template | Earn the CTA with real composition |
| **The logo lockup** (gradient icon tile + wordmark) | Instant made-by-AI logo | Bare mark, sized and colored with intent |
| **Kicker + serif H2 section head** | Template on nearly every section | Vary how sections begin: drop kicker, change scale, open with image/number/sentence |
| **Big serif statement block** (one large serif sentence + italic accent word) | Reflex, not composition | Compose deliberately |
| **Inset enquire island with form** | Default closing CTA, recolored every time | Design the closing from the brief |
| **Email-pill + button form** | Single most repeated component | Newsletter capture doesn't have to be pill + pill |
| **Image card with overlay caption** | Travel/product card preset | Custom wrapper for real content |
| **Flat fill under everything after hero** | Atmosphere stops at fold | Whole page needs atmosphere: imagery, texture, depth |
| **Multi-line headline (3+ lines)** | Tall staircase = no rhythm/composition | Hold to 1-2 lines or compose as real arrangement |
| **Filled + outlined button pair** | Stock fill-versus-outline duo | One clear action, or differentiate without the preset |
| **Small-label-over-big-heading** | Template for starting sections | Vary section openings |
| **Numbered steps beside vertical line** | "How it works" preset | Compose process some other way |
| **Labels as tinted pill chips everywhere** | Component-kit dashboard look | Real typographic hierarchy; reserve chips for genuine status needs |
| **The whole SaaS product-page template** (hero → 3 feature cards → tabs → pricing → FAQ → CTA slab → footer) | Default template with serial numbers filed off | Decide real signature first, build sections from brand/brief |

### Visual Effects & Decoration

| Pattern | Why It's Slop | Better Approach |
|---------|---------------|-----------------|
| **Lucide React icons everywhere** | Uniform thin-stroke look on every project | Custom iconography drawn for the brand |
| **Pill/eyebrow badge** (icon + text in rounded capsule) | Default hero decoration | Give labels presence through type/weight/color/spacing |
| **Oversized icon in colored tile** | "Icon in soft-colored box" everywhere | Bare icons, no container |
| **Floating cards** (bob/float/parallax) | Decorative motion with no purpose | Authored motion that responds to something |
| **Cut-off glow** (glow clipped by overflow:hidden) | Accidental hard edge on "premium" glow | Don't clip glows; design so they don't need clipping |
| **Kitchen-sink card** (icon tile + category pill + tag pills + divider + price + glowy button) | Piling every tell into one card | One deliberate composition |
| **Fake macOS/app window mockup** | "Look, a real app window" prop | Show real product UI or design from what the thing actually is |
| **Gradient pill with icon + text** | Gradient + pill + icon + label = complete slop fest | Style with intent |
| **Testimonial/quote card** (giant quote mark + centered quote + avatar + fake metric) | Prefab gesture | Real type and space for emphasis |
| **Gradient-circle initials avatar** | Slop on its own, worse with blue-purple gradient | Real photos or bare marks |
| **Grid/graph-paper background** | "Blueprint" look as full-bleed default | Sparing, specific technical drawing only |
| **Crude CSS/SVG illustrations** (bar charts from divs, floating circles) | Generated placeholders, not real illustration | Real photography, product UI, or bespoke SVG craft |
| **Accent-bar card** (dark box + single bright edge line) | Lone colored bar to "add interest" | Invented geometry with intent |
| **Background glow** (radial blob bleeding from corner) | On nearly every dark hero/CTA band | Considered light, not default glow |
| **Fake code-snippet window** (traffic lights + quickstart.ts + purple/green/grey palette) | Canned dev prop | Show real code or real product |
| **Floating tag pinned to image** | Little "info chip" to make flat box look alive | Real composition |
| **Letterspaced serif wordmark** | Tracking out default serif = instant "elegance" | Real composition with generosity, case decision, color/texture |
| **High-contrast Didone serifs** (Bodoni, Didot) | Reflexive "luxury" = obvious default | Chosen on purpose, not autopilot |
| **Monospace as house voice** | Costume, not decision | Use sparingly, only for genuine data |
| **One label treatment everywhere** (tracked caps on eyebrow, button, figures, nav, colophon) | Template, not voice | Different roles = different treatments |
| **Botched glass** (pixelation, banding, leak, pop) | Bad blur worse than no blur | Flawless or don't ship glass |
| **Botched fill animations** (caps flip rounded→sharp, partial fill, stutter) | Half-built motion screams slop | Animate clip/width with stable caps, full track, smooth ease |
| **Never hide content behind entrance animation** | Content = invisible when reveal fails | **CONTENT IS VISIBLE BY DEFAULT** — animate things already on screen |
| **Content sliced by edge** (clip-path, notch, overflow:hidden, fixed height) | Reads as broken | **CLEAR THE CUT** — pad content clear of cuts, verify pixel-for-pixel |
| **Misaligned parallel columns** (ragged pricing/feature grids) | Reads as broken/unconsidered | Shared horizontal grid: titles, prices, buttons all align |
| **Text jammed against edge** | Looks like overflow accident | Generous, consistent gutters from every edge |
| **Default all-around shadow** (soft symmetric bloom on everything) | "Float everything on fluffy cloud" | Directional, tight, tinted shadow — or depth from tone/edge |
| **Content flung to far edges** (footer: tagline far left, links far right) | Imbalance reads as unplaced | Symmetry, alignment, shared margins |
| **Missing/faked logos** | Thin/unfinished OR worse: invented | Real marks honestly/sparingly, or none at all |
| **Nothing actually centered** (off by pixels in circles, badges, pills) | Reads as broken | **Center what you meant to center, actually — verify, don't eyeball** |
| **Faking shadow with second box** | Hard-edged grey slab peeking out | Real tight shadow or none |
| **Icon/logo with box behind it** | Component-kit default | Bare mark on surface, separation from weight/color/spacing |
| **Little rule beside label** (eyebrow tick) | Decorative tic, not design | Presence through type/weight/color/spacing |
| **Oversized footer wordmark done as slop** (not centered, clipped, clashing gradient, default face) | Text dropped to satisfy rule | **Signature is a composition** — generous spacing, deliberate case, room, color that belongs to brand |
| **Colliding colors / hard seams between sections** | Fighting hues + hard lines at boundaries | Single disciplined palette, seamless transitions |
| **Botched shadow — hard-edged box behind it** | Visible rounded box silhouette | Seamless fall-off, tight offset, blur carries out |
| **Text you cannot read** (no contrast) | Most basic failure | Real value gap; push contrast further |
| **Bloom = element's shape blurred** | Sticker with halo, not lit object | Directional cast shadow |
| **Dot under active nav item** | Decoration standing in for real active state | Weight/color shift on current link |
| **Content clipped at section overlap** | Upper layer guillotines content below | Keep content on visible layer, clear past seam |
| **Cramped display type** (negative tracking, crushed separators) | Reads as squeezed | Big type needs air: loosen tracking, give separators space |
| **Grain on top of content** | Fights legibility | Grain on substrate only; text stays crisp |
| **Underline-fill hover animations** | Reflexive "look it's interactive" flourish | Clean state change: tonal shift, icon slide |
| **Sun-moon theme toggle / redrawn line icons** | Stock switch + generic glyphs redrawn | Bespoke iconography with real point of view |
| **Unrounded hairline rules as decoration** | Cheap, lazy structure faking | Round caps, invented shape, or real spacing/hierarchy |

---

## Deeper Tells: Dodging the List Is Still Slop

| Tell | Why It Fails |
|------|--------------|
| **Even the "tasteful" font swap** (Big Shoulders, Newsreader, IBM Plex Mono...) | Picking by reputation instead of brief |
| **Same skeleton, recolored** | Template with different paint |
| **The standard footer** (wordmark + tagline + rule + 4 columns + rule + copyright) | "Correct" footer with no idea = slop |
| **No icons at all** | Over-correction = flat, lifeless = just as lazy |
| **Avoiding the list ≠ design** | Checklist produces clean miss, not design. Design = point of view applied with conviction |

---

## What Premium Actually Looks Like (Craft, Not Avoidance)

### Markers of Premium

| Element | Slop Version | Premium Version |
|---------|--------------|-----------------|
| **Translucency** | Frosted box with blue glow ignoring backdrop | **Real liquid glass:** sits over backdrop worth showing, refracts/bends it, chromatic dispersion at edges, bright inner highlight top lip, light frost, tuned inner+drop shadows, reacts to backdrop |
| **Borders** | Hard contrasting 1px line on every box | **Self-colored borders + tonal elevation:** surface value shifted from background, 1px stroke = surface's own color at low opacity, soft inner highlight top edge = rounded lip catching light |
| **Geometry** | Plain straight accent bar | **Bespoke silhouette:** invented shape (diagonal cut-in, chamfer, notch, custom bracket) — reads as drawn on purpose |
| **Icons** | Icon in tile/chip/colored square | **Bare marks only** — strip to the mark itself |
| **Copy** | Walls of text, many stacked lines | **Say less** — terse, hierarchy/spacing/visuals carry meaning |
| **Iconography** | Pulled from pack | **Custom in-house set** — consistent stroke/corner/grid, designed objects |
| **Micro-interactions** | Default fade-and-translate | **Authored motion:** line travels/fills with popped cap, tuned easing, tight intentional shadows |
| **Light/Glow** | Reflexive blue-purple bloom | **Considered light:** specific, unexpected color (warm volumetric amber, single directional ray) |
| **Noise** | None or blanket sheet over everything | **Premium noise:** fine film grain/perlin at very low opacity — breaks flat fills, removes banding, adds tactile quality — feel it, don't see it |
| **Type** | Free Google defaults | **Licensed/self-hosted distinctive faces** (Perfectly Nineties, Matter, Soehne, GT America, Tiempos, Klim) + neutral workhorse + mono |
| **Composition** | Stacks of default sections | **Full-page, large-scale:** oversized headlines, enormous wordmark bleeding off edge, generous negative space, type/shapes sized past timid default |
| **Social proof** | Missing or fake logos | **Real logo walls** — recognizable brands, monochrome, even sizing, quiet |
| **Backgrounds** | Flat color or default grid | **Blueprint/canvas:** fine module grid, ruler ticks, corner crop marks, dashed guides — subtle, monochrome, evokes craft |
| **Inset sections** | Full-bleed bands welded to page | **Floating islands:** rounded panel with consistent margin ALL sides, on different surface — reads as detached, deliberate object |
| **SVG renders** | Crude CSS illustrations | **Crafted custom SVG** — correct proportions, layered detail, considered color/light |
| **Glass** | Blur + shadow fails | **Keep the gloss** (clean specular sheen = premium part), fix blur/leak/halo/pop |
| **Professional** | Lifeless, zero invention | **Clean + heartbeat:** authored creative moments (aligned hovers, drifting logo boxes, oversized footer typography with texture, scroll-driven reveal, kinetic detail) |
| **Grid** | Lazy full-page graph paper | **Good grid:** precise, small, intentional module grid + texture (grain, noise gradient, considered edge) — looks like printed substrate |
| **Gradients** | Smooth banded stripes | **Grainy gradients:** fine grain/noise dithered in — seamless, physical surface |
| **Motion** | None or default | **Scroll-authored:** content reveals/settles/shifts on viewport entry, quiet parallax — subtle, fast, tied to scroll, prefers-reduced-motion gated |

---

## The Signature: How Uniqueness Is Actually Made

```
uniqueness = one signature artifact + atmosphere + layered depth + character display face + one bespoke silhouette + treated nav + real specifics
```

### 1. One Signature Artifact
Every memorable hero has ONE custom, high-effort focal object that could not be pasted elsewhere.
- Craft: torn-paper collage sky
- Portal: painted dusk landscape with tiny robot
- Podqi: flowing green silk render
- Droppable: starfield with bold green wordmark
- Paper: layered design-tool canvas with terminal
**Decide this FIRST; everything else supports it.**

### 2. Atmosphere, Not Flat Fill
Background = composed environment with depth/mood (illustration, render, texture, scene). Not one flat color.

### 3. Layered Depth on Z-Axis
Three reads: foreground copy, midground focal object (product window, character), background scene. At least one element crosses a layer boundary.

### 4. Product as Real Populated Artifact
When product shown: detailed, fully-populated UI floated with depth, usually clipped at bottom edge. Empty placeholder boxes = boring.

### 5. Character in Display Type
Headline face has personality, set large: distinctive serif or characterful grotesque. Identity never rests on neutral grotesque.

### 6. One Bespoke Silhouette
Single custom-cut shape signs the page: receipt-shaped pricing card with torn zigzag, contained pill nav, notch.

### 7. Nav Is Treated, Not Defaulted
Menu bar = decision: float in contained pill, center it, make it big, thread real brand marks into it.

### 8. Real Specificity
Real logos in wall, real names/data inside product, real copy. Specifics read as true; placeholders read as stock template.

---

## A Kit of Specific Premium Moves

> **Disclaimer:** These are tools for the right context, never a checklist to run top-to-bottom. Two equal failures: using everything (makes noise), using nothing when a move is genuinely required. **Cohesion:** never use an element that doesn't complement the others. Every choice must belong to one system.

### The Signature Serif Headline
Elegant, slightly high-contrast serif with real character, set very large, often ONE word in italic and/or single accent color. Beats any grotesque when unsure.

### Two-Tone / Accent Headline
Inside headline, set one word/line apart: italic or single accent color (violet, indigo, brand hue), rest neutral. One emphasis per headline.

### Full-Bleed Atmospheric Hero
Single photographic/rendered/painted scene filling ENTIRE hero edge-to-edge (nature, sky, horizon, soft 3D world), headline centered over it, nav floating on top. Background IS the art.

### Animated Character-Field Background
Scattered monospace glyphs (digits, punctuation, symbols, ASCII) drifting over soft iridescent gradient, faintly animated twinkle/drift loop. Data/code atmosphere without literal illustration. Low-contrast, behind content, reduced-motion gated.

### Gradient-Filled Icons (Jewel Inside Mark)
Icon/logo whose FILL is multi-stop gradient (lightning bolt, bloom, shaped gradient interior), not flat monochrome. Rare, distinctive, like small enamel jewel. Use on brand mark or single eyebrow icon, sparingly.

### The Arrow Is a Tell, So Sweat It
Default horizontal right arrow = stock component. Upward/outward diagonal arrow (up-right) = small distinctive premium choice. Draw specific arrow matching stroke/corners to system.

### One Cohesive Visual Language ("Synchronized Edition")
Strongest pages feel like one system: nav, buttons, arrows, corner radius, borders, background all speak same language. Sharp corners everywhere, or one specific arrow reused, or one gradient threaded through icon/button/background. Nav must belong to system.

### Premium Glass CTA (When It Earns It)
Glossy, softly-blurred glass button over rich background, executed cleanly (gloss highlight, blur blends, no leak, no pop). Only works over atmospheric background worth refracting.

### Use Real Component Libraries, Don't Hand-Roll Generic UI
Pull proper UI libraries (shadcn/ui, tailark, motion-primitives, kokonut UI) instead of hand-building buttons/toggles/navs/cards. Reinventing basics reproduces slop defaults. Take accessible primitives and art-direct hard on top.

**De-slop the prebuilt pieces ALWAYS:** Free block = head start, not free pass. Libraries still ship slop defaults (blue-purple gradients, glowy pills, fill+outline pair, sun-moon toggles, tracked caps, default hero stack). Spot slop → replace/delete/rewrite. Take accessible behavior + structure; throw away generic styling.

---

## Field Notes: What Actually Landed

### Cohesion Is the Whole Game
Loudest failure = INCOHERENCE: individually-fine parts that don't belong to each other.
**Fix that landed every time:**
- One palette, held with discipline (monochrome/tightly-related beats mix)
- One type voice (never two display faces that argue; single family across weights/sizes, or one display + one quiet neutral)
- One signature artifact decided FIRST, whole page built around it
- Decide the world, then compose sections from it

### "Creative" ≠ "Realistic"
When brief asks creative/maximal: literal stock realism (photoreal lake) reads as OPPOSITE of creative.
**Reach for authored artistic treatment in ONE consistent medium:** cyanotype prints, single illustration style, pixel art, riso look, bright painted sky. Limited-palette medium auto-coheres.

### Type Without the Google Slop Shelf
**Fontshare** (General Sans, Clash Display, Cabinet Grotesk, Satoshi, Switzer, Pally, Gambarino, Sentient, Tanker; Velvetyne faces) = free, licensed-quality, NOT Google default rotation. Download woff2, self-host via `next/font/local`.

### Product-as-Artifact Is a Signature, Not the Slop Window
Faux app window = slop tell ONLY when empty/generic. Detailed, fully-populated, real-feeling product UI (actual editor, real diffs, real copy, working controls), floated with depth, clipped at edge = strongest signature. Build as real interactive UI, not picture. ONLY show product UI when there IS one.

### Take Design LANGUAGE From References, Never Content
Given example sites for "vibe": lift language (palette mood, type energy, motion, hero/footer kind) then design ORIGINAL copy/layout/artifact for THIS product. Reproducing reference's headline/product window verbatim = copying.

### "Distinctive Font" Keeps Moving
Clash Display / General Sans (Fontshare) now read as default startup look too. Reach further for character. Pair signature display with TRUE neutral body (system-ui = genuinely neutral and safe).

### Dead-Looking Is a Fail on Its Own
"Boring/static/menu has no animation" = real rejection even when nothing is slop.
**Put authored, purposeful motion:** nav that enters/responds, signature that drifts/floats, scroll-linked parallax, crafted hovers. Calm allowed; dead not.

---

## Reference Implementation: Liquid-Glass Button (Concrete Recipe)

### Shared Base
- **Fill:** `#2575FF`
  - Thick variant: 50% opacity (background reads through)
  - Thin variant: solid
- **Label + icon:** `#FFFFFF` at 100%
- **Type:** Geist Medium, 20
- **Icon-to-label gap:** 8
- **Padding:** 20 horizontal, 14 vertical
- **Two hairline strokes** at 20% opacity, near-surface colors:
  - Cyan tint `#22BBFD`
  - White `#FFFFFF`
  - These are self-colored edges, not contrasting outline
- **Inner shadow (top highlight):** `#FFFFFF`, 20% opacity, offset Y 1, blur 32
- **Drop shadow:** Tinted to FILL `#2575FF` (not black), 6% opacity, offset Y 3, blur 3

### Glass Material Parameters
| Parameter | Thin Pill | Thick Pill |
|-----------|-----------|------------|
| Light angle | -45deg | -50deg |
| Light intensity | 80% | 60% |
| Refraction | 80 | 64 |
| Depth | 2 | 44 |
| Dispersion | 40 | 67 |
| Frost | 6 | 2 |
| Splay | 0 | 20 |

### CSS Approximation (No Native Refraction/Dispersion)
```css
/* Base */
backdrop-filter: blur(6px) saturate(120%) contrast(110%); /* Frost + lensing */
box-shadow:
  inset 0 1px 32px rgba(255,255,255,0.2),  /* Top highlight */
  0 3px 3px rgba(37,117,255,0.06),         /* Color-matched drop shadow */
  0 0 0 1px rgba(34,187,253,0.2),          /* Cyan stroke */
  0 0 0 1px rgba(255,255,255,0.2);         /* White stroke */

/* Fake dispersion: 1px cyan/magenta offset on edge or thin conic/edge gradient */
```

**Always place over real content so there's something to refract.** SVG filters with `feDisplacementMap` can do true refraction if worth the cost.

---

## Quick Reference: The "Slop or Not?" Decision Tree

```
Is this element a default preset from a component library or AI suggestion?
├── YES → Does it serve a deliberate, brand-specific purpose?
│   ├── NO → REPLACE OR REMOVE (it's slop)
│   └── YES → Has it been art-directed for this brand (colors, motion, geometry, type)?
│       ├── NO → ART-DIRECT IT (de-slop the prebuilt piece)
│       └── YES → Verify it coheres with the rest of the system
└── NO (custom) → Does it complement the other choices?
    ├── NO → RECONSIDER (incoherence = slop)
    └── YES → Verify craft execution (centering, contrast, animation quality, etc.)
```

---

## Final Reminder

> **A checklist produces a clean miss, not a design.** Design is a point of view (an idea about who this is for and why it should look like this), applied with conviction. This file can only make work less wrong. It cannot make it good. **Decide the signature, then actually build something around it.**

Clean is the FLOOR, never the achievement. Calm is a deliberate style and can be gorgeous; empty is a miss. Professional with a heartbeat, not professional and asleep.