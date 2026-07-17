# Domain-Specific UI/UX Patterns — Deep Reference

This is the deep reference for design patterns and considerations specific to different product domains. Read this when working on a project in a particular domain — ecommerce, SaaS, enterprise, healthcare, fintech, content, social, or data-heavy products.

---

## 1. Ecommerce

### 1.1 Key UX Goals
- Minimize friction from discovery to purchase
- Build trust (security, returns, social proof)
- Reduce cart abandonment (average: 70%)
- Support product discovery (search, browse, filter)

### 1.2 Critical Patterns

**Product discovery**:
- Search with autocomplete, typo tolerance, faceted filtering
- Category navigation with clear hierarchy and mega-menus
- "Shop the look" / "Complete the set" cross-sell
- Personalized recommendations (based on browsing, purchase history)

**Product detail page (PDP)**:
- Multiple high-quality images with zoom and 360° view
- Clear CTAs: "Add to Cart", "Buy Now", "Add to Wishlist"
- Social proof: Reviews, ratings, "X people bought this recently"
- Scarcity: "Only 3 left", "X people are viewing this"
- Size/fit guides, variant selector (color, size, material)
- Trust signals: Free shipping, returns policy, secure checkout badges
- Accordion sections: Description → Specs → Reviews → FAQ

**Cart & Checkout**:
- Persistent cart (across devices if logged in)
- Mini cart preview (dropdown or slide-out)
- Progress indicator: Cart → Shipping → Payment → Review → Confirmation
- Guest checkout (don't force account creation)
- Auto-detect shipping address, save user input
- Multiple payment options (credit card, PayPal, Apple Pay, Google Pay, BNPL)
- Order summary with shipping costs and taxes clearly itemized
- "Buy with" contextual payment options (Shop Pay, PayPal)

**Post-purchase**:
- Clear order confirmation with tracking number
- Easy returns process (print label, drop off)
- Reorder from order history
- "You might also like" cross-sell with order confirmation

### 1.3 Ecommerce-Specific Heuristics

- [ ] Can users find products in ≤ 3 clicks from homepage?
- [ ] Are shipping costs shown before checkout (not at payment)?
- [ ] Is the checkout form saved if the user navigates away?
- [ ] Are return policy and terms accessible from every page?
- [ ] Is the mobile checkout as easy as desktop?
- [ ] Are product images zoomable on mobile?
- [ ] Can users compare products?
- [ ] Is the "Add to Cart" button always visible during product scroll?

---

## 2. SaaS / Dashboard / B2B

### 2.1 Key UX Goals
- Reduce time to value (faster onboarding)
- Enable task completion efficiently (power users)
- Provide clear data visibility (at-a-glance understanding)
- Support complex workflows without overwhelming users
- Minimize training and support burden

### 2.2 Critical Patterns

**Onboarding**:
- Progressive onboarding (show features as user needs them)
- Interactive product tours (step-by-step, dismissible)
- Template-based setup (fill in the blanks, don't configure everything)
- Sample data to explore before committing actual data

**Dashboard design**:
- Prioritize key metrics (what decision does the dashboard support?)
- Progressive disclosure: key metrics first → details on click
- Card-based layout for modular data widgets
- Time range selector (last 7d, 30d, 90d, custom)
- Data export (CSV, PDF, shareable link)
- Customizable layouts (drag-and-rearrange cards, save views)

**Data tables**:
- Sortable columns (single and multi-column sort)
- Search, filter, and column visibility controls
- Sticky header row + first column for scrolling
- Inline editing (editable cells)
- Bulk actions (select, delete, export)
- Pagination (20-50 rows per page) or infinite scroll for browse

**Forms & data entry**:
- Smart defaults and auto-save
- Guided setup wizards for complex configuration
- Batch operations for repetitive data entry
- Input validation (inline, on blur, debounced)

**Navigation**:
- Sidebar nav (primary) + top bar (secondary actions)
- Breadcrumbs for deep hierarchies
- Workspace/project switcher
- Global search (search everything: docs, settings, data)

### 2.3 SaaS-Specific Heuristics

- [ ] Can a new user accomplish their first meaningful task within 5 minutes?
- [ ] Are there keyboard shortcuts for frequent actions?
- [ ] Is data export available (CSV, API, etc.)?
- [ ] Can actions be undone or recovered?
- [ ] Are error messages helpful, not just "An error occurred"?
- [ ] Is there inline help / tooltips / documentation links?
- [ ] Are there bulk operations for repetitive tasks?
- [ ] Is the interface fast (under 1s for most interactions)?

---

## 3. Fintech / Financial Services

### 3.1 Key UX Goals
- Build trust above all else (security, transparency)
- Make complex financial concepts understandable
- Reduce anxiety around money decisions
- Ensure error prevention (money is high-stakes)
- Comply with regulations while maintaining usability

### 3.2 Critical Patterns

**Onboarding & KYC**:
- Clear explanation of why information is needed
- Step-by-step identity verification with progress
- Document upload with clear guidance (what kind of photo, lighting, etc.)
- Real-time verification feedback
- Secure data handling messaging

**Account overview**:
- Balance prominently displayed (most important number)
- Transaction list with search, filter, and categorization
- Spending insights (visualized: categories as donut chart, trend as line chart)
- Account switching (checking, savings, credit, investment)

**Transactions**:
- Consistent format: date, description, amount (with +/-), category
- Search transactions (by date, amount, vendor, category)
- Transaction detail view with receipt attachment option
- Pending vs posted status clearly indicated

**Payments & transfers**:
- Confirmation step with all details visible before submitting
- Error prevention: validation of account numbers, amounts, dates
- Scheduled/recurring payment setup with clear calendar
- Receipt generation and email confirmation

**Security patterns**:
- Multi-factor authentication (with recovery codes)
- Biometric login (fingerprint, face ID)
- Device management (see and revoke logged-in devices)
- Fraud alerts with clear action steps
- Session timeout with auto-save

### 3.3 Fintech-Specific Heuristics

- [ ] Are all security measures explained in plain language?
- [ ] Is error recovery clear and easy (cancel transaction, dispute charge)?
- [ ] Are fees, rates, and timelines transparently shown?
- [ ] Is the most important information (balance, due date) immediately visible?
- [ ] Are confirmation steps present for all money-moving actions?
- [ ] Is account/transaction data exportable?
- [ ] Are notifications clear and actionable (not just alerts)?
- [ ] Is the accessibility of financial information ensured for screen readers?

---

## 4. Healthcare

### 4.1 Key UX Goals
- Prioritize patient safety above all
- Make complex medical information understandable
- Reduce anxiety and stress for patients
- Support clinical workflows efficiently
- Comply with HIPAA/regulatory requirements

### 4.2 Critical Patterns

**Patient portal**:
- Secure login with MFA
- Appointment scheduling with real-time availability
- Test results with clear explanations (not just numbers)
- Secure messaging with response time expectations
- Medication list with refill requests
- Health record access (download/print)

**Provider workflows**:
- Clean, distraction-free interface for clinical context
- EHR data entry optimized for speed (templates, shortcuts, voice input)
- Alert fatigue management (prioritize important alerts)
- Interoperability (see patient data from other providers)
- Evidence-based guidelines integrated into workflow

**Telehealth**:
- Pre-visit checklist (connection test, privacy, consent)
- Waiting room experience (clear when provider will join)
- Clear audio/video indicators (mute status, connection quality)
- Screen sharing for test results or visual aids
- Post-visit summary auto-generated

### 4.3 Healthcare-Specific Heuristics

- [ ] Is patient data protected at every step (HIPAA compliance)?
- [ ] Are medical terms explained in plain language for patients?
- [ ] Is urgent information clearly distinguishable from routine?
- [ ] Can patients easily find their specific test results?
- [ ] Are appointment reminders configurable (time, channel)?
- [ ] Is there a clear emergency contact path?
- [ ] Are accessibility features built in (screen reader, large text, high contrast)?

---

## 5. Content-Heavy / Media / Publishing

### 5.1 Key UX Goals
- Maximize content discoverability
- Optimize for reading comprehension and comfort
- Support content exploration and serendipity
- Build habit-forming consumption patterns
- Balance content density with readability

### 5.2 Critical Patterns

**Article/content page**:
- Clear typography hierarchy and optimal reading measure (50-75 chars)
- Progress indicator (reading position in the article)
- Estimated reading time
- Related content at the end
- Save/bookmark for later reading
- Share functionality (social, link, embed)

**Content discovery**:
- Personalized recommendations (based on reading history, preferences)
- Editorial curation (hand-picked collections)
- Trending/popular sections
- Topic/subject taxonomy with browse by topic
- Continuous scroll (feed-based) for social content

**Search & navigation**:
- Global search with content type filter
- Advanced search (date range, author, topic)
- Category/subject navigation with clear hierarchy
- Tags and related content linking

### 5.3 Content-Specific Heuristics

- [ ] Is the reading experience comfortable (font, size, line height, contrast)?
- [ ] Is the content discoverable through search and navigation?
- [ ] Are loading times acceptable (especially for large media)?
- [ ] Is the content responsive (works on all screen sizes)?
- [ ] Can users save/bookmark for later reading?
- [ ] Are related/suggested articles contextually relevant?
- [ ] Is the content accessible (screen reader, keyboard navigation)?

---

## 6. Social / Community

### 6.1 Key UX Goals
- Maximize engagement and daily active usage
- Support content creation (ease of publishing)
- Foster meaningful connections and interactions
- Balance algorithmic vs chronological content
- Moderate content effectively (safety)

### 6.2 Critical Patterns

**Feed/stream**:
- Algorithmic or chronological sorting with clear controls
- Infinite scroll with periodic content refresh
- Rich media cards (text, image, video, poll, link)
- Interaction bar (like, comment, share, save)
- "Why you're seeing this" transparency (for algorithmic feeds)

**Content creation**:
- Prominent, low-friction create button (post, photo, video, story)
- Rich editor with media upload, emoji, tagging
- Draft saving (lose nothing if interrupted)
- Audience selector (public, friends, private)
- Schedule/post timing controls

**Profile & identity**:
- Avatar, cover, bio, links
- Activity history (posts, likes, comments)
- Privacy settings per content type
- Follow/subscriber counts and management
- Account settings and notification preferences

### 6.3 Social-Specific Heuristics

- [ ] Is content creation frictionless (≤ 3 taps/clicks)?
- [ ] Are privacy controls clear and accessible?
- [ ] Can users easily mute, block, or report?
- [ ] Is the content moderation system transparent?
- [ ] Are notifications manageable (not overwhelming)?
- [ ] Is the feed scannable (clear hierarchy, visual breaks)?
- [ ] Can users control what they see (algorithm settings)?

---

## 7. Enterprise / Internal Tools

### 7.1 Key UX Goals
- Maximize efficiency for repetitive tasks
- Reduce training time and support burden
- Support complex workflows with many steps
- Handle large data volumes gracefully
- Integrate with other enterprise systems

### 7.2 Critical Patterns

**Efficiency features**:
- Keyboard shortcuts for all frequent actions
- Batch operations (select multiple, apply action)
- Saved searches, filters, and views
- Bulk import/export (CSV, Excel, API)
- Macros, templates, and presets

**Data handling**:
- Virtual scrolling for large datasets (render only visible rows)
- Client-side filtering, sorting, and search
- Export to multiple formats (CSV, PDF, Excel)
- Data import with validation and error preview
- Audit logging (who did what and when)

**Navigation & structure**:
- Sidebar or top nav with clearly labeled sections
- Workspace/project/task hierarchy
- Breadcrumbs for deep navigation
- Tabbed views within a section
- "Recent items" or "Continue where you left off"

### 7.3 Enterprise-Specific Heuristics

- [ ] Can power users accomplish tasks with keyboard alone?
- [ ] Are bulk operations available for repetitive tasks?
- [ ] Is data import/export accessible and well-documented?
- [ ] Are there saved views/presets for common workflows?
- [ ] Is the performance acceptable with real data volumes?
- [ ] Are integrations with existing tools working smoothly?
- [ ] Is training/support documentation easily accessible?

---

## 8. Data-Heavy / Analytics

### 8.1 Key UX Goals
- Make data understandable at a glance
- Support exploration and discovery of insights
- Allow customization for different user roles
- Handle large datasets without performance degradation
- Provide confidence in data accuracy

### 8.2 Critical Patterns

**Data visualization**:
- Choose chart type by data relationship (comparison: bar, trend: line, composition: pie/donut/stacked, distribution: histogram/scatter)
- Interactive charts (hover for details, click to drill down, brush to select range)
- Consistent color mapping across visualizations
- Annotations and reference lines (targets, averages, benchmarks)
- Export chart as image or embeddable link

**Filtering & exploration**:
- Global date range selector (affects all widgets on the page)
- Cross-filtering (clicking one chart filters all other charts)
- Dimension/measure picker (change what's shown without rebuilding)
- Save/shared filters and views
- Drill-down path from summary → detail

**Dashboard composition**:
- Modular widget system with drag-and-drop
- User-configurable layouts and saved dashboards
- Scheduled report delivery (email, Slack)
- Collaborative annotations and discussions on data points

### 8.3 Data-Heavy Heuristics

- [ ] Is the most important metric immediately visible?
- [ ] Can users drill down from summary to detail?
- [ ] Are chart types chosen appropriately for the data?
- [ ] Is data export available at every level?
- [ ] Are filters and date ranges persistent across navigation?
- [ ] Is performance acceptable with real data volumes?
- [ ] Are visualizations accessible (screen reader, color-blind friendly)?

---

## When to Read This File

Read `domains.md` when:
- Designing for a specific industry or type of product
- Understanding domain-specific user expectations
- Auditing a design against domain-specific best practices
- Transitioning between domains and needing to learn patterns quickly
- Planning research in an unfamiliar domain

**Document reference**: Domain-specific patterns and considerations for ecommerce, SaaS, fintech, healthcare, content, social, enterprise, and data-heavy products
**Last updated**: July 2026
