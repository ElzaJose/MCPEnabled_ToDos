# 🤖 MCP Team To-Do Assistant

A lightweight, local-first **Model Context Protocol (MCP)** server built to help engineering teams track tasks, manage sprint timelines, and parse Minutes of Meeting (MoM) directly through natural language inside **VS Code** using **GitHub Copilot**.

---

## ✨ Key Features

- **Conversational Task Management:** Add, list, filter, update, and delete tasks using natural language prompts.
- **Team-Ready SQLite Backend:** Uses SQLite (`team_tasks.db`) for robust data persistence and safe concurrency when placed in a shared folder (like OneDrive).
- **Rich Task Metadata:** Track assignees, statuses (*Pending*, *In Progress*, *Blocked*, *Completed*), sprint timelines (*Current Sprint*, *Next Sprint*, *TBD*), and detailed remarks for blockers.
- **MoM Parsing:** Paste raw meeting notes directly into Copilot chat and let the AI automatically break down and assign action items.
- **Zero Heavy Infrastructure:** Runs entirely locally via standard input/output (`stdio`) transport over FastMCP.

---

## 🛠️ Tech Stack

- **Python** (Core logic & database handling)
- **[FastMCP](https://github.com/jlowin/fastmcp)** (Automated MCP schema generation and JSON-RPC transport)
- **SQLite** (Local relational database)
- **Model Context Protocol (MCP)** & **GitHub Copilot** (Client/Server agent interface)

---

## 🚀 Installation & Setup

### 1. Prerequisites
- Python 3.10+ installed on your system.
- VS Code with the **GitHub Copilot** extension enabled.

### 2. Clone or Download
Place `team_tracker_server.py` in your local project folder (or directly inside your team's shared OneDrive directory if collaborating).

### 3. Install Dependencies
```bash
pip install fastmcp
```
## Configure VS Code MCP
Register the server in your VS Code user or workspace MCP configuration file (mcp.json):

```json
{
  "servers": {
    "team-todo-tracker": {
      "type": "stdio",
      "command": "python",
      "args": ["/absolute/path/to/your/team_tracker_server.py"]
    }
  }
}
```

## 💡 Example Prompts to Try in Copilot Chat (Agent Mode)
Make sure your Copilot chat is set to Agent Mode, then try these commands:

**Adding a Task:**

  `"Add a task to review the failed test cases, assign it to Rahul, and set the due date to Current Sprint."`

**Parsing Meeting Notes:**

`"Here are the notes from today's sync: [Paste MoM text]. Extract all action items, assign them to respective members, and add them to the tracker."`

**Filtering Tasks:**

`"Show all tasks assigned to Rahul that are currently blocked."`

**Updating Task Status & Remarks:**

`"Mark task #4 as blocked and add a remark: 'Waiting for API credentials from the vendor'."`

**Deleting a Task:**

`"Delete task #2 from the tracker."`

