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

            # Crear web service
            result = await session.call_tool("create_web_service", arguments={
                "name": "render-devsecops-api",
                "repo": "https://github.com/TU_USUARIO/render-devsecops-mcp",
                "branch": "main",
                "buildCommand": "pip install -r requirements.txt",
                "startCommand": "gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:10000",
                "plan": "free",
                "region": "oregon"
            })
            if result.content:
                print(result.content[0].text)

if __name__ == "__main__":
    asyncio.run(run_mcp())
