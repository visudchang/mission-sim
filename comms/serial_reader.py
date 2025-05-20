import serial

ser = serial.Serial('/dev/tty.usbserial-0001', 9600)

while True:
    line = ser.readline().decode().strip()
    print("[Serial Received]", line)