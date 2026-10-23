from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .models import Purchase
from . import rules


def create_app():
    app = FastAPI(title='Juniper Rewards — fictional practice')
    static = Path(__file__).parent / 'static'
    app.mount('/static', StaticFiles(directory=static), name='static')

    @app.get('/')
    def home():
        return FileResponse(static / 'index.html')

    @app.get('/health')
    def health():
        return {'status': 'ok'}

    @app.post('/api/eligibility')
    def eligibility(purchase: Purchase):
        return {'eligible': rules.eligible(purchase)}

    @app.post('/api/rewards/quote')
    def quote(purchase: Purchase):
        return rules.quote(purchase)

    return app


app = create_app()
