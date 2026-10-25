from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .ledger import Ledger
from .models import ExpenseRequest, Month
from .summaries import employee_summary


def create_app():
    app = FastAPI(title='Fieldwork Expenses - fictional practice')
    ledger = Ledger()
    static = Path(__file__).parent / 'static'
    app.mount('/static', StaticFiles(directory=static), name='static')

    @app.get('/')
    def home():
        return FileResponse(static / 'index.html')

    @app.get('/health')
    def health():
        return {'status': 'ok'}

    @app.get('/api/employees')
    def employees():
        return {'items': ledger.employees}

    @app.get('/api/expenses')
    def expenses():
        return {'items': ledger.expenses}

    @app.post('/api/expenses', status_code=201)
    def submit(request: ExpenseRequest):
        return ledger.submit(request)

    @app.get('/api/employees/{employee_id}/summary')
    def summary(employee_id: str, month: Month):
        return employee_summary(ledger, employee_id, month)

    return app


app = create_app()
