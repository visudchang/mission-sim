#!/bin/bash

SOCAT_LINK="/tmp/ttyV0"
SERIAL_DEV="/dev/cu.usbserial-0001"

echo "Cleaning up socat, Docker, and old device file..."
pkill socat 2>/dev/null || true
docker-compose down -v
rm -rf "$SOCAT_LINK"

echo "Starting socat bridge..."
socat -d -d PTY,link=$SOCAT_LINK,raw,echo=0 FILE:$SERIAL_DEV,raw,echo=0 &
SOCAT_PID=$!

sleep 2

# Confirm that /tmp/ttyV0 is a character device
if [ ! -c "$SOCAT_LINK" ]; then
  echo "ERROR: $SOCAT_LINK is not a character device. Aborting."
  kill $SOCAT_PID
  exit 1
fi

echo "Verified: $SOCAT_LINK is a character device."
echo "Starting Docker containers..."
docker-compose up --build

echo "Cleaning up socat process ($SOCAT_PID)..."
kill $SOCAT_PID
