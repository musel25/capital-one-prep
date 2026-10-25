from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .delivery import receive
from .inbox import Inbox
from .models import DeliveryEvent


def create_app():
    app = FastAPI(title='Parcel Signal — fictional practice')
    inbox = Inbox()
    static = Path(__file__).parent / 'static'
    app.mount('/static', StaticFiles(directory=static), name='static')

    @app.get('/')
    def home():
        return FileResponse(static / 'index.html')

    @app.get('/health')
    def health():
        return {'status': 'ok'}

    @app.get('/api/parcels')
    def parcels():
        return {'items': list(inbox.parcels.values())}

    @app.get('/api/deliveries')
    def deliveries():
        return {'items': [receipt['result'] for receipt in inbox.receipts.values()]}

    @app.post('/api/deliveries')
    def deliver(event: DeliveryEvent):
        return receive(inbox, event)

    @app.get('/api/notifications')
    def notifications():
        return {'items': inbox.notifications}

    return app


app = create_app()
