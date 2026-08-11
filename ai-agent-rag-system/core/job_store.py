from threading import Lock


jobs = {}

jobs_lock = Lock()


def create_job(job_id, query):
    with jobs_lock:
        jobs[job_id] = {
            "job_id": job_id,
            "query": query,
            "status": "pending",
            "result": None,
            "error": None
        }


def update_job(job_id, **updates):
    with jobs_lock:
        if job_id in jobs:
            jobs[job_id].update(updates)


def get_job(job_id):
    with jobs_lock:
        return jobs.get(job_id)