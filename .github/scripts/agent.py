import asyncio
import os
import sys
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client

RENDER_MCP_URL = "https://mcp.render.com/mcp"
API_KEY = os.environ.get("RENDER_API_KEY")
WORKSPACE_ID = os.environ.get("RENDER_WORKSPACE_ID", "tea-d5n616cmrvns73figjog")

if not API_KEY:
    print("❌ Falta RENDER_API_KEY")
    sys.exit(1)

async def run_mcp():
    headers = {"Authorization": f"Bearer {API_KEY}"}

    async with streamablehttp_client(RENDER_MCP_URL, headers=headers) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✅ Conectado a Render MCP")

            # Seleccionar workspace (list_workspaces auto-selecciona si solo hay uno)
            ws_result = await session.call_tool("list_workspaces", arguments={})
            if ws_result.content and "automatically selected" not in ws_result.content[0].text.lower():
                await session.call_tool("select_workspace", arguments={"workspaceId": WORKSPACE_ID})

            # Listar servicios
            result = await session.call_tool("list_services", arguments={"limit": 10})
            if result.content:
                print(result.content[0].text)

if __name__ == "__main__":
    asyncio.run(run_mcp())
