import argparse
import pathlib
from typing import Dict, Optional

from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse
import uvicorn

from src.cli.pipeline import run_pipeline
from src.cli.validate import run_validation
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


def _ollama_models() -> list[str]:
    config = load_config()
    base_url = config.get("llm_settings", {}).get("base_url", "")
    if not base_url:
        return []
    try:
        import requests

        response = requests.get(f"{base_url}/api/tags", timeout=2)
        if not response.ok:
            return []
        payload = response.json()
        return [model.get("name", "") for model in payload.get("models", []) if model.get("name")]
    except Exception:  # pragma: no cover - runtime connectivity
        return []


def _render_home(jobs: Dict[str, str], status: Dict[str, str], models: list[str]) -> str:
    rows = []
    for job in jobs.values():
        progress_bar = (
            "<div class='progress-wrap'>"
            f"<div class='progress-bar' style='width: {job.progress}%;'></div>"
            "</div>"
        )
        output_link = (
            "<span class='links'>"
            f"<a href='/jobs/{job.job_id}/output'>view</a> | "
            f"<a href='/jobs/{job.job_id}/download'>download</a>"
            "</span>"
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
    model_options = (
        "".join(f"<option value='{name}'>{name}</option>" for name in models)
        if models
        else "<option value=''>無可用模型</option>"
    )
    return f"""
<!doctype html>
<html>
<head>
  <meta charset='utf-8'>
  <title>PrimeArchive Control Panel</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@400;600;700&family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {{
      --ink: #0f1620;
      --panel: #f7f5ef;
      --panel-strong: #fdfbf7;
      --accent: #0e7c86;
      --accent-2: #d98324;
      --muted: #596776;
      --line: rgba(15, 22, 32, 0.12);
      --shadow: 0 20px 60px rgba(15, 22, 32, 0.12);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      font-family: "IBM Plex Sans", "Segoe UI", sans-serif;
      margin: 0;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(14, 124, 134, 0.18), transparent 55%),
        radial-gradient(circle at 20% 20%, rgba(217, 131, 36, 0.12), transparent 45%),
        linear-gradient(120deg, #f5f2ea, #eef2f5);
      min-height: 100vh;
    }}
    .frame {{
      max-width: 1200px;
      margin: 32px auto 80px;
      padding: 0 24px;
    }}
    header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 20px 24px;
      border-radius: 20px;
      background: var(--panel);
      box-shadow: var(--shadow);
      border: 1px solid var(--line);
    }}
    .brand {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .brand h1 {{
      font-family: "Fraunces", "Georgia", serif;
      font-size: 32px;
      margin: 0;
      letter-spacing: 0.5px;
    }}
    .brand p {{
      margin: 0;
      color: var(--muted);
      font-size: 14px;
    }}
    .status {{
      display: inline-flex;
      align-items: center;
      gap: 10px;
      padding: 8px 14px;
      border-radius: 999px;
      font-family: "IBM Plex Mono", monospace;
      font-size: 13px;
      border: 1px solid var(--line);
      background: var(--panel-strong);
    }}
    .status::before {{
      content: "";
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #b94f3a;
      box-shadow: 0 0 0 3px rgba(185, 79, 58, 0.15);
    }}
    .status[data-status="ok"]::before {{
      background: #1d8f6a;
      box-shadow: 0 0 0 3px rgba(29, 143, 106, 0.15);
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 20px;
      margin-top: 24px;
    }}
    .card {{
      background: var(--panel);
      border-radius: 20px;
      padding: 22px;
      border: 1px solid var(--line);
      box-shadow: var(--shadow);
    }}
    .card h2 {{
      font-family: "Fraunces", "Georgia", serif;
      margin: 0 0 12px;
      font-size: 22px;
    }}
    .card p {{
      margin: 0 0 16px;
      color: var(--muted);
      font-size: 14px;
    }}
    label {{
      display: block;
      font-size: 13px;
      color: var(--muted);
      margin: 10px 0 6px;
    }}
    input, select {{
      width: 100%;
      padding: 10px 12px;
      border-radius: 12px;
      border: 1px solid var(--line);
      background: var(--panel-strong);
      font-family: "IBM Plex Mono", monospace;
      font-size: 13px;
    }}
    button {{
      margin-top: 16px;
      padding: 10px 16px;
      border-radius: 12px;
      border: 1px solid var(--ink);
      background: var(--ink);
      color: #fff;
      font-weight: 600;
      letter-spacing: 0.4px;
      cursor: pointer;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    button:hover {{
      transform: translateY(-1px);
      box-shadow: 0 10px 18px rgba(15, 22, 32, 0.2);
    }}
    .meta {{
      display: flex;
      align-items: center;
      gap: 12px;
      color: var(--muted);
      font-size: 13px;
    }}
    .table-wrap {{
      margin-top: 28px;
      background: var(--panel);
      border-radius: 20px;
      border: 1px solid var(--line);
      box-shadow: var(--shadow);
      overflow: hidden;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
      font-size: 13px;
    }}
    th, td {{
      padding: 12px 14px;
      text-align: left;
      border-bottom: 1px solid var(--line);
      vertical-align: top;
    }}
    th {{
      background: #efece6;
      font-weight: 600;
      font-family: "IBM Plex Mono", monospace;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      font-size: 11px;
    }}
    tr:last-child td {{
      border-bottom: none;
    }}
    .progress-wrap {{
      background: rgba(15, 22, 32, 0.08);
      height: 10px;
      border-radius: 999px;
      overflow: hidden;
    }}
    .progress-bar {{
      background: linear-gradient(90deg, var(--accent), var(--accent-2));
      height: 10px;
    }}
    .links a {{
      color: var(--accent);
      text-decoration: none;
      font-weight: 600;
    }}
    .links a:hover {{
      text-decoration: underline;
    }}
    @media (max-width: 720px) {{
      header {{
        flex-direction: column;
        align-items: flex-start;
      }}
      .frame {{
        margin: 20px auto 60px;
      }}
    }}
  </style>
</head>
<body>
  <div class="frame">
    <header>
      <div class="brand">
        <h1>PrimeArchive 控制面板</h1>
        <p>本地管線監控與資料輸出入口 · 即時狀態更新</p>
      </div>
      <div class="meta">
        <div class="status" data-status="{status['status']}">
          Ollama {status['status']} {status['detail']}
        </div>
      </div>
    </header>

    <section class="grid">
      <div class="card">
        <h2>Pipeline 任務</h2>
        <p>選擇檔案或路徑，啟動資料清理、分塊與生成流程。</p>
        <form method='post' action='/run' enctype='multipart/form-data' id="pipeline-form">
          <label>輸入檔案（檔案選擇）</label>
          <input name='upload_file' type='file' id="upload_file" />
          <label>或輸入檔案路徑</label>
          <input name='input_path' placeholder='/path/to/book.epub' id="input_path" />
          <label>格式</label>
          <select name='file_format' required>
            <option value='epub'>epub</option>
            <option value='pdf'>pdf</option>
            <option value='txt'>txt</option>
          </select>
          <label>輸出 JSONL 路徑</label>
          <input name='output_path' placeholder='/tmp/output.jsonl' required />
          <label>模型名稱（可覆寫）</label>
          <select name='model_name'>
            <option value=''>自動（使用預設設定）</option>
            {model_options}
          </select>
          <label>溫度（可覆寫）</label>
          <input name='temperature' placeholder='0.1' />
          <label>逾時秒數（可覆寫）</label>
          <input name='timeout' placeholder='300' />
          <label>僅處理前 N 個 Chunk（0=全部）</label>
          <input name='max_chunks' placeholder='5' />
          <label>Debug：輸出 Chunk 到螢幕</label>
          <select name='dump_chunks'>
            <option value='false'>false</option>
            <option value='true'>true</option>
          </select>
          <label>Debug：Chunk 檔案輸出路徑（可選）</label>
          <input name='dump_path' placeholder='./data/debug_chunks.txt' />
          <label>Debug：列印 LLM 原始輸出</label>
          <select name='print_llm_output'>
            <option value='false'>false</option>
            <option value='true'>true</option>
          </select>
          <button type='submit'>開始處理</button>
        </form>
      </div>

      <div class="card">
        <h2>驗證工具</h2>
        <p>以 JSONL 檢測引用準確度並產出 hallucination rate。</p>
        <form method='post' action='/validate' enctype='multipart/form-data' id="validate-form">
          <label>JSONL 檔案路徑</label>
          <input name='validate_path' placeholder='/tmp/output.jsonl' id="validate_path" required />
          <label>或上傳 JSONL 檔案</label>
          <input name='validate_file' type='file' id="validate_file" />
          <button type='submit'>執行驗證</button>
        </form>
      </div>
    </section>

    <section class="grid">
      <div class="card">
        <h2>處理狀態</h2>
        <p id="job-status">尚未啟動任務。</p>
        <div class="progress-wrap" aria-label="job-progress">
          <div class="progress-bar" id="job-progress" style="width: 0%;"></div>
        </div>
      </div>
      <div class="card">
        <h2>輸出預覽</h2>
        <p>顯示最新任務的前 20 行輸出。</p>
        <pre id="job-output" style="white-space: pre-wrap; font-family: 'IBM Plex Mono', monospace; font-size: 12px; background: var(--panel-strong); padding: 12px; border-radius: 12px; border: 1px solid var(--line); min-height: 120px;">尚未載入。</pre>
      </div>
    </section>

    <section class="table-wrap">
      <table>
        <thead>
          <tr><th>ID</th><th>狀態</th><th>進度</th><th>步驟</th><th>輸入</th><th>輸出</th><th>輸出檢視</th><th>錯誤</th></tr>
        </thead>
        <tbody>
          {table_rows}
        </tbody>
      </table>
    </section>
  </div>
  <script>
    const uploadInput = document.getElementById("upload_file");
    const pathInput = document.getElementById("input_path");
    const validateFileInput = document.getElementById("validate_file");
    const validatePathInput = document.getElementById("validate_path");
    const pipelineForm = document.getElementById("pipeline-form");
    const jobStatus = document.getElementById("job-status");
    const jobProgress = document.getElementById("job-progress");
    const jobOutput = document.getElementById("job-output");
    let activeJobId = null;
    let pollTimer = null;

    const setJobStatus = (text, progress) => {{
      if (jobStatus) {{
        jobStatus.textContent = text;
      }}
      if (jobProgress && typeof progress === "number") {{
        jobProgress.style.width = `${{Math.max(0, Math.min(100, progress))}}%`;
      }}
    }};

    const pollJob = async () => {{
      if (!activeJobId) {{
        return;
      }}
      try {{
        const response = await fetch(`/jobs/${{activeJobId}}`);
        if (!response.ok) {{
          return;
        }}
        const data = await response.json();
        setJobStatus(`狀態：${{data.status}} · 進度：${{data.progress}}% · 步驟：${{data.last_step}}`, data.progress);
        if (jobOutput && data.output) {{
          jobOutput.textContent = data.output;
        }} else if (jobOutput) {{
          const outputResponse = await fetch(`/jobs/${{activeJobId}}/output`);
          if (outputResponse.ok) {{
            jobOutput.textContent = await outputResponse.text();
          }}
        }}
        if (data.status === "completed" || data.status === "failed") {{
          if (pollTimer) {{
            clearInterval(pollTimer);
          }}
        }}
      }} catch (error) {{
        console.warn(error);
      }}
    }};

    const startPolling = () => {{
      if (pollTimer) {{
        clearInterval(pollTimer);
      }}
      pollTimer = setInterval(pollJob, 3000);
    }};

    pipelineForm?.addEventListener("submit", async (event) => {{
      event.preventDefault();
      const formData = new FormData(pipelineForm);
      setJobStatus("任務啟動中…", 0);
      if (jobOutput) {{
        jobOutput.textContent = "等待輸出...";
      }}
      try {{
        const response = await fetch("/run", {{
          method: "POST",
          body: formData,
        }});
        const data = await response.json();
        if (!response.ok) {{
          setJobStatus(`啟動失敗：${{data.error || "未知錯誤"}}`, 0);
          return;
        }}
        activeJobId = data.job_id;
        setJobStatus(`任務已啟動：${{activeJobId}}`, 0);
        startPolling();
      }} catch (error) {{
        setJobStatus("啟動失敗，請檢查網路或伺服器狀態。", 0);
      }}
    }});

    uploadInput?.addEventListener("change", () => {{
      if (!uploadInput.files || uploadInput.files.length === 0) {{
        return;
      }}
      const file = uploadInput.files[0];
      if (file && (!pathInput.value || pathInput.value.trim() === "")) {{
        pathInput.value = file.name;
      }}
    }});

    validateFileInput?.addEventListener("change", () => {{
      if (!validateFileInput.files || validateFileInput.files.length === 0) {{
        return;
      }}
      const file = validateFileInput.files[0];
      if (file && validatePathInput && (!validatePathInput.value || validatePathInput.value.trim() === "")) {{
        validatePathInput.value = file.name;
      }}
    }});
  </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    jobs = job_manager.list_jobs()
    status = _ollama_status()
    models = _ollama_models()
    return _render_home(jobs, status, models)


@app.post("/run")
def run_job(
    input_path: str = Form(""),
    upload_file: UploadFile | None = File(None),
    output_path: str = Form(...),
    file_format: str = Form(...),
    model_name: str = Form(""),
    temperature: str = Form(""),
    timeout: str = Form(""),
    max_chunks: str = Form(""),
    dump_chunks: str = Form("false"),
    dump_path: str = Form(""),
    print_llm_output: str = Form("false"),
) -> JSONResponse:
    uploads_dir = pathlib.Path("data/uploads")
    uploads_dir.mkdir(parents=True, exist_ok=True)
    input_file: pathlib.Path
    if upload_file is not None and upload_file.filename:
        target = uploads_dir / upload_file.filename
        content = upload_file.file.read()
        target.write_bytes(content)
        input_file = target
        input_path = str(target)
    else:
        if not input_path:
            return JSONResponse({"error": "No input file provided."}, status_code=400)
        input_file = pathlib.Path(input_path)
        if not input_file.exists():
            return JSONResponse(
                {"error": f"Input file not found: {input_path}"}, status_code=400
            )
    job = job_manager.create_job(input_path, output_path, file_format)
    config = load_config()
    debug_cfg = config.get("debug", {})
    dump_chunks_value = dump_chunks.lower() == "true"
    print_llm_output_value = print_llm_output.lower() == "true"
    dump_path_value = dump_path or debug_cfg.get("dump_path", "")
    max_chunks_value = int(max_chunks) if max_chunks.strip() else debug_cfg.get("max_chunks", 0)
    temperature_value = float(temperature) if temperature.strip() else None
    timeout_value = int(timeout) if timeout.strip() else None
    model_name_value = model_name.strip() or None
    job_manager.run_in_thread(
        job.job_id,
        run_pipeline,
        pathlib.Path(input_path),
        pathlib.Path(output_path),
        lambda msg: job_manager.append_log(job.job_id, msg),
        lambda progress, step: job_manager.update_job(
            job.job_id, progress=progress, last_step=step
        ),
        dump_chunks_value,
        pathlib.Path(dump_path_value) if dump_path_value else None,
        max_chunks_value,
        model_name_value,
        temperature_value,
        timeout_value,
        print_llm_output_value,
    )
    return JSONResponse(
        {"job_id": job.job_id, "status": "started"},
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


@app.post("/validate")
def validate_output(
    validate_path: str = Form(""),
    validate_file: UploadFile | None = File(None),
) -> HTMLResponse:
    uploads_dir = pathlib.Path("data/uploads")
    uploads_dir.mkdir(parents=True, exist_ok=True)
    path: pathlib.Path
    if validate_file is not None and validate_file.filename:
        target = uploads_dir / validate_file.filename
        content = validate_file.file.read()
        target.write_bytes(content)
        path = target
    else:
        if not validate_path:
            return HTMLResponse("<p>No validation file provided.</p>", status_code=400)
        path = pathlib.Path(validate_path)
        if not path.exists():
            return HTMLResponse("<p>Validation file not found.</p>", status_code=400)
    try:
        rate = run_validation(path)
    except Exception as exc:
        return HTMLResponse(f"<p>Validation failed: {exc}</p>", status_code=400)
    return HTMLResponse(
        f"<p>Validation complete. Hallucination rate: {rate}</p><p><a href='/'>Back</a></p>",
        status_code=200,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="PrimeArchive admin UI")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
