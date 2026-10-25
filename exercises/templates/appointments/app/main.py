from datetime import date
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .calendar import Calendar
from .models import BookingRequest
from . import scheduling


def create_app():
    app = FastAPI(title='Juniper Appointments - fictional practice')
    calendar = Calendar()
    static = Path(__file__).parent / 'static'
    app.mount('/static', StaticFiles(directory=static), name='static')

    @app.get('/')
    def home():
        return FileResponse(static / 'index.html')

    @app.get('/health')
    def health():
        return {'status': 'ok'}

    @app.get('/api/providers')
    def providers():
        return {'items': calendar.providers}

    @app.get('/api/bookings')
    def bookings():
        return {'items': calendar.bookings}

    @app.post('/api/bookings', status_code=201)
    def book(request: BookingRequest):
        return scheduling.book(calendar, request)

    @app.get('/api/availability')
    def availability(provider_id: str, on: date, duration_minutes: int = Query(30)):
        if duration_minutes not in (30, 60):
            raise HTTPException(422, 'Duration must be 30 or 60 minutes')
        return scheduling.availability(calendar, provider_id, on, duration_minutes)

    return app


app = create_app()
