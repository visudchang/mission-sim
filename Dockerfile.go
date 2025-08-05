FROM golang:1.24.4

WORKDIR /app

COPY go/src/ .

RUN go build -o imu imu.go

CMD ["./imu"]
