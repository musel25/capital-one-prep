def select_tickets(store, team, status):
    rows = [t for t in store.ticket_snapshot() if t['team'] == team and t['status'] == status]
    return sorted(rows, key=lambda t: (t['priority'], t['id']))


def text_search(store, query):
    needle = query.casefold().strip()
    return {'items': [t for t in store.ticket_snapshot() if needle in t['title'].casefold()]}
