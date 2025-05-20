import socket
import json
import time
import random

HOST = "127.0.0.1"
PORT = 65432

def generate_telemetry():
    return {
        "BAT": random.randint(90, 100),
        "TEMP": round(random.uniform(20.0, 30.0), 1),
        "ALT": round(random.uniform(400.0, 430.0), 1)
    }

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("[Spacecraft] connected to ground station")
    while True:
        telemetry = generate_telemetry()
        message = json.dumps(telemetry).encode()
        s.sendall(message)
        print(f"[Sent] {telemetry}")
        time.sleep(2)