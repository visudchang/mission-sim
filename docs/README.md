# Mission Simulator by Visud Chang

Mission Simulator is a spacecraft operations system I built to emulate real-time telemetry, orbital mechanics, and command/control loops between a ground station and an onboard flight computer. The system models telemetry from an IMU sensor, visualizes live telemetry and orbital state, and allows mission commands like burns to be executed and monitored in a mission-style interface.

Built using:
-React + Tailwind CSS (GUI)
-Python + Computer Networking (TCP/Websockets/Flask) (Ground Station)
-Golang + C++ (Flight Computer logic)
-Arduino + ESP32 + BNO055 IMU + RF Systems (E32) (Hardware Interface)
-Docker (Containerized Deployment)

Features
-Real-Time Telemetry Feed: Live pitch, roll, yaw, and temperature displayed from a real IMU (BNO055) send using radio frequencies between two LoRa modules.
-Orbit Visualization: Displays orbital trajectory using poliastro based on live burn execution and spacecraft dynamics.
-Mission Command Interface: Adds burns to a command queue, execute maneuvers, and monitor mission log updates.
-Fallback Mode: System switches to simulated data if hardware disconnects, ensuring a smooth demo experience.
-Fully Dockerized: Run the entire system—frontend, backend, and Go logic—with one command.

# Setup Instructions
1. Clone the Repository
In terminal, run:
git clone https://github.com/visudchang/mission-sim.git  
cd mission-sim

2. Run the System with Docker
Make sure Docker and Docker Compose are installed on your machine.
In terminal, run:
docker-compose up --build

Once built, the GUI will be available at: http://localhost:3000

# Project Structure
mission-sim/ 
── gui/ # React frontend 
── go/ # Go-based flight computer 
── sim/ # Orbital mechanics and spacecraft physics 
── telemetry/ # Serial/LoRa/IMU interface 
── comms/ # TCP client-server connection 
── docs/ # README.md 
── tests/ # Unit and integration tests 
── Dockerfile.* # Docker configurations 
── docker-compose.yml ``` </pre>

# Demo
A full demo video is available at: https://visudchang.com/projects/mission-sim.
Alternatively, clone the repo and run locally using Docker, or visit https://visudchang.com/projects/mission-sim/demo.

# Key Technologies
React, Tailwind CSS, Vite
Flask, PySerial, Poliastro, Astropy
Golang TCP Server
Arduino, ESP32, BNO055 IMU
Docker, LoRa RF (for wireless telemetry)

# Author
Visud Chang
NASA Ames | UC Berkeley Aerospace Engineering
https://visudchang.com

