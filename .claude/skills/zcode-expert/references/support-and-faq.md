# Support & FAQ

## Feedback & Support Channels

### Available Channels
| Channel | Details |
|---|---|
| **Email** | Send details for a one-time submission |
| **In-App Feedback Panel** | Via avatar menu, error banner, or task More menu |
| **GitHub Issues** | `zai-org/feedback` for public tracking |
| **Discord** | Community discussion |
| **Feishu (Lark)** | Official team responds fastest here |
| **WeChat** | Developer beta group available |

### In-App Entry Points
- **Avatar Menu** (lower-left corner) — Best for general usage questions, suggestions, experience issues. Auto-attaches screenshots.
- **Error Banner** — Appears during errors. Useful for initialization failures and runtime errors. Carries error summaries.
- **Task More Menu** (task title bar) — Useful when issue is tied to one task. Includes session file paths.

### Submission Process
1. Submit report → uploads continue in background.
2. Track progress in "My Feedback".
3. Status flow: **Submitted → In Review → In Progress → Closed**.

### Bug Reports
Include: title summary, environment details, steps to reproduce, expected behavior.
- **Recommended:** Use built-in **Export Logs** feature first.
- **Manual logs (macOS):** `~/.zcode`
- **Manual logs (Windows):** `%USERPROFILE%\.zcode`

---

## FAQ & Troubleshooting

### General
| # | Question | Answer |
|---|----------|--------|
| 1 | What's ZCode's positioning? | ZCode is an Agentic Development Environment (ADE). An AI Agent powers the entire coding loop. Built-in file/terminal/Git/preview with full-context AI awareness. Focus on long-task stability and continuous workflow. |
| 2 | Is ZCode free? | The app is free. You need an API key or model plan: GLM Coding Plan, BigModel packages, Z.ai, enterprise-managed channels, or private self-hosted services. |
| 3 | Terminal GLM config needed? | Yes — desktop settings don't sync. Connect via the welcome screen/avatar menu or manually add Base URL & key in "Manage Models". If the account has an active plan, it connects automatically. |

### Connection Issues
| # | Question | Answer |
|---|----------|--------|
| 4 | Connection keeps loading? | Check network access to the model service. Confirm account/API key has quota and model rights. |
| 5 | Coding vs General vs Anthropic endpoints? | **Coding-only:** `.../api/coding/paas/v4` (use with GLM Coding Plan). **General OpenAI:** `.../api/paas/v4` (resource packages/prepaid). **Anthropic:** `.../api/anthropic` (same resources, Anthropic protocol). Mismatching URLs breaks quota usage. |

### Editor Usage
| # | Question | Answer |
|---|----------|--------|
| 6 | Can't pick folders with @? | The `@` picker only lists files, skills, agents. Drag the folder into the input box to add it as context. |
| 7 | Can I edit past messages? | Yes — use Edit History. Hover over a user message, click the pencil icon. Only applies to the latest turn, disabled during active tasks. |
| 8 | What's the difference between $ and /? | `$` triggers skills (complex workflows), `/` triggers commands (simple prompts). |

### Remote Development
| # | Question | Answer |
|---|----------|--------|
| 9 | SSH alias not showing? | Config may be malformed — check the SSH config file syntax. |
| 10 | Remote Dev download fails? | "Download on remote server" requires internet access on the remote host. |
| 11 | Can Mobile Remote Control create SSH/Docker connections? | No — those must be created from the desktop app. |
