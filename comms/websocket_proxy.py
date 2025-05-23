import asyncio
import json
import websockets
import socket

TCP_HOST = "127.0.0.1"
TCP_PORT = 65432
WS_PORT = 8765

connected_clients = set()

async def fetch_telemetry_from_tcp():
    while True:
        try:
            with socket.create_connection((TCP_HOST, TCP_PORT)) as s:
                print("[Bridge] Connected to TCP ground station")
                while True:
                    s.sendall(b"GET_STATUS\n")
                    data = s.recv(1024).decode()
                    try:
                        telemetry = json.loads(data)
                        await broadcast(json.dumps(telemetry))
                        await asyncio.sleep(1)
                    except json.JSONDecodeError:
                        print("[Bridge] Invalid telemetry JSON")
                        await asyncio.sleep(1)
        except Exception as e:
            print(f"[Bridge Error] {e}")
            await asyncio.sleep(2)

async def broadcast(message):
    for ws in connected_clients.copy():
        try:
            await ws.send(message)
        except:
            connected_clients.remove(ws)

async def handler(websocket):
    print("[WebSocket] Client connected")
    connected_clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)
        print("[WebSocket] Client disconnected")

async def main():
    print(f"[Bridge] Starting WebSocket server on ws://localhost:{WS_PORT}")
    ws_server = await websockets.serve(handler, "localhost", WS_PORT)

    # Run both the TCP fetcher and WebSocket server loop
    await asyncio.gather(
        fetch_telemetry_from_tcp(),
        ws_server.wait_closed()
    )

if __name__ == "__main__":
    asyncio.run(main())
