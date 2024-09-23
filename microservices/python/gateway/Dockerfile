# Use the Python slim image
FROM python:3.10-slim-bullseye

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt requirements.txt


RUN apt update && apt install -y default-libmysqlclient-dev build-essential pkg-config

RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Set environment variables if necessary
# ENV ...

# Expose the port
EXPOSE 5000

# Define the entry point
CMD ["python", "server.py"]
