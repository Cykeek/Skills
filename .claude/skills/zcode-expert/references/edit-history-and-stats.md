# Edit History & Usage Stats

## Edit History

Edit History lets you revise messages previously sent to the Agent without restarting the session. It preserves the model, workspace, and task context.

### How to Access
- Hover over a user message → **pencil icon** appears.
- Click it to switch the original message to editable input.

### What You Can Do
- Fix unclear instructions, missing paths, or wrong constraints.
- Add file references using `@`.
- Insert commands.
- Submit → Agent continues based on new context.
- Cancel → original message stays intact.

### Limitations
- Applies only to the **latest turn** in the conversation.
- Disabled while a task is actively running or messages are queued.

### Common Use Cases
- Correcting incomplete requirements.
- Adding missing details like file paths or error logs.
- Shifting task objectives mid-stream.
- Fixing a target, path, or constraint without repeated setup.

---

## Usage Stats

### App Usage
Monitors local ZCode sessions on your device:
- **Token usage, sessions, messages, active days**
- Streak information and peak hours
- **Daily token trends** and an **activity heatmap**
- **Model usage ranking** (which models you use most)
- Filter options: All Time, Last 30 Days, Last 7 Days
- Interactive charts showing token breakdowns by model and usage comparisons

### Coding Plan
Tracks remote Z.ai/BigModel Coding Plan statistics:
- **Quota status:** 5-hour prompt pool, weekly quota, monthly MCP quota
- Token consumption across models (GLM-5.2, GLM-5-Turbo, etc.)
- Tool usage (Network Search MCP, Web Reader MCP, etc.)
- Expanded details reveal context-window breakdown, message and tool usage share, and remaining quota
