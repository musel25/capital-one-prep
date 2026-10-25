from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .models import Comment, StatusChange
from .store import Store
from . import tickets
from .timeline import timeline


def create_app():
    app = FastAPI(title='Lantern Desk — fictional practice')
    store = Store()
    static = Path(__file__).parent / 'static'
    app.mount('/static', StaticFiles(directory=static), name='static')

    @app.get('/')
    def home():
        return FileResponse(static / 'index.html')

    @app.get('/health')
    def health():
        return {'status': 'ok'}

    @app.get('/api/tickets')
    def ticket_list():
        return {'items': list(store.tickets.values())}

    @app.get('/api/tickets/{ticket_id}')
    def ticket_detail(ticket_id: str):
        return tickets.get_ticket(store, ticket_id)

    @app.post('/api/tickets/{ticket_id}/comments', status_code=201)
    def comment(ticket_id: str, request: Comment):
        return tickets.add_comment(store, ticket_id, request)

    @app.post('/api/tickets/{ticket_id}/status')
    def status(ticket_id: str, request: StatusChange):
        return tickets.change_status(store, ticket_id, request)

    @app.get('/api/tickets/{ticket_id}/timeline')
    def activity(ticket_id: str):
        return timeline(store, ticket_id)

    return app


app = create_app()
