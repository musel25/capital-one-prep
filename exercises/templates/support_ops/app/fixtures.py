"""Fictional support data; every app instance receives its own copy."""
TICKETS = [
    {'id': 't-1', 'title': 'Build runner unavailable', 'team': 'platform', 'status': 'open', 'priority': 1, 'assignee': None},
    {'id': 't-2', 'title': 'Monitor adapter request', 'team': 'support', 'status': 'open', 'priority': 2, 'assignee': None},
    {'id': 't-3', 'title': 'Archive permission restored', 'team': 'platform', 'status': 'resolved', 'priority': 2, 'assignee': 'a-1'},
    {'id': 't-4', 'title': 'CI credentials rotation', 'team': 'platform', 'status': 'open', 'priority': 3, 'assignee': None},
]
AGENTS = [
    {'id': 'a-1', 'name': 'Alex', 'team': 'platform', 'active': True},
    {'id': 'a-2', 'name': 'Rae', 'team': 'support', 'active': True},
    {'id': 'a-3', 'name': 'Sam', 'team': 'platform', 'active': False},
]
