import asyncio
import json
import os
import sys
import urllib.request
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client

# Config
RENDER_MCP_URL = "https://mcp.render.com/mcp"
API_KEY = os.environ.get("RENDER_API_KEY")
SERVICE_ID = os.environ.get("RENDER_SERVICE_ID", "srv-d5n9pol6ubrc73anse60")
SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK")

# Threat vectors
AUDIT_RISKS = [
    "ViewConnectionInfoEvent",
    "DownloadDatabaseBackupEvent",
    "StartShellEvent",
    "UpdateEnvVarsEvent",
    "CreateEnvVarsEvent",
    "DeleteEnvVarsEvent",
    "ViewEnvVarValuesEvent",
    "DeleteEnvGroupEvent"
]

SECURITY_PATTERNS = [
    "XSS_DETECTED", "SQLI_DETECTED", "SECURITY_ALERT",
    "<script", "javascript:", "' OR", "1=1", "DROP TABLE", "UNION SELECT"
]


async def scan_logs() -> dict:
    """Scan Render logs for security threats."""
    if not API_KEY:
        print("❌ RENDER_API_KEY missing")
        sys.exit(1)

    alerts = {"audit": [], "security": [], "logs_analyzed": 0}
    headers = {"Authorization": f"Bearer {API_KEY}"}

    async with streamablehttp_client(RENDER_MCP_URL, headers=headers) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✅ Connected to Render MCP")

            await session.call_tool("list_workspaces", arguments={})
            result = await session.call_tool("list_logs", arguments={
                "resource": [SERVICE_ID],
                "limit": 100
            })

            if not result.content:
                return alerts

            logs = json.loads(result.content[0].text).get("logs", [])
            alerts["logs_analyzed"] = len(logs)
            print(f"\n📄 Analyzing {len(logs)} logs...\n")

            for log in logs:
                msg = log.get("message", "")
                ts = log.get("timestamp", "")[:19]

                for risk in AUDIT_RISKS:
                    if risk in msg:
                        alerts["audit"].append(f"[{ts}] {risk}")

                for pattern in SECURITY_PATTERNS:
                    if pattern.lower() in msg.lower():
                        alerts["security"].append(f"[{ts}] {pattern}: {msg[:80]}")
                        break

            # Print summary
            print("📋 Recent logs:")
            for log in logs[:10]:
                print(f"  [{log.get('timestamp', '')[:19]}] {log.get('message', '')[:80]}")

            print("\n" + "=" * 50)
            if alerts["audit"]:
                print("\n🚨 AUDIT EVENTS:")
                for a in alerts["audit"]:
                    print(f"  🔐 {a}")

            if alerts["security"]:
                print("\n🚨 SECURITY ATTACKS:")
                for a in alerts["security"]:
                    print(f"  🛡️ {a}")

            total = len(alerts["audit"]) + len(alerts["security"])
            if total == 0:
                print("\n✅ No threats detected")
            else:
                print(f"\n⚠️ Total alerts: {total}")

    return alerts


def notify_slack(alerts: dict):
    """Send Slack notification."""
    if not SLACK_WEBHOOK:
        return

    total = len(alerts.get("audit", [])) + len(alerts.get("security", []))
    text = f"🚨 ALERTA: Vulnerabilidad detectada en {SERVICE_ID}" if total else f"✅ Scan OK - {SERVICE_ID}"

    try:
        req = urllib.request.Request(SLACK_WEBHOOK, json.dumps({"text": text}).encode(), {"Content-Type": "application/json"})
        urllib.request.urlopen(req)
    except Exception:
        pass


if __name__ == "__main__":
    alerts = asyncio.run(scan_logs())
    notify_slack(alerts)
