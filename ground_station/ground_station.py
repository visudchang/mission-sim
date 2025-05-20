import socket
import json
import csv
from datetime import datetime

HOST = "127.0.0.1"
PORT = 65432

with open("telemetry_log.csv", mode = "a", newline = "") as csvfile:
    fieldnames = ["timestamp", "BAT", "TEMP", "ALT"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    if csvfile.tell() == 0:
        writer.writeheader()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[Ground Station] listening on {HOST}:{PORT}")
        conn, addr = s.accept()
        with conn:
            print(f"[Ground Station] connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                try:
                    decoded = data.decode()
                    telemetry = json.loads(decoded)
                    timestamp = datetime.now().isoformat()
                    telemetry["timestamp"] = timestamp
                    writer.writerow(telemetry)
                    csvfile.flush()
                    print(f"[Telemetry Received] {telemetry}")
                except Exception as e:
                    print(f"[Error] {e}")