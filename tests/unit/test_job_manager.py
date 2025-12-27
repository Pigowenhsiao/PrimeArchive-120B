from src.services.job_manager import JobManager


def test_job_lifecycle_updates():
    manager = JobManager()
    job = manager.create_job("in.txt", "out.jsonl", "txt")
    assert job.status == "queued"
    manager.update_job(job.job_id, status="running")
    updated = manager.get_job(job.job_id)
    assert updated is not None
    assert updated.status == "running"
