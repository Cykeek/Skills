# Subagents — Complete Guide

## What Are Subagents?

Subagents are secondary AI agents that run in their own isolated context. Each subagent has:
- Its own conversation history and state
- A configured set of allowed tools
- Optional custom system prompt
- Optional custom model (different from the main Agent)

When the main Agent delegates a task to a subagent, the subagent works autonomously and returns its results. This enables parallel work, specialized research, and complex multi-step coordination.

---

## Built-in Subagent Types

### a) "general-purpose" (Default)
- **Full tool access:** Read, Write, Bash, Edit, WebFetch, Git, etc.
- **Best for:** Implementing features, organizing files, running multi-step tasks in parallel, code review, testing.
- **Use when:** You need a subagent to do real work independently.

### b) "Explore"
- **Read-only access:** Search files, regex grep, call-chain mapping, read content — no write or execute.
- **Best for:** Research, codebase exploration, understanding unfamiliar code, finding patterns.
- **Use when:** You need to understand something without risk of modification.

---

## Creating Custom Subagents (Step-by-Step)

Custom subagents are in **Beta** but fully functional.

### Step 1: Open Settings
- Click the gear icon or navigate to **Settings** in ZCode.
- Find the **Subagents** or **Agents** section.

### Step 2: Create a New Subagent
Click **Create** or **Add** to define a new subagent. Configure these fields:

| Field | Description | Example |
|---|---|---|
| **Name** | Unique identifier. Use lowercase kebab-case. | `code-reviewer` |
| **Model** | (Optional) Override the model. Defaults to parent Agent's model. | `GLM-5.2` |
| **Tool Permissions** | Select allowed tools. Options: Read, Write, Bash, Edit, WebFetch, etc. | Read + Edit only |
| **System Prompt** | Define behavior, expertise, and constraints. **Most important field.** | See examples below |

### Step 3: Write an Effective System Prompt

The system prompt controls everything the subagent does. Make it:
- **Role-defining:** State who the subagent is and what it specializes in.
- **Constraint-focused:** What tools it should/shouldn't use, output format expectations.
- **Context-rich:** If it needs domain knowledge, include it.

**Example 1 — Code Reviewer Subagent:**
```text
You are a senior code reviewer. Your job is to review code diffs for bugs, security issues, performance problems, and style violations. Always output:
1. A severity rating (critical/high/medium/low)
2. The exact file and line number
3. The issue description
4. A suggested fix

Do NOT modify any files. Do NOT run commands. Only read and analyze.
```

**Example 2 — Documentation Writer Subagent:**
```text
You are a technical documentation specialist. Given code files, you produce clear, user-friendly documentation. Output in Markdown format. Include:
- Overview of what the code does
- API/function reference with parameters and return values
- Usage examples
- Setup instructions if applicable

You may read files but must never edit them.
```

**Example 3 — Test Generator Subagent:**
```text
You are a test automation engineer. Given source code, generate comprehensive unit tests. Follow these rules:
- Use the same test framework as the project (detect from package.json or equivalent)
- Cover edge cases, happy paths, and error conditions
- Output each test file in full
- Run the tests after writing them and report failures
You have full tool access: read source files, write test files, and run test commands.
```

### Step 4: Save and Apply
- Save the subagent configuration.
- File is stored on disk at `~/.zcode/agents/<subagent-name>/`.
- Close and reopen Settings if it does not appear immediately.

---

## Using Subagents in Conversation

Once created, subagents can be invoked by the main Agent automatically when it determines a task is suitable for delegation. You can also explicitly ask:

> "Ask the code-reviewer subagent to review my latest changes."
> "Delegate the research task to the Explore subagent."
> "Have the test-generator subagent create tests for utils.py."

---

## Important Limitations & Notes

| Limitation | Details |
|---|---|
| **Scope** | Custom subagents are user-level only (not workspace-level). |
| **Built-ins** | The built-in "general-purpose" and "Explore" subagents cannot be edited or deleted. |
| **Foreground Only** | Subagents run in foreground mode — inline, not background. Main Agent waits for completion. |
| **Storage** | Stored as files in `~/.zcode/agents/<name>/`. |
| **Naming** | Names must be unique. Avoid conflicts with built-in names. |

---

## Best Practices

1. **Start with built-ins first** — Try Explore for research, general-purpose for implementation.
2. **One responsibility per subagent** — Create focused, single-purpose subagents.
3. **Invest in the system prompt** — Quality of prompt determines quality of output. Be specific, include examples, define output format.
4. **Use tool restrictions wisely** — Limit tool access to minimum needed. Research subagents should never have Write or Bash.
5. **Test with real tasks** — After creating, test with a concrete task to verify behavior.
6. **Iterate based on results** — If output isn't as expected, refine the system prompt.

---

## Example Workflows

### Research + Implementation Pattern
1. Main Agent sets goal: "Add user authentication"
2. Delegates to **Explore subagent**: "Research existing auth patterns in the codebase"
3. Explore reads files, returns report
4. Main Agent processes report, delegates to **general-purpose subagent**: "Implement auth following found patterns"
5. General-purpose writes code, runs tests
6. Reports back when done

### Code Review Pattern
1. During a task, Agent creates a **code-reviewer subagent**
2. Passes the diff to it
3. Code reviewer returns findings
4. Main Agent applies suggested fixes
