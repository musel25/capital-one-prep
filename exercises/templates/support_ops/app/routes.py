from copy import deepcopy
from typing import Literal
from fastapi import APIRouter, Query
from .models import AssignmentRequest, CommentRequest, StatusRequest
from .assignments import assign_many
from .events import history
from .reporting import overview, queue_report
from .search import text_search
from .tickets import change_status, comment


def api(store):
    router = APIRouter(prefix='/api')

    @router.get('/tickets')
    def tickets():
        return {'items': store.ticket_snapshot()}

    @router.get('/tickets/search')
    def search(q: str = ''):
        return text_search(store, q)

    @router.get('/tickets/{ticket_id}')
    def ticket(ticket_id: str):
        return deepcopy(store.ticket(ticket_id))

    @router.get('/agents')
    def agents():
        return {'items': deepcopy(list(store.agents.values()))}

    @router.get('/queues')
    def queues(team: Literal['platform', 'support'] = 'platform',
               status: Literal['open', 'resolved'] = 'open',
               page: int = Query(1, ge=1), page_size: int = Query(2, ge=1, le=20)):
        return queue_report(store, team, status, page, page_size)

    @router.get('/overview')
    def summary():
        return overview(store)

    @router.get('/events')
    def events():
        return history(store)

    @router.get('/tickets/{ticket_id}/events')
    def ticket_events(ticket_id: str):
        return history(store, ticket_id)

    @router.post('/tickets/{ticket_id}/comments', status_code=201)
    def add_comment(ticket_id: str, request: CommentRequest):
        return comment(store, ticket_id, request)

    @router.post('/tickets/{ticket_id}/status')
    def status(ticket_id: str, request: StatusRequest):
        return change_status(store, ticket_id, request)

    @router.post('/assignments')
    def assignments(request: AssignmentRequest):
        return assign_many(store, request)

    return router
