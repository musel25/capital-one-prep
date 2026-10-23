from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .models import Reservation
from .store import Store
from . import service


def create_app():
    app = FastAPI(title='Harbor Supply — fictional practice')
    store = Store()
    static = Path(__file__).parent / 'static'
    app.mount('/static', StaticFiles(directory=static), name='static')

    @app.get('/')
    def home():
        return FileResponse(static / 'index.html')

    @app.get('/health')
    def health():
        return {'status': 'ok'}

    @app.get('/api/products')
    def products():
        return {'items': list(store.products.values())}

    @app.get('/api/reservations')
    def reservations():
        return {'items': list(store.reservations.values())}

    @app.post('/api/reservations', status_code=201)
    def reserve(request: Reservation):
        return service.reserve(store, request)

    @app.post('/api/reservations/{reservation_id}/cancel')
    def cancel(reservation_id: str):
        return service.cancel(store, reservation_id)

    return app


app = create_app()
