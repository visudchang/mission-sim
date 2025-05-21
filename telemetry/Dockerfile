# Use slim version of Python for a small image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy everything from the local folder into the container
COPY . .

# Install required packages
RUN pip install pyserial

# Run the ground station
CMD ["python", "-u", "ground_station.py"]