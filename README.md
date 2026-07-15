# Plate - Meal Tracking Module

Plate is a full-stack meal tracking application built as part of the Fitshield Dietfood Pvt Ltd Full-Stack Developer Assessment.

The application enables users to log meals, track calories and macronutrients against a daily goal, filter meal records, view daily summaries, and analyze calorie trends over time.

The project was developed using Django REST Framework for the backend and React.js for the frontend, with Docker-based local development and deployment support.

## Live URLs

Frontend Live URL: https://zesty-sable-70f48c.netlify.app/

Backend URL:  https://plate-backend-production.up.railway.app/

# Local Setup

The project is fully containerized using Docker and Docker Compose.

## Prerequisites

* Docker
* Docker Compose

## Database Setup

A pre-configured MySQL Docker setup is provided.

1. Extract the provided MySQL shared folder ZIP.
2. Place the extracted folder in the configured Docker volume location.
3. Start the database container:

```bash
docker compose up
```

The MySQL container will automatically start and expose the database on:

```
http://localhost:7000
```

Database credentials are available in the provided `docker-compose.yml` file.

## Backend Setup

Clone the backend repository:

```bash
git clone https://github.com/Aayushi-jain22/plate-backend
```

Navigate to the project directory and start the application:

```bash
docker compose up
```

Database migrations and seed data loading are configured to run automatically during startup.

The application will be ready to use immediately after the containers become healthy.

# AI Tools Used

The following AI tools were used as development assistants during implementation:

* ChatGPT — requirement analysis, debugging support, API design review, and documentation improvements.
* Claude — implementation discussions and architecture validation.
* GitHub Copilot — development productivity and boilerplate generation.

All AI-generated suggestions were reviewed, validated, and modified before integration into the final implementation.

# What I Didn't Finish and Why

The backend and frontend implementation, validation, database optimizations, Docker setup, and local execution were completed successfully.

At the time of submission, the only pending item is the public deployment of the backend service due to deployment-specific configuration issues. The deployment process is actively being finalized, and the live URLs will be shared immediately after successful completion.

Priority was given to ensuring the correctness of the application logic, API behavior, validation rules, database performance, and frontend functionality before final deployment.
