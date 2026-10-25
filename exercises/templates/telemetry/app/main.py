from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .samples import Samples
from .models import ReadingRequest
from .overview import summary
from .representation import reading


def create_app():
    app = FastAPI(title='Pulse Window - fictional practice')
    samples = Samples()
    static = Path(__file__).parent / 'static'
    app.mount('/static', StaticFiles(directory=static), name='static')

    @app.get('/')
    def home():
        return FileResponse(static / 'index.html')

    @app.get('/health')
    def health():
        return {'status': 'ok'}

    @app.get('/api/services')
    def services():
        return {'items': samples.services}

    @app.get('/api/services/{service_id}/readings')
    def readings(service_id: str):
        return {'items': [reading(row) for row in samples.for_service(service_id)]}

    @app.post('/api/readings', status_code=201)
    def collect(request: ReadingRequest):
        return reading(samples.collect(request))

    @app.get('/api/services/{service_id}/summary')
    def overview(service_id: str):
        return summary(samples, service_id)

    return app


app = create_app()
