package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"log"
	"net"
	"strings"

	"github.com/tarm/serial"
)

type IMUData struct {
	Roll  float64 `json:"ROLL"`
	Pitch float64 `json:"PITCH"`
	Yaw   float64 `json:"YAW"`
	Temp  float64 `json:"TEMP"`
}

func parseLine(line string) (*IMUData, error) {
	data := IMUData{}
	parts := strings.Split(line, ",")
	for _, part := range parts {
		pair := strings.Split(part, ":")
		if len(pair) != 2 {
			continue
		}
		key, val := pair[0], pair[1]
		var f float64
		_, err := fmt.Sscanf(val, "%f", &f)
		if err != nil {
			return nil, err
		}
		switch key {
		case "ROLL":
			data.Roll = f
		case "PITCH":
			data.Pitch = f
		case "YAW":
			data.Yaw = f
		case "TEMP":
			data.Temp = f
		}
	}
	return &data, nil
}

func main() {
	// Start TCP server on port 65433
	ln, err := net.Listen("tcp", ":65433")
	if err != nil {
		log.Fatal("Failed to start TCP server:", err)
	}
	fmt.Println("IMU TCP server listening on port 65433")

	// Connect to Arduino over serial
	ser, err := serial.OpenPort(&serial.Config{Name: "/dev/tty.usbserial-0001", Baud: 115200})
	if err != nil {
		log.Fatal("Serial open failed:", err)
	}
	serialScanner := bufio.NewScanner(ser)

	for {
		conn, err := ln.Accept()
		if err != nil {
			log.Println("Connection error:", err)
			continue
		}
		fmt.Println("Client connected")

		go func(c net.Conn) {
			defer c.Close()
			for serialScanner.Scan() {
				line := serialScanner.Text()
				data, err := parseLine(line)
				if err != nil {
					continue
				}
				jsonData, _ := json.Marshal(data)
				_, err = c.Write([]byte(string(jsonData) + "\n"))
				if err != nil {
					log.Println("Write error:", err)
					break
				}
			}
		}(conn)
	}
}
