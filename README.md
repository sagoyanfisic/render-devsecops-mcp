# 🛡️ Render DevSecOps Sentinel

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Render-black)](https://render.com)
[![Architecture](https://img.shields.io/badge/architecture-Serverless_Agent-purple)](https://github.com/features/actions)

**A reference implementation for Active Observability in PaaS environments.**

This repository implements a **Sentinel Agent** pattern: an ephemeral, automated auditor that continuously monitors your Render infrastructure for security threats (credential exfiltration) and system instability (critical application errors).

> 📖 **Read the research article:** [Link to your Medium Article]

## 🏗️ Architecture

Unlike passive monitoring solutions, this Sentinel Agent runs externally via **GitHub Actions** cron jobs, ensuring the auditor operates on a separate trust plane from the infrastructure being monitored.



### Core Capabilities

1.  **🕵️ Human Behavior Analysis (Audit Logs):**
    * Detects **Credential Exfiltration** (`ViewConnectionInfoEvent`).
    * Detects **Unauthorized SSH Access** (`StartShellEvent`).
    * Detects **Data Dumps** (`DownloadDatabaseBackupEvent`).

2.  **🔥 System Health Heuristics (App Logs):**
    * Scans runtime logs for keywords like `CRITICAL`, `Panic`, or `Exception`.
    * Alerts on silent failures that don't trigger standard uptime monitors.

3.  **🤖 AI-Native Integration (MCP):**
    * Includes **Model Context Protocol** configuration.
    * Allows AI assistants (Claude, Cursor, Windsurf) to interact with the infrastructure contextually.

---

## 🚀 Quick Start

### 1. Fork & Clone
Fork this repository to your GitHub account to enable the Actions workflows.

### 2. Configure Secrets
Go to your repository **Settings > Secrets and variables > Actions** and add the following:

| Secret | Description |
| :--- | :--- |
| `RENDER_API_KEY` | Your Render API Key (Account Settings). |
| `RENDER_WORKSPACE_ID` | The ID of your workspace (found in the dashboard URL). |
| `RENDER_SERVICE_ID` | The ID of the specific service you want to monitor (e.g., `srv-xxxx`). |
| `SLACK_WEBHOOK` | A Slack Incoming Webhook URL for alerts. |

### 3. Deploy the "Victim" API (Optional)
This repo includes a sample FastAPI application in `src/` to demonstrate log generation.
1. Create a new **Web Service** in Render linked to this repo.
2. **Build Command:** `pip install -r requirements.txt`
3. **Start Command:** `uvicorn src.main:app --host 0.0.0.0 --port 10000`

### 4. Activate the Sentinel
The agent is scheduled to run automatically every 30 minutes. To test it immediately:
1. Go to the **Actions** tab in GitHub.
2. Select **🛡️ Sentinel Active Observer**.
3. Click **Run workflow**.

---

## 📂 Project Structure

```text
render-devsecops-starter/
├── .github/
│   ├── workflows/
│   │   └── security.yml       # The Orchestrator (Cron Job)
│   └── scripts/
│       └── agent.py           # The Brain (Heuristic Logic)
├── mcp/
│   └── config.json            # AI Integration Config
├── src/                       # Sample Application
│   ├── main.py
│   └── routes.py
└── requirements.txt

## 🤖 AI Integration (MCP)

This project supports the official **Render Hosted MCP Server**. This allows you to manage the infrastructure using natural language in Cursor or Claude while you develop.

**Setup for Cursor/Windsurf:**

1. Open your MCP settings (usually `~/.cursor/mcp.json` or via UI).
2. Add the Hosted Render configuration:

```json
{
  "mcpServers": {
    "render": {
      "url": "[https://mcp.render.com/mcp](https://mcp.render.com/mcp)",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY_HERE"
      }
    }
  }
}