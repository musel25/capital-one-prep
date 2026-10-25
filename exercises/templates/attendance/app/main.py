from datetime import date
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .reporting import daily_report
from .roster import MEMBERS
from .sessions import SessionLog, member_sessions


def create_app():
    app = FastAPI(title='Studio Attendance — fictional practice')
    log = SessionLog()
    static = Path(__file__).parent / 'static'
    app.mount('/static', StaticFiles(directory=static), name='static')

    @app.get('/')
    def home():
        return FileResponse(static / 'index.html')

    @app.get('/health')
    def health():
        return {'status': 'ok'}

    @app.get('/api/members')
    def members():
        return {'items': list(MEMBERS.values())}

    @app.get('/api/sessions')
    def sessions():
        return {'items': log.sessions}

    @app.get('/api/members/{member_id}/sessions')
    def visits(member_id: str):
        return {'items': member_sessions(log, member_id)}

    @app.get('/api/attendance')
    def report(on: date):
        return daily_report(log, on)

    return app


app = create_app()
