# ZCode Installation & Model Connection

## Installation

### Supported Platforms
| Platform | Architecture | Installer |
|---|---|---|
| macOS | Apple Silicon | `.dmg` |
| macOS | Intel | `.dmg` |
| Windows | x64 (64-bit) | `.exe` |
| Windows | ARM64 | `.exe` |
| Linux | x64 / ARM64 | Requires beta group |

### Steps by OS
- **Windows:** Download `.exe`, double-click, follow setup wizard.
- **macOS:** Open `.dmg`, drag `ZCode.app` to `Applications`, launch from Launchpad.
- **Linux:** Join the beta group, get the package, install via distribution's standard method.

### Verification
Launch the app and sign in. The welcome screen prompts you to connect a model.

---

## Model Connection

### Where to Configure
- **First-launch welcome screen** — appears automatically after install.
- **In-app:** Click the model name in chat → "Manage Models" → opens settings panel.

### Connection Methods
| Method | How It Works |
|---|---|
| **Account Binding** | Authorize with Z.ai or BigModel to auto-bind account. |
| **API Key** | Manually enter credentials for direct access. |

### GLM Models (Z.ai & BigModel)

⚠️ **Critical:** The Coding endpoint and General endpoint are NOT interchangeable.

| Use Case | OpenAI-compatible URL | Anthropic-compatible URL |
|---|---|---|
| **Coding only** | `/api/coding/paas/v4` | `/api/anthropic` |
| **General usage** | `/api/paas/v4` | `/api/anthropic` |

- Connecting BigModel grants new users a free daily trial quota.
- Subscriptions purchaseable within the app.

### Third-Party & Custom Providers
Click "Add Provider", name the service, input Base URL and API Key. System auto-detects and loads available models.

| Provider | Endpoint |
|---|---|
| **OpenAI** | `https://api.openai.com` |
| **Anthropic** | `https://api.anthropic.com` |
| **OpenRouter** | `https://openrouter.ai/api` |
| **Moonshot** | `https://api.moonshot.cn/anthropic` |
| **MiniMax** | `https://api.minimaxi.com/anthropic` |
| **Xiaomi MiMo** | `https://api.xiaomimimo.com/v1` |

Custom providers (compatible with OpenAI or Anthropic protocols) also work — enter Base URL + key, system detects available models automatically.

### Verification
Select the channel in the chat model picker, send a test instruction. If the model responds reliably, connection works.

### Troubleshooting Connection Issues
- **Connection keeps loading:** Check network access to model service. Confirm API key has quota and model rights.
- **Wrong endpoint:** Using General endpoint with Coding Plan (or vice versa) breaks quota usage. Switch to the correct endpoint.
- **Terminal config:** Desktop settings don't sync to terminal. Connect via welcome screen, avatar menu, or manually add Base URL & key in "Manage Models".
