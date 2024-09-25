---

# KubeStream API: Microservices for Video to MP3 Conversion

## Project Overview

**KubeStream API** is a microservices-based platform that allows users to upload videos and convert them into MP3 format. This project leverages Python, Flask, Docker, Kubernetes, RabbitMQ, and other tools to build a scalable, efficient, and secure video-to-audio conversion service.

The microservices architecture ensures that each component functions independently, facilitating scalability, maintainability, and flexibility. Each service is containerized using Docker and orchestrated with Kubernetes for seamless deployment and management.

---

## Features

- **User Authentication Service:** Implements JWT-based authentication for secure API access.
- **Gateway Service:** Manages incoming requests, routes them to the appropriate microservices, and performs validation and authentication.
- **Converter Service:** Listens for incoming video upload jobs, converts videos to MP3 format, and stores the output.
- **Notification Service:** Sends notifications to users when the conversion is complete.
- **RabbitMQ Integration:** Handles messaging between services for video processing jobs.
- **Containerization:** Each microservice is containerized using Docker.
- **Kubernetes Orchestration:** The application is deployed on Kubernetes for high availability and scalability.
  
---

## Microservices Architecture

### 1. **Authentication Service**
- **Language/Framework:** Python/Flask
- **Description:** Handles user login, JWT generation, and token validation.
- **Database:** MySQL for user data storage.
- **Key Endpoints:**
  - `/login`: Authenticates users and returns a JWT token.
  - `/validate`: Validates JWT tokens.

### 2. **Gateway Service**
- **Language/Framework:** Python/Flask
- **Description:** Serves as the API gateway, validating user requests and routing them to respective microservices.
- **Key Features:**
  - Authenticates requests using the `auth/validate` endpoint.
  - Routes requests to microservices (e.g., video upload, conversion).

### 3. **Converter Service**
- **Language/Framework:** Python
- **Description:** Responsible for converting uploaded video files into MP3 format using the RabbitMQ queue.
- **Features:**
  - Listens to messages from RabbitMQ for video conversion jobs.
  - Converts the video files to MP3 and stores the results.

### 4. **Notification Service**
- **Description:** Sends email notifications to users once the video conversion process is completed.

---

## Project Directory Structure

```
microservices/
│
├── python/
│   ├── auth/                # Authentication service
│   │   ├── server.py        # Main application logic
│   │   ├── init.sql         # MySQL database schema
│   │   ├── requirements.txt # Dependencies
│   │   ├── Dockerfile       # Docker configuration for auth service
│   │   └── manifest/        # Kubernetes manifests for auth service
│   │       ├── auth-deploy.yaml
│   │       ├── configmap.yaml
│   │       ├── secret.yaml
│   │       ├── service.yaml
│   │
│   ├── gateway/             # API Gateway service
│   │   ├── auth/validate.py # Validation logic for requests
│   │   ├── Dockerfile       # Docker configuration for gateway service
│   │   └── manifest/        # Kubernetes manifests for gateway service
│   │       ├── configmap.yaml
│   │       ├── gateway-deploy.yaml
│   │       ├── ingress.yaml
│   │       ├── secret.yaml
│   │       ├── service.yaml
│   │
│   ├── converter/           # Video-to-MP3 conversion service
│   │   ├── consumer.py      # Message consumer for processing jobs
│   │   ├── convert/         # Conversion logic
│   │   │   └── to_mp3.py    # Video to MP3 conversion script
│   │   ├── Dockerfile       # Docker configuration for converter service
│   │   └── manifest/        # Kubernetes manifests for converter service
│   │
├── manifests/               # Kubernetes manifests for deployment
└── venv/                    # Virtual environments for Python services
```

---

## Prerequisites

- **Docker:** Required to build and run the containerized microservices.
- **Kubernetes:** Required for orchestrating the microservices.
- **RabbitMQ:** For handling asynchronous messaging between services.
- **Python 3.10:** Ensure that Python is installed to run Flask services.
- **MySQL:** Database service for the Authentication service.

---

## Setup and Deployment

### 1. **Clone the Repository**
```bash
git clone https://github.com/psalmseins01/KubeStream-API-Microservices-for-YouTube-Video-to-MP3-Conversion.git
cd KubeStream-API-Microservices-for-YouTube-Video-to-MP3-Conversion.git
```

### 2. **Environment Variables**
Configure the following environment variables for each service:

| Variable        | Description                         |
|-----------------|-------------------------------------|
| `MYSQL_HOST`    | MySQL host (e.g., `localhost`)      |
| `MYSQL_USER`    | MySQL user (e.g., `mysqluser`)      |
| `MYSQL_PASSWORD`| MySQL password (e.g., `mysqlpass`)    |
| `MYSQL_DB`      | MySQL database (e.g., `auth`)       |
| `JWT_SECRET`    | Secret key for encoding JWT tokens  |

These can be configured using Kubernetes ConfigMaps and Secrets for each microservice (see `manifest/configmap.yaml` and `manifest/secret.yaml`).

### 3. **Dockerization**
Each microservice has its own `Dockerfile` for building the container.

Example for the Authentication Service:
```bash
cd microservices/python/auth
docker build -t auth-service .
```

### 4. **Kubernetes Deployment**
Ensure that the Kubernetes manifests are properly configured before deployment. You can deploy each microservice using `kubectl`:

```bash
kubectl apply -f microservices/python/auth/manifest/auth-deploy.yaml
kubectl apply -f microservices/python/gateway/manifest/gateway-deploy.yaml
kubectl apply -f microservices/python/converter/manifest/converter-deploy.yaml
```

---

## Running the Services

1. **Start RabbitMQ:**
   Install and start RabbitMQ using Docker or your package manager.

   ```bash
   docker run -d --hostname my-rabbit --name some-rabbit rabbitmq:3-management
   ```

2. **Run MySQL for Authentication Service:**
   Install MySQL and create the necessary databases using the provided `init.sql` file in the `auth` service.

3. **Run Services in Docker:**
   After building the Docker images, run the containers:

   ```bash
   docker-compose up
   ```

4. **Access the Gateway:**
   Once all services are running, the Gateway will be available on `http://localhost:8000`.

---

## Author

- **Name:** Anthony Gbobo
- **Email:** psalmseins@gmail.com

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Contributions

Contributions are welcome! Please fork the repository and create a pull request with your changes.

---

## Troubleshooting

If you encounter issues during setup, please verify the following:
- All environment variables are correctly set.
- RabbitMQ and MySQL services are up and running.
- Docker images have been built for all services.
- Kubernetes cluster is properly configured, and `kubectl` is authenticated.

For further assistance, please contact the author via the provided email.
