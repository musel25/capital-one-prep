def matching(books, genre, available_only):
    return [book for book in books if (genre is None or book['genre'] == genre)
            and (not available_only or book['available'])]


def browse(catalog, genre, available_only, page, page_size):
    start = (page - 1) * page_size
    ordered = sorted(matching(catalog.books.values(), genre, available_only),
                     key=lambda book: (book['title'].casefold(), book['id']))
    total = len(ordered)
    return {'items': ordered[start:start + page_size], 'total': total, 'page': page,
            'page_size': page_size, 'has_next': start + page_size < total}
