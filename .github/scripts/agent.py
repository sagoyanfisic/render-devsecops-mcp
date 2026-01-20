import asyncio
import os
import sys
import json
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client

RENDER_MCP_URL = "https://mcp.render.com/mcp"
API_KEY = os.environ.get("RENDER_API_KEY")
SERVICE_ID = "srv-d5n9pol6ubrc73anse60"

# Vectores de amenaza - Audit Events
AUDIT_RISKS = [
    "ViewConnectionInfoEvent",      # Robo de credenciales
    "DownloadDatabaseBackupEvent",  # Robo de datos
    "StartShellEvent",              # Acceso al sistema (RCE)
    # Environment variables
    "UpdateEnvVarsEvent",           # Variables modificadas
    "CreateEnvVarsEvent",           # Variables creadas
    "DeleteEnvVarsEvent",           # Variables eliminadas
    "ViewEnvVarValuesEvent",        # Variables vistas
    "DeleteEnvGroupEvent"           # Grupo de env eliminado
]

# Patrones de seguridad en logs de aplicación
SECURITY_PATTERNS = [
    "XSS_DETECTED",
    "SQLI_DETECTED",
    "SECURITY_ALERT",
    "<script",
    "javascript:",
    "' OR",
    "1=1",
    "DROP TABLE",
    "UNION SELECT"
]

if not API_KEY:
    print("❌ Falta RENDER_API_KEY")
    sys.exit(1)

async def run_mcp():
    headers = {"Authorization": f"Bearer {API_KEY}"}

    async with streamablehttp_client(RENDER_MCP_URL, headers=headers) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✅ Conectado a Render MCP")

            await session.call_tool("list_workspaces", arguments={})

            # Logs de aplicación
            result = await session.call_tool("list_logs", arguments={
                "resource": [SERVICE_ID],
                "limit": 100
            })

            if result.content:
                data = json.loads(result.content[0].text)
                logs = data.get("logs", [])
                print(f"\n📄 Analizando {len(logs)} logs...\n")

                audit_alerts = []
                security_alerts = []

                for log in logs:
                    message = log.get("message", "")
                    timestamp = log.get("timestamp", "")[:19]

                    # Detectar audit events
                    for risk in AUDIT_RISKS:
                        if risk in message:
                            audit_alerts.append(f"🔐 [{timestamp}] {risk}")

                    # Detectar ataques XSS/SQLi
                    for pattern in SECURITY_PATTERNS:
                        if pattern.lower() in message.lower():
                            security_alerts.append(f"🛡️ [{timestamp}] {pattern}: {message[:80]}")
                            break

                # Mostrar últimos logs
                print("📋 Últimos logs:")
                for log in logs[:10]:
                    msg = log.get("message", "")[:80]
                    ts = log.get("timestamp", "")[:19]
                    print(f"  [{ts}] {msg}")

                # Resumen de alertas
                print("\n" + "="*50)
                if audit_alerts:
                    print("\n🚨 AUDIT EVENTS DETECTADOS:")
                    for alert in audit_alerts:
                        print(f"  {alert}")

                if security_alerts:
                    print("\n🚨 ATAQUES DETECTADOS (XSS/SQLi):")
                    for alert in security_alerts:
                        print(f"  {alert}")

                if not audit_alerts and not security_alerts:
                    print("\n✅ No se detectaron amenazas")
                else:
                    print(f"\n⚠️ Total alertas: {len(audit_alerts) + len(security_alerts)}")

if __name__ == "__main__":
    asyncio.run(run_mcp())
