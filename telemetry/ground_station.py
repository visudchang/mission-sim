import socket
import json
import csv
from datetime import datetime
import threading

HOST = "127.0.0.1"
PORT = 65432

def handle_connection(conn, addr, writer):
    global latest_telemetry
    with conn:
        print(f"[Ground Station] Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            try:
                decoded = data.decode().strip()
                if decoded == "GET_STATUS":
                    if latest_telemetry != None:
                        response = json.dumps(latest_telemetry).encode()
                        conn.sendall(response)
                        print("[Ground Station] Sent latest telemetry to requester")
                    else:
                        conn.sendall(b"No data yet.")
                        print("[Ground Station] No telemetry available yet")
                else:
                    telemetry = json.loads(decoded)
                    timestamp = datetime.now().isoformat()
                    telemetry["timestamp"] = timestamp
                    writer.writerow(telemetry)
                    latest_telemetry = telemetry
                    csvfile.flush()
                    print(f"[Telemetry Received] {telemetry}")
            except Exception as e:
                print(f"[Error] {e}")

with open("telemetry/telemetry_log.csv", mode = "a", newline = "") as csvfile:
    fieldnames = ["timestamp", "BAT", "TEMP", "ALT"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    if csvfile.tell() == 0:
        writer.writeheader()

    latest_telemetry = None

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[Ground Station] Listening on {HOST}:{PORT}")
        
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target = handle_connection, args = (conn, addr, writer))
            thread.start()