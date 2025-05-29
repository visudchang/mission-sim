import asyncio
import json
import websockets
import socket

TCP_HOST = "127.0.0.1"
TCP_PORT = 65432
WS_PORT = 8765

connected_clients = set()

async def fetch_telemetry_from_tcp():
    buffer = ""
    while True:
        try:
            with socket.create_connection((TCP_HOST, TCP_PORT)) as s:
                print("[Bridge] Connected to TCP ground station")
                while True:
                    s.sendall(b"GET_STATUS\n")
                    chunk = s.recv(8192).decode()
                    buffer += chunk

                    # Try to parse complete JSON objects in the buffer
                    while True:
                        try:
                            obj, idx = json.JSONDecoder().raw_decode(buffer)
                            buffer = buffer[idx:].lstrip()
                            await broadcast(json.dumps(obj))
                        except json.JSONDecodeError:
                            # Incomplete JSON, wait for next chunk
                            break

                    await asyncio.sleep(1)
        except Exception as e:
            print("[Bridge] Connection error:", e)
            await asyncio.sleep(2)

async def broadcast(message):
    for client in connected_clients.copy():
        try:
            await client.send(message)
        except:
            connected_clients.remove(client)

async def handler(websocket):
    connected_clients.add(websocket)
    print("[WebSocket] Client connected")
    try:
        async for _ in websocket:
            pass
    finally:
        connected_clients.remove(websocket)

async def main():
    print(f"[Bridge] Starting WebSocket server on ws://localhost:{WS_PORT}")
    await asyncio.gather(
        websockets.serve(handler, "localhost", WS_PORT),
        fetch_telemetry_from_tcp()
    )

if __name__ == "__main__":
    asyncio.run(main())
