from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .directory import Directory
from .models import ContactRequest, ImportRequest
from .registration import register
from .importing import import_contacts


def create_app():
    app = FastAPI(title='Gather Directory - fictional practice')
    directory = Directory()
    static = Path(__file__).parent / 'static'
    app.mount('/static', StaticFiles(directory=static), name='static')

    @app.get('/')
    def home():
        return FileResponse(static / 'index.html')

    @app.get('/health')
    def health():
        return {'status': 'ok'}

    @app.get('/api/contacts')
    def contacts():
        return {'items': directory.contacts}

    @app.get('/api/contacts/{contact_id}')
    def contact(contact_id: str):
        return directory.find(contact_id)

    @app.post('/api/contacts', status_code=201)
    def create(request: ContactRequest):
        return register(directory, request)

    @app.post('/api/imports', status_code=201)
    def batch(request: ImportRequest):
        return import_contacts(directory, request)

    return app


app = create_app()
