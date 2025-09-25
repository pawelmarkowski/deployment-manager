# Quick Start Guide

This guide provides step-by-step instructions to set up and run the project on your local machine.

## Prerequisites

Before you begin, ensure you have the following tools installed:

-   **Python** (version 3.10 or higher)
-   **Pip** and **venv**
-   **Docker**
-   **A local Kubernetes cluster** (e.g., [Docker Desktop's built-in cluster](https://docs.docker.com/desktop/kubernetes/), [Minikube](https://minikube.sigs.k8s.io/docs/start/), or [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/))
-   **[Tilt](https://docs.tilt.dev/install.html)** (for local development orchestration)

## 1. Environment Setup

First, clone the repository and set up the necessary files.

```bash
# Clone the repository (if you haven't already)
# git clone <repository-url>
# cd <repository-name>

# Create a file to hold the database password.
# This file is git-ignored, so the password will not be checked into version control.
echo "mysecretpassword" > postgres-password.txt

# Create a Python virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS and Linux:
source venv/bin/activate
# On Windows:
# .\venv\Scripts\activate

# Install the required Python packages
pip install -r requirements.txt
```

## 2. Running the Application with Tilt

With the prerequisites installed and the environment set up, you can start the entire application stack using Tilt.

Make sure your local Kubernetes cluster is running, then execute the following command in your terminal:

```bash
tilt up
```

Tilt will now:
1.  Build the Docker image for the Python application.
2.  Create a Kubernetes secret for the database password.
3.  Deploy the PostgreSQL database and the application to your Kubernetes cluster.
4.  Deploy a gRPC UI for interacting with the application.
5.  Set up port-forwarding:
    -   PostgreSQL will be accessible at `localhost:5432`.
    -   The gRPC service will be accessible at `localhost:50051`.
    -   The gRPC UI will be accessible at `http://localhost:8080`.
6.  Run the database seeding script to populate the database with initial data.
7.  Run the `flake8` and `pylint` linters to check the code.
8.  Open a web UI in your browser at `http://localhost:10350/` where you can monitor the status of all your services.

The application will automatically reload if you make any changes to the source code.

## 3. Interacting with the gRPC API

Once the application is running, you can interact with it using the gRPC UI.

Open your web browser and navigate to [**http://localhost:8080**](http://localhost:8080).

You will see a simple web interface where you can:
-   Select a service (e.g., `system.System`).
-   Select a method (e.g., `GetProduct`).
-   Enter the request data in JSON format (e.g., `{"id": 1}`).
-   Click "Invoke" to send the request and see the response.

This provides a much more user-friendly way to explore the API than using `grpcurl`.

## 4. Shutting Down

To stop and clean up the environment, you can run:

```bash
tilt down
```

This will delete all the resources that were created in your Kubernetes cluster. To deactivate the Python virtual environment, simply run:

```bash
deactivate
```