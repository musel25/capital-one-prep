def page_of(rows, page, page_size):
    start = (page - 1) * page_size
    return {'items': rows[start:start + page_size], 'total': len(rows),
            'has_next': start + page_size < len(rows)}
