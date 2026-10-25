from fastapi import HTTPException


class Catalog:
    def __init__(self):
        self.books = {book['id']: book for book in [
            {'id': 'b-05', 'title': 'Earth in Motion', 'author': 'Morgan Lake', 'genre': 'science', 'available': True},
            {'id': 'b-02', 'title': 'Borrowed Summer', 'author': 'Terry Lane', 'genre': 'fiction', 'available': True},
            {'id': 'b-07', 'title': 'Field Notes', 'author': 'Remy Park', 'genre': 'science', 'available': True},
            {'id': 'b-01', 'title': 'A Brief Atlas', 'author': 'Morgan Lake', 'genre': 'science', 'available': True},
            {'id': 'b-06', 'title': 'Field Notes', 'author': 'Casey Reed', 'genre': 'history', 'available': True},
            {'id': 'b-04', 'title': 'Distant Harbor', 'author': 'Terry Lane', 'genre': 'fiction', 'available': True},
            {'id': 'b-03', 'title': 'Cells and Signals', 'author': 'Remy Park', 'genre': 'science', 'available': False},
        ]}
        self.loans = []

    def get_book(self, book_id):
        if book_id not in self.books:
            raise HTTPException(404, 'Book not found')
        return self.books[book_id]
