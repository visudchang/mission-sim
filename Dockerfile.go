# Dockerfile.go
FROM golang:1.21

WORKDIR /app

COPY go/src/ .

RUN go build -o imu imu.go

CMD ["./imu"]
