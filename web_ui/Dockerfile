# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the web_ui and src directories into the container at /app
COPY web_ui/ web_ui/
COPY src/ src/

# Set the python path to include the app directory
ENV PYTHONPATH /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the web server when the container launches
CMD ["uvicorn", "web_ui.main:app", "--host", "0.0.0.0", "--port", "8000"]