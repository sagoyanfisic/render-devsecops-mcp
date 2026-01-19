import asyncio
import os
import sys
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client

RENDER_MCP_URL = "https://mcp.render.com/mcp"
API_KEY = os.environ.get("RENDER_API_KEY")
SERVICE_ID = "srv-d5n9pol6ubrc73anse60"

if not API_KEY:
    print("❌ Falta RENDER_API_KEY")
    sys.exit(1)

async def run_mcp():
    headers = {"Authorization": f"Bearer {API_KEY}"}

    async with streamablehttp_client(RENDER_MCP_URL, headers=headers) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✅ Conectado a Render MCP")

            # Seleccionar workspace
            await session.call_tool("list_workspaces", arguments={})

            # Actualizar el start command del servicio
            result = await session.call_tool("update_web_service", arguments={
                "serviceId": SERVICE_ID,
                "startCommand": "gunicorn app:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:10000"
            })
            if result.content:
                print(result.content[0].text)

if __name__ == "__main__":
    asyncio.run(run_mcp())
