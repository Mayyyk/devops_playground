# GEMINI.md

## Project Overview

This is a DevOps project that demonstrates a complete CI/CD pipeline for a microservices application. The application consists of a Python/Flask backend API that simulates a water tank model, and a Python/Streamlit frontend that visualizes the simulation data.

The project uses a modern DevOps toolchain to automate the entire lifecycle of the application, from infrastructure provisioning to application deployment and monitoring.

## Architecture

The application is composed of two main services:

*   **`api`:** A Python/Flask backend that provides a REST API for simulating the step response of a water tank model.
*   **`ui`:** A Python/Streamlit frontend that consumes the API and visualizes the simulation data in a web interface.

These services are containerized using Docker and deployed to a Kubernetes cluster.

## Technologies

*   **Infrastructure as Code:** Terraform is used to provision two DigitalOcean droplets that will host the Kubernetes cluster.
*   **Configuration Management:** Ansible is used to configure the servers, install K3s (a lightweight Kubernetes distribution), and deploy the application.
*   **Containerization:** Docker is used to containerize the frontend and backend services.
*   **Orchestration:** Kubernetes (K3s) is used to manage the containerized application.
*   **CI/CD:** GitHub Actions is used to automate the build, test, and deployment process.

## Building and Running

### Local Development

The `workflow.txt` file provides detailed instructions on how to build and run the application locally using `docker`, `k3d`, and `kubectl`.

**1. Create a local Kubernetes cluster:**

```bash
k3d cluster create my-test-cluster --servers 1 --agents 1 -p "8080:80@loadbalancer"
```

**2. Build the Docker images:**

```bash
docker build -t devops-api:local ./src
docker build -t devops-ui:local ./src_frontend
```

**3. Import the images into the local cluster:**

```bash
k3d image import devops-api:local --cluster my-test-cluster
k3d image import devops-ui:local --cluster my-test-cluster
```

**4. Deploy the application to the local cluster:**

```bash
kubectl apply -f k8s/
```

**5. Access the application:**

The application will be available at [http://localhost:8080](http://localhost:8080).

### Production Deployment

The production deployment is fully automated using GitHub Actions. The workflow is triggered on every push to the `master` branch and performs the following steps:

1.  **Provision Infrastructure:** Terraform is used to provision the servers on DigitalOcean.
2.  **Configure Servers:** Ansible is used to configure the servers, install K3s, and deploy the application.
3.  **Build and Push Images:** The Docker images are built and pushed to a container registry.
4.  **Deploy Application:** The Kubernetes manifests are applied to the cluster to deploy the application.

## Development Conventions

*   **Git Workflow:** The project uses a Git workflow with `master`, `dev`, and `feat/...` branches.
*   **Commits:** Commits should be atomic and represent a single logical change.
*   **Pushing:** Code should be pushed to the remote repository regularly for backup and collaboration.
