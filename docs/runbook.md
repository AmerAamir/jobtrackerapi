# Job Tracker API Runbook

## Incident: Container running but API not reachable

### Symptom

The Docker container is running, but the API cannot be reached from the browser at:

http://127.0.0.1:8000/health

### Possible Causes

1. Container is not running
2. Port is not published from host to container
3. Application failed to start inside the container
4. Application is listening on the wrong host or port
5. Browser or host machine cannot reach the published port

### First Checks

Check running containers:

docker ps

Check container logs:

docker logs jobapi

Check API from the host machine:

Invoke-RestMethod http://127.0.0.1:8000/health

Check API from inside the container:

docker exec -it jobapi sh

Inside the container, run:

python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/health').read())"

Exit the container shell:

exit

### Key Diagnosis

If docker ps shows:

8000/tcp

The container has port 8000 internally, but the host machine cannot reach it.

If docker ps shows:

0.0.0.0:8000->8000/tcp

Host port 8000 is mapped to container port 8000.

### Root Cause

The container was started without port publishing.

Incorrect command:

docker run --rm --name jobapi-noport job-tracker-api:local

Correct command:

docker run --rm --name jobapi -p 8000:8000 job-tracker-api:local

### Resolution

Stop the bad container with Ctrl + C.

Run the container with port publishing:

docker run --rm --name jobapi -p 8000:8000 job-tracker-api:local

Verify:

docker ps
Invoke-RestMethod http://127.0.0.1:8000/health

### Production Lesson

A running container does not always mean the application is reachable.

Always verify:

1. Container status
2. Port publishing
3. Application logs
4. Host access
5. Internal container access

### Interview Answer

The container was running, but the port was not published to the host. I confirmed this using docker ps. It showed 8000/tcp instead of 0.0.0.0:8000->8000/tcp. I fixed it by running the container with -p 8000:8000.
