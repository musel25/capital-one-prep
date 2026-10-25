from pathlib import Path
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .catalog import Catalog
from .models import LoanRequest
from .search import browse
from .circulation import borrow


def create_app():
    app = FastAPI(title='Maple Library — fictional practice')
    catalog = Catalog()
    static = Path(__file__).parent / 'static'
    app.mount('/static', StaticFiles(directory=static), name='static')

    @app.get('/')
    def home():
        return FileResponse(static / 'index.html')

    @app.get('/health')
    def health():
        return {'status': 'ok'}

    @app.get('/api/books')
    def books(genre: str | None = None, available_only: bool = False,
              page: int = Query(1, ge=1), page_size: int = Query(3, ge=1, le=20)):
        return browse(catalog, genre, available_only, page, page_size)

    @app.get('/api/books/{book_id}')
    def book_detail(book_id: str):
        return catalog.get_book(book_id)

    @app.get('/api/loans')
    def loans():
        return {'items': catalog.loans}

    @app.post('/api/loans', status_code=201)
    def checkout(request: LoanRequest):
        return borrow(catalog, request)

    return app


app = create_app()
