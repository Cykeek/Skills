# Dashboard UX Writing Guide

This reference covers all UX copy touchpoints in a dashboard or web application. Read this when writing or editing product copy for dashboards, admin panels, analytics tools, or internal tools.

**The principle:** Users in a dashboard are task-oriented. They're trying to do something, find something, or understand something. Your copy should reduce friction, not add to it.

---

## 1. Core UX Writing Principles

### The 4 dashboard copy jobs
| Job | What the user needs | Copy response |
|---|---|---|
| **Orient** | "Where am I and what can I do here?" | Clear headings, navigation labels, page titles |
| **Act** | "What should I do next?" | Action-oriented CTAs, empty state guidance |
| **Understand** | "What does this data mean?" | Contextual microcopy, tooltips, labels |
| **Recover** | "Something went wrong. Now what?" | Error messages that explain and guide |

### General rules
- **Front-load the value**: "Your data is ready" not "The data retrieval process has completed."
- **Use the user's verbs**: Match how users talk about the action, not the internal system name.
- **Be specific**: "12 new leads" not "New activity detected."
- **Don't make the user do math**: "You saved $2,400 this month" not "Your costs decreased by 15% from an average of $16,000."
- **One idea per sentence**: Especially in tooltips and microcopy.
- **Keep tooltips under 12 words**: If you need more, move it to inline help or a documentation link.

---

## 2. Page Title & Heading Copy

### Pattern
```
[Section name] | [Product name]
```

### Examples
- "Dashboard | Acme"
- "Reports | Acme"
- "Settings > API Keys | Acme"

### Guidelines
- Use sentence case for all headings (capitalize first word only).
- Match the navigation label to the page title exactly.
- Add "New" prefix for creation pages: "New Report" not "Create Report."
- For edit pages: "Edit [noun]" not "[Noun] Settings."

---

## 3. Empty States

Every empty state has a job: orient the user, explain why it's empty, and guide the next action.

### The empty state formula
```
[Icon or illustration]
[Title: what this space is for]
[Body: why it's empty + what to do about it]
[CTA: the first action to take]
```

### Empty state types

**New user, nothing yet**
> Title: "No projects yet"
> Body: "Projects are where you organize your analysis. Create your first one to get started."
> CTA: "Create your first project"

**Data cleared or reset**
> Title: "All set"
> Body: "Your data has been reset. Ready to start fresh?"
> CTA: "Import data"

**Feature not yet configured**
> Title: "Integrations need setup"
> Body: "Connect your tools to pull data into your dashboard."
> CTA: "Set up integration"

**No results for a filter/search**
> Title: "No matches found"
> Body: "Try adjusting your filters or search terms."
> CTA: "Clear all filters"

**Data not available yet (e.g., first day)**
> Title: "Data is on its way"
> Body: "Your dashboard will populate as data comes in. Check back soon."
> CTA: "Learn what to expect"

### Empty state don'ts
- ❌ "Nothing here yet" without saying what "here" is.
- ❌ Generic illustrations that don't relate to the feature.
- ❌ No CTA: the user has to guess what to do.
- ❌ Blaming the user: "No data found" (feels like it's their fault).
- ❌ Over-explaining: keep it to 2-3 sentences max.

---

## 4. Tooltips & Hover Copy

### When to use a tooltip
- The label needs clarification.
- The metric needs definition.
- The user needs to know the data source or calculation.
- The action has a non-obvious consequence.

### When NOT to use a tooltip
- The label is self-explanatory ("Delete," "Save," "Email").
- The information belongs in a documentation page (too long for a tooltip).
- The tooltip would block critical UI.
- The information never changes: put it on the page.

### Tooltip patterns
| Situation | Pattern | Example |
|---|---|---|
| Metric definition | "[Metric] = [explanation]" | "LTV = Customer lifetime value in dollars." |
| Data source | "Data from [source]" | "Data from Stripe, updated hourly." |
| Action warning | "[Action] → [result]" | "Delete → removes item permanently." |
| State explanation | "Why [state]?" | "Offline: syncing with server." |

### Tooltip don'ts
- ❌ Repeating what's already visible in the label.
- ❌ Walls of text in a tooltip.
- ❌ Using tooltips as the only way to access important information.
- ❌ Marketing language in tooltips ("Unlock the power of analytics!").

---

## 5. Form Microcopy

### Label patterns
- Labels should be short nouns or noun phrases: "Email address," not "Please enter your email address below."
- Use sentence case: "First name" not "First Name."
- Mark optional fields with "(optional)", not required fields with "*".

### Helper text patterns
| Location | Pattern | Example |
|---|---|---|
| Above field | Format hint | "Format: name@company.com" |
| Below field | Purpose/example | "Report delivered Mondays" |
| Inline error | Fix direction | "Enter valid email" |

### Placeholder patterns
- Use placeholders for examples, not instructions: "e.g., https://acme.com" not "Paste your URL here."
- Never replace labels with placeholders (accessibility failure: the label disappears when they type).
- Keep placeholders under 8 words.

### Validation messages
| State | Pattern | Example |
|---|---|---|
| Required field empty | "[Label] is required" | "Email is required" |
| Format error | "Enter a valid [format]" | "Enter a valid email address" |
| Length error | "[Label] must be at least [n] characters" | "Password must be at least 8 characters" |
| Match error | "[Label A] must match [Label B]" | "Confirm password must match password" |

---

## 6. Action Labels (Buttons & Links)

### CTA verb patterns
| Action | Verb | Stronger verb |
|---|---|---|
| Save | Save | Publish, Deploy, Submit |
| Cancel | Cancel | Dismiss, Discard, Abandon |
| Delete | Delete | Remove, Archive, Deactivate |
| Create | Create | Add, Build, Generate |
| Edit | Edit | Customize, Configure, Modify |
| View | View | Open, Preview, Inspect |
| Download | Download | Export, Generate, Extract |
| Close | Close | Dismiss, Complete, Done |

### Button copy rules
- Start with a verb: "Save changes," not "Changes."
- Be specific: "Export as CSV" not "Export."
- Match the user's mental model: "Send invitation" not "Execute invitation delivery."
- For destructive actions, repeat the object: "Delete report" not "Delete."
- Use sentence case: "Save changes" not "Save Changes."

---

## 7. Confirmation & Success Messages

### Confirmation dialogs
```
Title: [Action]?
Body: [What will happen. Be specific about consequences.]
Buttons: [Cancel] / [Confirm action]
```

Examples:
> "Delete report? This will permanently remove it for all team members. This can't be undone."

### Success messages
| Context | Pattern | Example |
|---|---|---|
| Background action | "Done" / "Complete" | "Report generated." |
| User action | "[Action] completed" | "Report saved." |
| Multi-step | "[Action] done. Next: [step]" | "Project created. Next: invite team." |
| Scheduled | "[Action] set for [time]" | "Report scheduled Monday 9 AM." |

### Success message rules
- Don't over-celebrate. "Congratulations! Your file has been uploaded!" feels patronizing for a routine task.
- Use a green checkmark for positive, not confetti.
- Auto-dismiss success messages after 3-5 seconds unless the user needs to reference the result.

---

## 8. Notification & Alert Copy

### In-app notification patterns
| Type | Pattern | Example |
|---|---|---|
| Informational | "[Event] happened" | "Report ready." |
| Positive | "[Event] completed" | "Import done: 245 added." |
| Warning | "Trouble with [X]" | "Stripe connection issue." |
| Error | "Problem with [X]" | "Save failed. Try again or contact support." |

### Alert rules
- State what happened, what it means for the user, and what to do.
- Don't use error messages for marketing. "Sorry, we had a problem!" should not precede an upsell.
- For temporary issues, add "We're looking into it" to signal awareness.
- For permanent failures, provide a next step or contact path.

---

## 9. Guide & Onboarding Copy

### Feature announcement tips
- Show the feature in context, not in a full-screen modal on first login.
- Use a tooltip pointing to the new element: "New: filter by date range."
- Provide a brief "what changed" and "why you'll care."
- Link to docs for full explanation, don't inline it.

### Empty dashboard onboarding pattern
For new users who haven't set up their dashboard:
1. "Welcome to [Product]"
2. "Here's what you can do in 3 steps:"
3. Step 1: Connect your data source
4. Step 2: Choose your metrics
5. Step 3: Invite your team
6. "Start with [step 1 CTA]"

### Product Onboarding Steps (Product Tours)
Standardize short-form copy for step-by-step product tours by focusing on action outcomes (what the user gains by doing this step) rather than just pointing at UI buttons, and use interactive button states.

- **Title:** Focus on the benefit or outcome (e.g., "Add your first host"). Avoid generic titles like "Step X" or "Onboarding Step 1."
- **Body:** Under 25 words. Focus on the action/outcome and why it matters.
- **Progress indicator:** Short and clear (e.g., "Step 1 of 3").
- **Navigation:** Primary action button starts with a value-driven verb ("Create," "Next," etc.) or "Got it" / "Finish." Secondary button (if applicable) is "Skip."

*Structure:*
```
Title: [Outcome/Benefit]
Body: [Actions to take + why they matter]
Footer: [Skip] [Next / CTA]
```

*Example Tour Steps:*
- **Step 1:**
  - *Title:* Connect your repository
  - *Body:* Link your GitHub account to import your repositories. You will be able to deploy your first project in one click.
  - *Navigation:* `[Skip]` and `[Connect Account]`
- **Step 2:**
  - *Title:* Choose a deployment template
  - *Body:* Select a framework template to build your site. Templates pre-configure your build settings automatically.
  - *Navigation:* `[Skip]` and `[Next: Configure Settings]`

### Inline guidance pattern
For complex workflows, use subtle inline guidance:
```
"Need help? [See a quick demo →]
```
Not:
```
"Let us walk you through this process in a comprehensive tutorial!"
```

---

## 10. Error Message Patterns

### Three-Part Error Recovery Messages
Standardize error messages around a recovery-centric framework:
1. **State what happened:** Acknowledge the problem immediately using plain, non-technical language.
2. **Explain why it matters:** Convey the immediate impact on the user's workload or goal.
3. **Offer a clear resolution CTA:** Provide a specific, actionable step to resolve the issue.

#### The Recovery Framework in Action

| Mapped Element | Copy Pattern | Example |
|---|---|---|
| **What happened** | "We couldn't [action or process]." | "We couldn't import your contacts." |
| **Why it matters** | "Your [related asset] will be [consequence]." | "Your marketing campaign will be paused until these contacts are loaded." |
| **Clear resolution** | "[Action verb] to resolve this." | "Check the CSV file for missing headers and upload again." |

#### Good vs. Bad Recovery Messages
- **Bad:** "Error 402: Account delinquent. Payment required." (Stops flow, cold tone, no recovery guidance).
- **Good:** "Payment failed: Your workspace is now read-only. Your campaigns are paused until billing is active. Please update your payment details to resume." (Clear impact and immediate recovery path).

### Error type reference
| Type | Pattern | Example |
|---|---|---|
| Network error | "Couldn't load [thing]. Check your connection and try again." | "Couldn't load your reports. Check your connection and try again." |
| Permission error | "You don't have permission to [action]. Contact your admin to request access." | "You don't have permission to delete this project. Contact your admin to request access." |
| Timeout error | "[Action] timed out. [Thing] might be slow right now. Try again in a few minutes." | "Your export timed out. Our system might be slow right now. Try again in a few minutes." |
| Data error | "We couldn't process [data]. The file may be corrupted or in an unsupported format." | "We couldn't process your CSV. The file may be corrupted or in an unsupported format." |
| Save error | "Couldn't save your changes. Auto-saved draft available." | "Couldn't save your changes. We auto-saved a draft you can restore." |

### Error message don'ts
- ❌ Oops, Whoops, Uh-oh, Yikes, Oof, or any attempt at humor.
- ❌ "An error occurred" (what error?).
- ❌ "Something went wrong" (no guidance).
- ❌ "Please try again" (try what? will it work this time?).
- ❌ Blaming the user: "Your file is in the wrong format" (rephrase to "We support.csv and.xlsx files").
- ❌ Over-explaining technical details: "ECONNREFUSED on socket 443" means nothing to most users.

---

## 11. AI/LLM Greeting States & System Prompts

Greeting states and prompt alerts set the tone for conversational AI interactions. Keep copy collaborative, boundary-clear, and actionable.

### Greeting States (Empty Chat)
When the user first opens an AI interface, the greeting must establish what the system can do and prompt the next step.
- **Welcome:** Warm, contextual greeting.
- **Capabilities:** Clearly state 2-3 specific tasks the LLM excels at.
- **Suggested Prompts:** Provide click-to-run templates so the user does not face a blank prompt box.

#### Greeting Example
> **System:** "Hello! I am your research assistant. I can help analyze documents, synthesize key findings, or generate summaries. What are we working on?
> 
> **Try these: **
> - [Synthesize key statistics from my reports]
> - [Find contradictions in our meeting transcripts]
> - [Draft a summary of this research paper]"

### Prompt Alerts & Boundary Messages
If the AI reaches a limitation (such as offline database access or long processing times), explain the system status and manage expectations.
- **Be transparent about capability:** Clearly state what the AI can't perform (e.g., "I can't access live internet data").
- **State resource requirements:** If a prompt takes time, tell the user (e.g., "This synthesis requires about 30 seconds. Feel free to browse other tabs while I finish").
- **Acknowledge boundaries gracefully:** Avoid apologetic language. Use "I can only access files loaded into this project. Please upload the PDF to analyze it" instead of "Sorry, I am just an AI and can't do that."

---

## 12. UX Copy Tone Calibration

| Dashboard type | Tone | Example |
|---|---|---|
| Financial/analytics | Professional, precise, data-forward | "Revenue grew 12% this quarter." |
| Internal tool | Direct, efficient, no fluff | "Task assigned. Due Friday." |
| CRM/sales | Encouraging, success-oriented | "Great progress. 5 deals at risk need attention." |
| Health/wellness | Warm, supportive, non-judgmental | "You've logged 3 days this week. Every bit counts." |
| Developer tool | Technical, respectful, concise | "Deploy successful. Build #4512 is live." |
| Small business | Friendly, plain-spoken, reassuring | "Your invoice has been sent. We'll let you know when it's paid." |
