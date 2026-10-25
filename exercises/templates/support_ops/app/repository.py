from copy import deepcopy
from fastapi import HTTPException
from .fixtures import TICKETS, AGENTS


class Store:
    def __init__(self):
        self.tickets = {row['id']: deepcopy(row) for row in TICKETS}
        self.agents = {row['id']: deepcopy(row) for row in AGENTS}
        self.events = []
        self.queue_cache = {}

    def ticket(self, ticket_id):
        if ticket_id not in self.tickets:
            raise HTTPException(404, 'Ticket not found')
        return self.tickets[ticket_id]

    def agent(self, agent_id):
        if agent_id not in self.agents:
            raise HTTPException(404, 'Agent not found')
        return self.agents[agent_id]

    def ticket_snapshot(self):
        return deepcopy(list(self.tickets.values()))
