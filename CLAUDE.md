# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Render DevSecOps Sentinel - A reference implementation for Active Observability in PaaS environments. Implements a Sentinel Agent pattern: an ephemeral, automated auditor that runs via GitHub Actions cron jobs to monitor Render infrastructure for security threats and system instability.

## Architecture

**Sentinel Agent Pattern**: The auditor runs externally via GitHub Actions, operating on a separate trust plane from the monitored infrastructure.

**Components**:
- `.github/workflows/security.yml` - GitHub Actions orchestrator (cron job)
- `.github/scripts/agent.py` - Heuristic logic for threat detection
- `mcp/config.json` - Model Context Protocol configuration for AI integration
- `src/` - Sample FastAPI application for demonstration

**Core Detection Capabilities**:
1. Human Behavior Analysis (Audit Logs): Credential exfiltration, unauthorized SSH access, data dumps
2. System Health Heuristics (App Logs): Runtime log scanning for CRITICAL, Panic, Exception keywords

## Commands

**Run the sample FastAPI app locally**:
```bash
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 10000
```

**Run the agent script**:
```bash
python .github/scripts/agent.py
```

## Required Secrets (GitHub Actions)

- `RENDER_API_KEY` - Render API Key
- `RENDER_WORKSPACE_ID` - Workspace ID from dashboard URL
- `RENDER_SERVICE_ID` - Service ID (e.g., `srv-xxxx`)
- `SLACK_WEBHOOK` - Slack Incoming Webhook URL for alerts

## MCP Integration

The project uses Render's hosted MCP server at `https://mcp.render.com/mcp` for AI assistant integration (Claude, Cursor, Windsurf). Configuration lives in `mcp/config.json`.
