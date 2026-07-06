# Goal Mode & ZCode Agent

## ZCode Agent — The Core Driver

The **ZCode Agent** is the central AI driver that powers the entire development loop. It handles:

- **Planning:** Understanding requirements and designing implementation approaches.
- **Coding:** Writing, editing, and refactoring code.
- **Debugging:** Reading errors, analyzing logs, and fixing issues.
- **Preview & Iteration:** Running applications and iterating based on results.
- **Tool Execution:** Using file operations, terminal commands, Git operations, and more.

The Agent is context-aware across the entire workspace — it reads files, terminal output, and knows the current project structure. Tasks, permissions, and file references are all organized around the Agent's workflow.

---

## Goal Mode

**Goal Mode** is designed for complex, long-running tasks. Instead of manually prompting the Agent to continue, the system iterates automatically until the objective is met.

### How It Works
1. Type `/goal <your objective>` to set a session goal.
2. The Agent performs work and runs a verification check at the end of each cycle.
3. If the goal is not met, the next round starts immediately.
4. If complete, the task summarizes and finishes.

### Goal Management
The official docs describe these goal-management actions:
- **Show** the current goal
- **Set** a goal with `/goal <objective>`
- **Replace** the current goal
- **Pause** the goal loop
- **Resume** a paused goal
- **Clear** the goal constraint entirely

### Execution Modes
Goal Mode integrates with execution strategies. The goal defines completion criteria, while the execution mode determines the level of user confirmation needed for actions.

Pair Goal Mode with a permissive execution mode such as **Full Access** to minimize interruptions during extended tasks.

### Status Tracking
Once active, a status card appears in the summary panel showing:
- Progress toward goal
- Time elapsed
- Cost/token consumption

### Best Practices
- Objectives should be **specific and verifiable** (e.g. `Fix all compilation errors` rather than `Make it work`).
- You are not locked in — modify direction or stop the task at any point.
- Ideal for: fixing compilation errors, improving performance scores, implementing features with clear acceptance criteria, and other long-running tasks.
