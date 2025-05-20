package main

import (
	"fmt"
	"net"
	"os"
)

func main() {
	conn, err := net.Dial("tcp", "127.0.0.1:65432")
	if err != nil {
		fmt.Println("Error connecting:", err)
		os.Exit(1)
	}
	defer conn.Close()

	message := "GET_STATUS"
	_, err = conn.Write([]byte(message))
	if err != nil {
		fmt.Println("Error sending:", err)
		os.Exit(1)
	}
	fmt.Println("[Operator] Sending command:", message)
	buffer := make([]byte, 1024)
	n, _ := conn.Read(buffer)
	fmt.Println("Received:", string(buffer[:n]))
}
