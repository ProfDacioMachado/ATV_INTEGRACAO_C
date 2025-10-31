class BookStoreMock:
    """
    Mock simples de Catálogo: mantém um dict book_id -> dict(info).
    Campos: 'title', 'loaned' (bool)
    Interface mínima:
      - add(book_id, title)
      - exists(book_id) -> bool
      - is_available(book_id) -> bool
      - set_loaned(book_id, True/False)
      - get(book_id) -> dict
    """
    def __init__(self):
        self._books = {}

    def add(self, book_id: int, title: str):
        self._books[book_id] = {"title": title, "loaned": False}

    def exists(self, book_id: int) -> bool:
        return book_id in self._books

    def is_available(self, book_id: int) -> bool:
        if not self.exists(book_id):
            raise KeyError("Book not found")
        return not self._books[book_id]["loaned"]

    def set_loaned(self, book_id: int, loaned: bool):
        if not self.exists(book_id):
            raise KeyError("Book not found")
        self._books[book_id]["loaned"] = bool(loaned)

    def get(self, book_id: int):
        return self._books.get(book_id)