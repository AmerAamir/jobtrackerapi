from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import JobApplication

app = FastAPI(title="Job Tracker API", version="1.0.0")

Base.metadata.create_all(bind=engine)


class JobCreate(BaseModel):
    company: str
    role: str
    status: str


class JobResponse(JobCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


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


@app.get("/jobs", response_model=list[JobResponse])
def list_jobs(db: Session = Depends(get_db)):
    return db.query(JobApplication).all()


@app.post("/jobs", response_model=JobResponse, status_code=201)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    new_job = JobApplication(
        company=job.company,
        role=job.role,
        status=job.status
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


@app.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(JobApplication).filter(JobApplication.id == job_id).first()

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return job
