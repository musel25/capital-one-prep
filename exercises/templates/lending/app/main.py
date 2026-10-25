from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .inventory import Library
from .loans import checkout, find_loan
from .models import LoanRequest
from .returns import accept_return


def create_app():
    app = FastAPI(title='Field Kit Library — fictional practice')
    library = Library()
    static = Path(__file__).parent / 'static'
    app.mount('/static', StaticFiles(directory=static), name='static')

    @app.get('/')
    def home():
        return FileResponse(static / 'index.html')

    @app.get('/health')
    def health():
        return {'status': 'ok'}

    @app.get('/api/equipment')
    def equipment():
        return {'items': list(library.equipment.values())}

    @app.get('/api/loans')
    def loans():
        return {'items': list(library.loans.values())}

    @app.get('/api/loans/{loan_id}')
    def loan(loan_id: str):
        return find_loan(library, loan_id)

    @app.post('/api/loans', status_code=201)
    def borrow(request: LoanRequest):
        return checkout(library, request)

    @app.post('/api/loans/{loan_id}/return')
    def return_loan(loan_id: str):
        return accept_return(library, loan_id)

    return app


app = create_app()
