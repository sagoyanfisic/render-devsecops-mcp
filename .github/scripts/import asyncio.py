import asyncio
import os
import httpx # pip install httpx

RENDER_MCP_URL = "https://mcp.render.com/mcp"
# API_KEY = os.environ.get("RENDER_API_KEY")
API_KEY = "rnd_zePHIfTo3fXcjxlpQa6EZlJg04kU"

async def debug_stream():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "text/event-stream"
    }
    
    print(f"🔬 Conectando a {RENDER_MCP_URL} en modo RAW...")
    
    async with httpx.AsyncClient() as client:
        try:
            # Usamos aconnect_sse si tienes httpx-sse instalado, si no, stream normal
            async with client.stream("GET", RENDER_MCP_URL, headers=headers, timeout=30) as response:
                print(f"📡 Estado HTTP: {response.status_code}")
                
                if response.status_code != 200:
                    print("❌ Error: El servidor rechazó la conexión.")
                    print(await response.read())
                    return

                print("⏳ Esperando primer byte de datos (Handshake)...")
                
                # Leemos línea por línea lo que manda el servidor
                async for line in response.aiter_lines():
                    if line:
                        print(f"📥 RECIBIDO: {line}")
                        # Si recibimos el endpoint, es que funciona
                        if "endpoint" in line:
                            print("✅ ¡Handshake detectado! El servidor funciona.")
                            break
                    else:
                        # Línea vacía es un "latido" (keep-alive)
                        print("💓 (ping)")

        except httpx.ReadTimeout:
            print("❌ Timeout: El servidor aceptó la conexión pero no envió datos.")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    if not API_KEY:
        print("Falta API Key")
    else:
        asyncio.run(debug_stream())