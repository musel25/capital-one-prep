from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .repository import Store
from .routes import api


def create_app():
    app = FastAPI(title='Atlas Support Operations — fictional practice')
    static = Path(__file__).parent / 'static'
    app.mount('/static', StaticFiles(directory=static), name='static')
    app.include_router(api(Store()))

    @app.get('/health')
    def health():
        return {'status': 'ok'}

    @app.get('/')
    def home():
        return FileResponse(static / 'index.html')

    return app


app = create_app()
