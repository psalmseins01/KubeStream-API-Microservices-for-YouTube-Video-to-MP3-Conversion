# Use the Python slim image
FROM python:3.10-slim-bullseye

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app

RUN apt update && apt install -y build-essential ffmpeg pkg-config

RUN pip install -r /app/requirements.txt

# Copy the rest of the application code
COPY . /app

# Set environment variables if necessary
# ENV ...

# Define the entry point for the app
CMD ["python", "consumer.py"]
