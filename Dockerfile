# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . .

# Generate gRPC code
RUN python -m grpc_tools.protoc -I./protos --python_out=./src/generated --grpc_python_out=./src/generated ./protos/system.proto

# Make port 50051 available to the world outside this container
EXPOSE 50051

# Define environment variable
ENV DATABASE_URL="postgresql://user:password@postgres:5432/mydatabase"

# Run main.py when the container launches
CMD ["python", "main.py"]