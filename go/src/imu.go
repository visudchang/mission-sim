package main

import (
	"bufio"
	"fmt"
	"log"
	"strings"

	"github.com/tarm/serial"
)

type IMUData struct {
	Roll  float64
	Pitch float64
	Yaw   float64
	Temp  float64
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
	c := &serial.Config{Name: "/dev/cu.usbserial-0001", Baud: 115200} // or "COM3" on Windows, "/dev/tty.usbserial-..." on Mac
	s, err := serial.OpenPort(c)
	if err != nil {
		log.Fatal(err)
	}
	scanner := bufio.NewScanner(s)
	for scanner.Scan() {
		line := scanner.Text()
		fmt.Println("Raw:", line)
		data, err := parseLine(line)
		if err != nil {
			log.Println("Parse error:", err)
			continue
		}
		fmt.Printf("Parsed: %+v\n", data)
	}
}
