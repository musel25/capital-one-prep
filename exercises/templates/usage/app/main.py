from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .models import Month, UsageEvent
from .events import EventFeed
from .billing import bill


def create_app():
    app = FastAPI(title='Meter Trail - fictional practice')
    feed = EventFeed()
    static = Path(__file__).parent / 'static'
    app.mount('/static', StaticFiles(directory=static), name='static')

    @app.get('/')
    def home():
        return FileResponse(static / 'index.html')

    @app.get('/health')
    def health():
        return {'status': 'ok'}

    @app.get('/api/workspaces')
    def workspaces():
        return {'items': feed.workspaces}

    @app.get('/api/events')
    def events():
        return {'items': feed.events}

    @app.post('/api/events', status_code=201)
    def ingest(request: UsageEvent):
        return feed.append(request)

    @app.get('/api/workspaces/{workspace_id}/bill')
    def invoice(workspace_id: str, month: Month):
        return bill(feed, workspace_id, month)

    return app


app = create_app()
