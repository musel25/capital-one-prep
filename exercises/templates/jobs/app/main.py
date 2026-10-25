from pathlib import Path

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .models import ExportRequest
from .registry import Registry
from .submission import submit


def create_app():
    app = FastAPI(title='Export Desk — fictional practice')
    registry = Registry()
    static = Path(__file__).parent / 'static'
    app.mount('/static', StaticFiles(directory=static), name='static')

    @app.get('/')
    def home():
        return FileResponse(static / 'index.html')

    @app.get('/health')
    def health():
        return {'status': 'ok'}

    @app.get('/api/datasets')
    def datasets():
        return {'items': list(registry.datasets.values())}

    @app.get('/api/jobs')
    def jobs():
        return {'items': list(registry.jobs.values())}

    @app.get('/api/jobs/{job_id}')
    def job(job_id: str):
        if job_id not in registry.jobs:
            raise HTTPException(404, 'Job not found')
        return registry.jobs[job_id]

    @app.post('/api/jobs', status_code=201)
    def create_job(request: ExportRequest, idempotency_key: str | None = Header(default=None)):
        return submit(registry, request, idempotency_key)

    return app


app = create_app()
