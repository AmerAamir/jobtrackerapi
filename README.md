# Job Tracker API

Production style FastAPI project for learning DevOps, Systems Operations, SRE, AWS, Kubernetes, CI CD, incident management, and operational excellence.

## Current Features

• Health endpoint
• Basic jobs API
• Automated test for health endpoint

## Local Setup

1. Create virtual environment

python -m venv venv

2. Activate virtual environment

.\venv\Scripts\Activate.ps1

3. Install dependencies

pip install -r requirements.txt

4. Run tests

python -m pytest

5. Run API

uvicorn app.main:app --reload

## Endpoints

GET /health
GET /jobs
POST /jobs
GET /jobs/{job_id}

## Production Goals

• Docker containerization
• PostgreSQL database
• GitHub Actions pipeline
• ECR image registry
• EKS deployment
• CloudWatch logging
• Terraform infrastructure
• Operational runbooks
