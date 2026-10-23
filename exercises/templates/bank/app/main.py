from pathlib import Path
from typing import Annotated
from fastapi import FastAPI, Header, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .models import Event, Transfer
from .store import Store
from . import service

Month = Annotated[str, Query(pattern=r'^\d{4}-(0[1-9]|1[0-2])$')]


def create_app():
    app = FastAPI(title='Cedar Wallet — fictional practice app')
    store = Store()
    static = Path(__file__).parent / 'static'
    app.mount('/static', StaticFiles(directory=static), name='static')

    @app.get('/')
    def home():
        return FileResponse(static / 'index.html')

    @app.get('/health')
    def health():
        return {'status': 'ok'}

    @app.get('/api/accounts')
    def accounts():
        return service.accounts(store)

    @app.get('/api/transactions')
    def transactions(category: str | None = None, min_cents: Annotated[int | None, Query(ge=0)] = None,
                     page: Annotated[int, Query(ge=1)] = 1, page_size: Annotated[int, Query(ge=1, le=100)] = 50):
        return service.transaction_page(store, category, min_cents, page, page_size)

    @app.post('/api/transfers', status_code=201)
    def transfer(request: Transfer, idempotency_key: Annotated[str | None, Header()] = None):
        return service.transfer_with_key(store, request, idempotency_key)

    @app.get('/api/accounts/{account}/history')
    def history(account: str):
        return service.history(store, account)

    @app.get('/api/cashback')
    def cashback(month: Month, cap_cents: Annotated[int | None, Query(ge=0)] = None):
        return service.cashback(store, month, cap_cents)

    @app.get('/api/spend')
    def spend(month: Month):
        return service.spend(store, month)

    @app.get('/api/spend/categories')
    def categories(month: Month):
        return service.categories(store, month)

    @app.post('/api/events')
    def event(request: Event):
        return service.accept_event(store, request)

    return app


app = create_app()
