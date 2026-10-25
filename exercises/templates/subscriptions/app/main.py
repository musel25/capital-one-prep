from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .accounts import Accounts, find_subscription
from .catalog import PLANS
from .models import QuoteRequest
from .pricing import quote


def create_app():
    app = FastAPI(title='Plan Studio — fictional practice')
    accounts = Accounts()
    static = Path(__file__).parent / 'static'
    app.mount('/static', StaticFiles(directory=static), name='static')

    @app.get('/')
    def home():
        return FileResponse(static / 'index.html')

    @app.get('/health')
    def health():
        return {'status': 'ok'}

    @app.get('/api/plans')
    def plans():
        return {'items': list(PLANS.values())}

    @app.get('/api/subscriptions')
    def subscriptions():
        return {'items': list(accounts.subscriptions.values())}

    @app.get('/api/subscriptions/{subscription_id}')
    def subscription(subscription_id: str):
        return find_subscription(accounts, subscription_id)

    @app.post('/api/subscriptions/{subscription_id}/quote')
    def preview(subscription_id: str, request: QuoteRequest):
        return quote(accounts, subscription_id, request)

    return app


app = create_app()
