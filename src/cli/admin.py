import argparse
import pathlib
from typing import Dict, Optional

from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse
import uvicorn

from src.cli.pipeline import run_pipeline
from src.lib.config import load_config
from src.services.job_manager import JobManager


app = FastAPI(title="PrimeArchive Control Panel")
job_manager = JobManager()


def _ollama_status() -> Dict[str, str]:
    config = load_config()
    base_url = config.get("llm_settings", {}).get("base_url", "")
    try:
        import requests

        response = requests.get(f"{base_url}/api/version", timeout=2)
        if response.ok:
            return {"status": "ok", "detail": response.json().get("version", "")}
        return {"status": "error", "detail": f"HTTP {response.status_code}"}
    except Exception as exc:  # pragma: no cover - runtime connectivity
        return {"status": "error", "detail": str(exc)}


def _render_home(jobs: Dict[str, str], status: Dict[str, str]) -> str:
    rows = []
    for job in jobs.values():
        progress_bar = (
            "<div class='progress-wrap'>"
            f"<div class='progress-bar' style='width: {job.progress}%;'></div>"
            "</div>"
        )
        output_link = (
            f"<a href='/jobs/{job.job_id}/output'>view</a> | "
            f"<a href='/jobs/{job.job_id}/download'>download</a>"
            if job.output_path
            else ""
        )
        rows.append(
            f"<tr><td>{job.job_id}</td><td>{job.status}</td>"
            f"<td>{progress_bar}<div>{job.progress}%</div></td><td>{job.last_step}</td>"
            f"<td>{job.input_path}</td><td>{job.output_path}</td>"
            f"<td>{output_link}</td><td>{job.error or ''}</td></tr>"
        )
    table_rows = "".join(rows) or (
        "<tr><td colspan='8'>No jobs yet.</td></tr>"
    )
    return f"""
<!doctype html>
<html>
<head>
  <meta charset='utf-8'>
  <meta http-equiv="refresh" content="5" />
  <title>PrimeArchive Control Panel</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 16px; }}
    th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
    th {{ background: #f5f5f5; }}
    input, select {{ padding: 6px; margin: 4px 0; width: 100%; }}
    button {{ padding: 8px 12px; }}
    .progress-wrap {{ background: #eee; height: 10px; border-radius: 6px; overflow: hidden; }}
    .progress-bar {{ background: #4a7cff; height: 10px; }}
  </style>
</head>
<body>
  <h1>PrimeArchive 控制面板</h1>
  <p>Ollama 狀態: <strong>{status['status']}</strong> {status['detail']}</p>
  <p>頁面每 5 秒自動刷新</p>
  <form method='post' action='/run'>
    <label>輸入檔案路徑</label>
    <input name='input_path' placeholder='/path/to/book.epub' required />
    <label>格式</label>
    <select name='file_format'>
      <option value='epub'>epub</option>
      <option value='pdf'>pdf</option>
      <option value='txt'>txt</option>
    </select>
    <label>輸出 JSONL 路徑</label>
    <input name='output_path' placeholder='/tmp/output.jsonl' required />
    <button type='submit'>開始處理</button>
  </form>

  <h2>最近任務</h2>
  <table>
    <thead>
      <tr><th>ID</th><th>狀態</th><th>進度</th><th>步驟</th><th>輸入</th><th>輸出</th><th>輸出檢視</th><th>錯誤</th></tr>
    </thead>
    <tbody>
      {table_rows}
    </tbody>
  </table>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    jobs = job_manager.list_jobs()
    status = _ollama_status()
    return _render_home(jobs, status)


@app.post("/run")
def run_job(
    input_path: str = Form(...),
    output_path: str = Form(...),
    file_format: str = Form(...),
) -> HTMLResponse:
    input_file = pathlib.Path(input_path)
    if not input_file.exists():
        return HTMLResponse(
            f"<p>Input file not found: {input_path}</p>", status_code=400
        )
    job = job_manager.create_job(input_path, output_path, file_format)
    job_manager.run_in_thread(
        job.job_id,
        run_pipeline,
        pathlib.Path(input_path),
        pathlib.Path(output_path),
        lambda msg: job_manager.append_log(job.job_id, msg),
        lambda progress, step: job_manager.update_job(
            job.job_id, progress=progress, last_step=step
        ),
    )
    return HTMLResponse(
        f"<p>Job started: {job.job_id}</p><p><a href='/'>Back</a></p>",
        status_code=202,
    )


@app.get("/jobs")
def list_jobs() -> JSONResponse:
    jobs = {
        job_id: {
            "status": job.status,
            "input": job.input_path,
            "output": job.output_path,
            "error": job.error,
            "progress": job.progress,
            "last_step": job.last_step,
            "started_at": job.started_at,
            "finished_at": job.finished_at,
        }
        for job_id, job in job_manager.list_jobs().items()
    }
    return JSONResponse(jobs)


@app.get("/jobs/{job_id}")
def get_job(job_id: str) -> JSONResponse:
    job = job_manager.get_job(job_id)
    if not job:
        return JSONResponse({"error": "not found"}, status_code=404)
    return JSONResponse(
        {
            "status": job.status,
            "input": job.input_path,
            "output": job.output_path,
            "error": job.error,
            "progress": job.progress,
            "last_step": job.last_step,
            "logs": job.logs[-50:],
            "started_at": job.started_at,
            "finished_at": job.finished_at,
        }
    )


@app.get("/jobs/{job_id}/output")
def view_output(job_id: str) -> PlainTextResponse:
    job = job_manager.get_job(job_id)
    if not job or not job.output_path:
        return PlainTextResponse("not found", status_code=404)
    path = pathlib.Path(job.output_path)
    if not path.exists():
        return PlainTextResponse("output not ready", status_code=404)
    content = path.read_text(encoding="utf-8").splitlines()
    preview = "\n".join(content[:20])
    return PlainTextResponse(preview)


@app.get("/jobs/{job_id}/download")
def download_output(job_id: str) -> FileResponse:
    job = job_manager.get_job(job_id)
    if not job or not job.output_path:
        return FileResponse("", status_code=404)
    path = pathlib.Path(job.output_path)
    if not path.exists():
        return FileResponse("", status_code=404)
    return FileResponse(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="PrimeArchive admin UI")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
