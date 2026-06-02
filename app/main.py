from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="Job Tracker API", version="1.0.0")


class JobCreate(BaseModel):
    company: str
    role: str
    status: str


class Job(JobCreate):
    id: int


jobs: Dict[int, Job] = {}
next_id = 1


@app.get("/")
def root():
    return {
        "service": "job-tracker-api",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "job-tracker-api"
    }


@app.get("/jobs")
def list_jobs():
    return list(jobs.values())


@app.post("/jobs", status_code=201)
def create_job(job: JobCreate):
    global next_id

    new_job = Job(
        id=next_id,
        company=job.company,
        role=job.role,
        status=job.status
    )

    jobs[next_id] = new_job
    next_id += 1

    return new_job


@app.get("/jobs/{job_id}")
def get_job(job_id: int):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    return jobs[job_id]
