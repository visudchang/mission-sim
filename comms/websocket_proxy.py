import asyncio
import json
import websockets
import socket
import time
import random

last_valid_telemetry_time = 0
fallback_active = False

TCP_HOST = "127.0.0.1"
TCP_PORT = 65432
WS_PORT = 8765

connected_clients = set()

tcp_writer = None  # will hold TCP connection writer

async def fetch_telemetry_from_tcp():
    global tcp_writer
    buffer = ""
    while True:
        try:
            with socket.create_connection((TCP_HOST, TCP_PORT)) as s:
                tcp_writer = s
                print("[Bridge] Connected to TCP ground station")
                while True:
                    s.sendall(b"GET_STATUS\n")
                    chunk = s.recv(8192).decode()
                    buffer += chunk

                    while True:
                        try:
                            obj, idx = json.JSONDecoder().raw_decode(buffer)
                            buffer = buffer[idx:].lstrip()
                            await broadcast(json.dumps(obj))
                        except json.JSONDecodeError:
                            break

                    await asyncio.sleep(1 / 24)
        except Exception as e:
            print("[Bridge] Connection error:", e)
            tcp_writer = None
            await asyncio.sleep(2)

async def broadcast(message):
    for client in connected_clients.copy():
        try:
            await client.send(message)
        except:
            connected_clients.remove(client)

async def handler(websocket):
    global tcp_writer
    connected_clients.add(websocket)
    print("[WebSocket] Client connected")
    try:
        async for message in websocket:
            print(f"[WebSocket] Received from browser: {message}")
            if tcp_writer:
                try:
                    tcp_writer.sendall(message.encode())
                    print(f"[Bridge] Sent to TCP: {message}")
                except Exception as e:
                    print(f"[Bridge] Failed to send to TCP: {e}")
            else:
                print("[Bridge] TCP connection not established")
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
