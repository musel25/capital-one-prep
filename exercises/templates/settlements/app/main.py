from datetime import date
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .store import Store
from . import service


def create_app():
    app = FastAPI(title='Fern Merchant Operations — fictional practice')
    store = Store()
    static = Path(__file__).parent / 'static'
    app.mount('/static', StaticFiles(directory=static), name='static')

    @app.get('/')
    def home():
        return FileResponse(static / 'index.html')

    @app.get('/health')
    def health():
        return {'status': 'ok'}

    @app.get('/api/charges')
    def charges():
        return {'items': store.charges}

    @app.get('/api/settlements')
    def settlements(merchant_id: str):
        return {'items': service.eligible(store, merchant_id)}

    @app.get('/api/merchants/{merchant_id}/summary')
    def summary(merchant_id: str, on: date):
        return service.summary(store, merchant_id, on)

    return app


app = create_app()
