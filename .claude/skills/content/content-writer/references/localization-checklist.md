# Localization Checklist

## 1. Core Principles

Localization goes beyond translation. It's adapting content so it feels native in every market. A translated piece preserves meaning. A localized piece preserves intent, tone, and cultural resonance.

### The localization spectrum
| Approach | What it does | When to use |
|---|---|---|
| **Translation** | Word-for-word language conversion | Legal, technical specs, compliance |
| **Localization** | Adapts tone, references, format, examples | Marketing, content, brand communication |
| **Transcreation** | Rewrites from scratch with same intent | Slogans, taglines, campaigns, humor |
| **Globalization** | Builds content to work everywhere from day one | Product copy, UX, technical docs |

---

## 2. Pre-Localization: Writing Source Content That Travels Well

Write source content with localization in mind. This saves 50%+ of downstream cost.

### Do
- Use simple, clear sentences. Short main clauses.
- Use active voice (easier to translate than passive).
- Define acronyms on first use.
- Use standard date/time/number formats (ISO 8601 dates: 2026-07-09).
- Keep compound modifiers clear (use a hyphen or rephrase).
- Use descriptive link text visible out of context.
- Keep sentence structure parallel in lists.
- Use "you" and "we" consistently.

### Avoid
- Idioms and culturally specific metaphors.
- Humor that relies on wordplay or cultural knowledge.
- Sports, political, or religious references.
- Regional examples (replace "like the Super Bowl" with "like a major championship").
- Phrasal verbs with multiple meanings ("pick up," "set up," "break down").
- Long noun stacks ("end-user data privacy compliance certification process").
- Ambiguous pronoun references ("it," "this" without clear antecedents).

---

## 3. Locale-Specific Formatting

### Dates
| Locale | Format | Example |
|---|---|---|
| US | Month Day, Year | July 9, 2026 |
| UK/EU | Day Month Year | 9 July 2026 |
| ISO | YYYY-MM-DD | 2026-07-09 |
| Japan | YYYY年M月D日 | 2026年7月9日 |

### Numbers
| Locale | Decimal | Thousand | Example |
|---|---|---|---|
| US/UK | . | , | 1,234.56 |
| EU/SA | , | . or space | 1.234,56 or 1 234,56 |
| Switzerland | . | ' | 1'234.56 |

### Currencies
- Use locale-appropriate symbol placement: $1,234 (US), 1.234$ (some EU), 1,234円 (Japan).
- Include the ISO code (USD, EUR, JPY) in financial or B2B content.
- Don't assume US dollars as default for global content.

### Units of measurement
- Provide metric equivalents for imperial measurements.
- For technical docs, include both systems where the audience is global.
- Temperature: °C for most of the world, add °F for US audiences.

### Addresses
- Don't assume postal code format, state/province system, or address ordering.
- Use multi-field address forms that adapt by locale.

---

## 4. Linguistic Considerations

### Text expansion/contraction
- English source text typically expands 20-35% when translated into Spanish, French, or German.
- Contracts 10-15% in Japanese, Korean, or Chinese.
- Design UI and layouts with 35% expansion buffer for text containers.
- Short headlines are hardest to localize: keep them tight but not cryptic.

### Right-to-left (RTL) languages
- Arabic, Hebrew, Urdu, Persian, and others read right-to-left.
- All UI elements (buttons, menus, progress bars) should flip, not just text.
- Some punctuation remains left-to-right within RTL text (numbers, URLs).
- Alignment of headings, text blocks, and icons must reverse.
- Test for overlapping text, broken layout, and misaligned CTA buttons.

### Character encoding
- Use UTF-8 encoding. Always. No exceptions.
- Don't use all-caps for emphasis in scripts where capital letters don't exist (CJK, Arabic).
- Font selection must support the target script (CJK fonts are 10x+ larger in file size).

### Plurals & gender
- English has 2 plural forms (singular/plural). Arabic has 6. Polish has 3.
- Don't code for English-only plural rules. Use ICU MessageFormat for UI strings.
- Avoid gendered language in source content. Many languages assign gender to objects.
- In gendered languages, consider gender-neutral phrasing or using the masculine as generic (check local norms).

---

## 5. Cultural Adaptation Checklist

- [ ] Colors: red = warning in US, good luck in China, mourning in South Africa.
- [ ] Icons and symbols: thumbs-up is positive in the West, offensive in parts of the Middle East.
- [ ] Hand gestures, body parts, and animal imagery: meanings vary dramatically.
- [ ] Religious and holiday references: don't assume Christmas, weekends, or workweeks are universal.
- [ ] Political boundaries: maps, country names, and disputed territories require careful handling.
- [ ] Humor: rarely translates. Puns, irony, and sarcasm are high-risk.
- [ ] Social norms: formality levels (tu/usted/du/Sie), first-name vs title usage.
- [ ] Power dynamics: direct vs indirect communication styles (high-context vs low-context cultures).
- [ ] Example scenarios: a family dinner, a commute, a holiday look different in every culture.

---

## 6. Transcreation: When Translation Isn't Enough

Transcreation is needed when the *effect* matters more than the literal words.

### When to transcreate
- Taglines and brand slogans
- Campaign headlines and hooks
- Product names with unintended meanings
- Humor, wordplay, and cultural references
- Emotional or aspirational copy
- Calls to action

### Transcreation process
1. Brief the local expert on the brand voice, target emotion, and constraints.
2. Let them write from scratch, not translate.
3. Evaluate: does it evoke the same feeling and action as the original?
4. Legal review if it's a regulated claim or trademark.

---

## 7. Localization QA Process

### Linguistic QA
- [ ] No truncation or overlapping text in UI.
- [ ] All strings are translated (nothing left in source language).
- [ ] Terminology is consistent across the product/docs/marketing.
- [ ] Tone matches brand voice in the target language (formal vs casual).
- [ ] Variables and placeholders (%s, {0}) are preserved in correct order.
- [ ] Cultural references are adapted, not translated.
- [ ] Numbers, dates, currencies, and units follow local conventions.
- [ ] Links point to localized pages, not source-language pages.

### Functional QA
- [ ] All text fits in UI containers (no overflow, no truncation).
- [ ] RTL layout renders correctly (mirrored, not forced LTR).
- [ ] Font rendering supports target script (CJK, Arabic, Devanagari, etc.).
- [ ] Input methods work (IME for CJK, RTL keyboard for Arabic/Hebrew).
- [ ] Voiceover/screen reader reads correctly in target language.
- [ ] Sorting, search, and filters handle target characters correctly.

### Cultural QA
- [ ] Images and icons are culturally appropriate.
- [ ] Color meanings are checked per market.
- [ ] No unintended meanings in product names or copy.
- [ ] Legal disclaimers are adapted per local regulations.
- [ ] Examples and case studies are relevant or adapted.

---

## 8. SEO in Localization

- Don't machine-translate keywords. Research what people actually search in each locale.
- The same keyword may have different search volume, intent, or competitors in different languages.
- Hreflang tags: use language + region, not just language (e.g., "en-US" vs "en-GB").
- Translated slugs (URLs) help in local search.
- Local backlinks matter more than global domain authority in some markets.
- Some markets prefer different content structures (e.g., Japanese pages often have more visual density).

---

## 9. Common Localization Pitfalls

| Pitfall | Example | Fix |
|---|---|---|
| Idiom that doesn't translate | "Hit the ground running" | "Start quickly and effectively" |
| Cultural assumption | "Stock up for the holidays" (assumes Christmas) | Specify the holiday or use seasonal general |
| False friend | "Embarrassed" (English) vs "Embarazada" (Spanish = pregnant) | Research false cognates per locale |
| Format assumption | "07/09/26" could be July 9 or September 7 | Use month names or ISO format |
| Icon confusion | Mail icon = email in most places, but not universally used | Test icon comprehension per market |
| Text overflow | "Add to cart" (EN, 11 chars) → "Ajouter au panier" (FR, 17 chars, 55% longer) | Design with 35% expansion buffer |
| Missing alt text | Screenreader reads source-language alt text | Alt text must be localized too |
| Legal gaps | GDPR ≠ LGPD ≠ CCPA ≠ PIPL | Localize privacy and compliance copy per jurisdiction |
