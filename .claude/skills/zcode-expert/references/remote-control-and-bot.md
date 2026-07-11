# Remote Control & Bot Channel

## Remote Control

Remote Control lets your phone connect to the current desktop ZCode workspace.

### Connection Steps
1. Select the **phone icon** in the bottom-left sidebar.
2. A window appears with a **barcode** and **web address**.
3. Scan the QR code with your phone or visit the link.
4. Once connected, your phone serves as a controller and viewer.

### Capabilities
- View task progress in real-time.
- Send new instructions or extra context.
- **Confirm, continue, or stop** a long-running task.
- Re-enter the session remotely.

### Limitations
- Only one mobile connection at a time.
- Only for projects currently open on the desktop.
- For extended access via chat platforms, use **Bot Channel** instead.

### Use Cases
- Active job requires attention away from the desk.
- Need to add input from your phone.
- Monitoring lengthy processes without returning to PC.

---

## Bot Channel

Bot Channel links external chat apps (WeChat, Feishu) to ZCode so you can interact with the Agent from within those tools over longer periods.

### How It Differs from Remote Control
| Remote Control | Bot Channel |
|---|---|
| Quick QR-code access | Persistent entry inside a chat tool |
| Short-term, immediate | Long-term, revisit over days/weeks |
| One session at a time | Multi-session capable |

### Creating a Bot
1. Navigate to **Bots settings** via the left sidebar.
2. Click **Create Bot**.
3. Choose a channel: **WeChat** or **Feishu**.
4. Support for DingTalk, Discord, and WeCom is planned for future releases.

### Feishu Pairing (Step-by-Step)
1. Select Feishu in ZCode → scan the QR code.
2. ZCode creates the Feishu app automatically and generates a pairing code.
3. In Feishu chat, send `/bind <pairing-code>`.
4. Once confirmed, the Bot becomes active and returns available commands.
5. You can check status, create tasks, switch projects, change models, toggle run mode, and set reply detail.

### Bot Management
- Toggle bots **on/off**.
- **Bind/unbind credentials**.
- Control **reply granularity** (how much detail the Bot reports).
- Define **workspace access scope**.
- **Delete** a Bot entirely.

### Remote Task Flow
1. Send a message to the Bot in WeChat/Feishu.
2. The Bot forwards the request to ZCode Agent.
3. ZCode Agent continues the task in the desktop workspace.
4. Progress updates flow back to the chat thread.
5. Useful for "long-running mobile follow-up" — message the Bot continuously, open full desktop when needed.
