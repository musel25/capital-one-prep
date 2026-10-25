from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .models import QuoteRequest
from .rates import RATES, rate_for
from .quotes import quote


def create_app():
    app = FastAPI(title='Parcel Lane — fictional practice')
    static = Path(__file__).parent / 'static'
    app.mount('/static', StaticFiles(directory=static), name='static')

    @app.get('/')
    def home():
        return FileResponse(static / 'index.html')

    @app.get('/health')
    def health():
        return {'status': 'ok'}

    @app.get('/api/rates')
    def rates():
        return {'items': list(RATES.values())}

    @app.get('/api/rates/{zone}')
    def rate_detail(zone: str):
        return rate_for(zone)

    @app.post('/api/quotes')
    def shipping_quote(request: QuoteRequest):
        return quote(request)

    return app


app = create_app()
