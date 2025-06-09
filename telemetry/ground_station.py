import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import socket
import json
import csv
import threading
import serial
import numpy as np
from astropy import units as u
from flask import Flask, request, jsonify
from flask_cors import CORS

from sim.orbits import orb0
from sim.spacecraft.spacecraft import Spacecraft

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

HOST = "127.0.0.1"
PORT = 65432

spacecraft = Spacecraft(orb0)
telemetry_log = []

@app.route("/propagate")
def propagate():
    try:
        t = float(request.args.get("missionTime", 0))
        print(f"[Flask] Received missionTime = {t}")
        spacecraft.propagate(t)  # t is mission time in seconds
        telemetry = spacecraft.get_telemetry()
        return jsonify(telemetry)
    except Exception as e:
        print("[Flask ERROR]", e)
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    return jsonify({"message": "Flask server is running!"})

def serial_reader():
    ser = serial.Serial('/dev/tty.usbserial-0001', 9600)
    while True:
        try:
            line = ser.readline().decode().strip()
            print("[Serial Received]", line)
            parts = dict(item.strip().split(":") for item in line.split(","))

            # No propagation here – keep sim time consistent
            orbital_data = spacecraft.get_telemetry()

            telemetry = {
                "BAT": int(parts["BAT"]),
                "TEMP": float(parts["TEMP"]),
                "VEL": orbital_data["VEL"],
                "ALT": orbital_data["ALT"],
                "ACC": orbital_data["ACC"],
                "missionTime": orbital_data["missionTime"]
            }

            telemetry_log.append(telemetry)
            print("[Telemetry Parsed]", telemetry)

        except Exception as e:
            print("[Serial Error]", e)

def handle_connection(conn, addr, writer, csvfile):
    with conn:
        print(f"[Ground Station] Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            try:
                decoded = data.decode().strip()

                if decoded == "GET_STATUS":
                    # Return latest telemetry without propagating
                    telemetry = spacecraft.get_telemetry()
                    response = json.dumps(telemetry).encode()
                    conn.sendall(response)
                    print(f"[Ground Station] Sent latest telemetry: {telemetry}")

                    csv_safe = {k: telemetry.get(k, "") for k in writer.fieldnames}
                    writer.writerow(csv_safe)
                    csvfile.flush()

                elif decoded.startswith("BURN:"):
                    parts = decoded[5:].split(",")
                    dv = [float(p) for p in parts[:3]]
                    spacecraft.apply_burn(np.array(dv) * u.km / u.s)

                    print(f"[Burn Executed] Δv = {dv}")

                    telemetry = spacecraft.get_telemetry(include_path=True)
                    conn.sendall(json.dumps(telemetry).encode())
                    print("[Ground Station] Sent updated orbitPath")

                else:
                    telemetry = json.loads(decoded)
                    telemetry["missionTime"] = spacecraft.mission_time.to_value(u.s)
                    csv_safe = {k: telemetry.get(k, "") for k in writer.fieldnames}
                    writer.writerow(csv_safe)
                    csvfile.flush()
                    print(f"[Telemetry Received] {telemetry}")

            except Exception as e:
                print(f"[Error] {e}")

def socket_server(writer, csvfile):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[Ground Station] Listening on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_connection, args=(conn, addr, writer, csvfile))
            thread.start()

if __name__ == "__main__":
    # Uncomment to enable hardware serial telemetry
    # serial_thread = threading.Thread(target=serial_reader, daemon=True)
    # serial_thread.start()

    with open("telemetry/telemetry_log.csv", mode="a", newline="") as csvfile:
        fieldnames = ["missionTime", "BAT", "TEMP", "VEL", "ALT", "ACC"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        socket_thread = threading.Thread(
            target=lambda: socket_server(writer, csvfile), daemon=True
        )
        socket_thread.start()

        app.run(host="0.0.0.0", port=5000, debug=True)
