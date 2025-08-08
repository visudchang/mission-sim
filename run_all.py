import subprocess
import threading

def run_ground_station():
    subprocess.run(["python", "telemetry/ground_station.py"])

def run_websocket_proxy():
    subprocess.run(["python", "comms/websocket_proxy.py"])

if __name__ == "__main__":
    threading.Thread(target=run_ground_station).start()
    run_websocket_proxy()
