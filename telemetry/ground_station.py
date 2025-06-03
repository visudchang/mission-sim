import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import socket
import json
import csv
from datetime import datetime
import threading
import serial
import numpy as np
from astropy import units as u

from sim.orbits import orb0
from sim.spacecraft.spacecraft import Spacecraft

HOST = "127.0.0.1"
PORT = 65432

spacecraft = Spacecraft(orb0)
latest_telemetry = None

def serial_reader():
    global latest_telemetry
    ser = serial.Serial('/dev/tty.usbserial-0001', 9600)
    while True:
        try:
            line = ser.readline().decode().strip()
            print("[Serial Received]", line)
            parts = dict(item.strip().split(":") for item in line.split(","))
            print("[Parsed Telemetry]", parts)

            # Keep sensor values but use live orbital data for VEL, ALT, ACC
            now = datetime.now()
            spacecraft.propagate(now)
            orbital_data = spacecraft.get_telemetry()

            telemetry = {
                "BAT": int(parts["BAT"]),
                "TEMP": float(parts["TEMP"]),
                "VEL": orbital_data["VEL"],
                "ALT": orbital_data["ALT"],
                "ACC": orbital_data["ACC"],
                "timestamp": orbital_data["timestamp"]
            }

            latest_telemetry = telemetry

        except Exception as e:
            print("[Serial Error]", e)

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
                    now = datetime.now()
                    spacecraft.propagate(now)
                    telemetry = spacecraft.get_telemetry()

                    latest_telemetry = telemetry
                    response = json.dumps(telemetry).encode()
                    conn.sendall(response)
                    safe_telemetry = {k: v for k, v in telemetry.items() if k != "orbitPath"}
                    print(f"[Ground Station] Sent latest telemetry: {safe_telemetry}")

                    csv_safe = {k: telemetry.get(k, "") for k in writer.fieldnames}
                    writer.writerow(csv_safe)
                    csvfile.flush()

                elif decoded.startswith("BURN:"):
                    burn_str = decoded.split(":")[1]
                    dv_components = [float(x) for x in burn_str.split(",")]
                    if len(dv_components) != 3:
                        raise ValueError("Burn must have 3 components")

                    delta_v_vec = np.array(dv_components) * u.km / u.s
                    spacecraft.apply_burn(delta_v_vec)
                    print(f"[Burn Executed] Δv = {delta_v_vec}")

                    telemetry = spacecraft.get_telemetry(include_path=True)
                    conn.sendall(json.dumps(telemetry).encode())
                    print("[Ground Station] Sent updated orbitPath")

                else:
                    telemetry = json.loads(decoded)
                    telemetry["timestamp"] = datetime.now().isoformat()
                    latest_telemetry = telemetry
                    csv_safe = {k: telemetry.get(k, "") for k in writer.fieldnames}
                    writer.writerow(csv_safe)
                    csvfile.flush()
                    print(f"[Telemetry Received] {telemetry}")

            except Exception as e:
                print(f"[Error] {e}")

# serial_thread = threading.Thread(target=serial_reader, daemon=True)
# serial_thread.start()

with open("telemetry/telemetry_log.csv", mode="a", newline="") as csvfile:
    fieldnames = ["timestamp", "BAT", "TEMP", "VEL", "ALT", "ACC"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    if csvfile.tell() == 0:
        writer.writeheader()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[Ground Station] Listening on {HOST}:{PORT}")
        
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_connection, args=(conn, addr, writer))
            thread.start()
