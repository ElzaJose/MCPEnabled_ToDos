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
