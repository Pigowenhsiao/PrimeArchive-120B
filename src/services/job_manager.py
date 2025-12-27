import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


@dataclass
class JobStatus:
    job_id: str
    status: str
    input_path: str
    output_path: str
    file_format: str
    started_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    finished_at: Optional[str] = None
    error: Optional[str] = None
    progress: int = 0
    last_step: str = "queued"
    logs: list[str] = field(default_factory=list)
    log_path: Optional[str] = None


class JobManager:
    def __init__(self) -> None:
        self._jobs: Dict[str, JobStatus] = {}
        self._lock = threading.Lock()
        self._log_dir = Path("data/job_logs")
        self._log_dir.mkdir(parents=True, exist_ok=True)

    def create_job(self, input_path: str, output_path: str, file_format: str) -> JobStatus:
        job_id = str(uuid.uuid4())
        log_path = self._log_dir / f"{job_id}.log"
        status = JobStatus(
            job_id=job_id,
            status="queued",
            input_path=input_path,
            output_path=output_path,
            file_format=file_format,
            log_path=str(log_path),
        )
        with self._lock:
            self._jobs[job_id] = status
        return status

    def get_job(self, job_id: str) -> Optional[JobStatus]:
        with self._lock:
            return self._jobs.get(job_id)

    def list_jobs(self) -> Dict[str, JobStatus]:
        with self._lock:
            return dict(self._jobs)

    def update_job(self, job_id: str, **kwargs: str) -> None:
        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return
            for key, value in kwargs.items():
                setattr(job, key, value)

    def append_log(self, job_id: str, message: str) -> None:
        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return
            job.logs.append(message)
            if job.log_path:
                Path(job.log_path).parent.mkdir(parents=True, exist_ok=True)
                with open(job.log_path, "a", encoding="utf-8") as handle:
                    handle.write(message)
                    handle.write("\n")

    def run_in_thread(self, job_id: str, target, *args) -> None:
        def runner() -> None:
            self.update_job(job_id, status="running")
            try:
                target(*args)
                self.update_job(
                    job_id,
                    status="succeeded",
                    finished_at=datetime.utcnow().isoformat(),
                )
            except Exception as exc:  # pragma: no cover - runtime errors
                self.update_job(
                    job_id,
                    status="failed",
                    finished_at=datetime.utcnow().isoformat(),
                    error=str(exc),
                )

        thread = threading.Thread(target=runner, daemon=True)
        thread.start()
