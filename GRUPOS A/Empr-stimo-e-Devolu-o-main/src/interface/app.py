from flask import Flask, render_template, jsonify
from emprestimo.service import LoanService


# Mock services para desenvolvimento/testes
class MockUserService:
    def __init__(self):
        self.users = {
            1: {"id": 1, "name": "Alice", "active": True},
            2: {"id": 2, "name": "Bob", "active": True},
        }
    
    def get_user(self, user_id: int):
        return self.users.get(user_id)
    
    def is_active(self, user_id: int) -> bool:
        user = self.users.get(user_id)
        return user.get("active", False) if user else False


class MockCatalogService:
    def __init__(self):
        self.books = {
            1: {"id": 1, "title": "1984", "available": True},
            2: {"id": 2, "title": "Dom Casmurro", "available": True},
        }
    
    def get_book(self, book_id: int):
        return self.books.get(book_id)
    
    def is_available(self, book_id: int) -> bool:
        book = self.books.get(book_id)
        return book.get("available", False) if book else False
    
    def mark_loaned(self, book_id: int):
        if book_id in self.books:
            self.books[book_id]["available"] = False
    
    def mark_available(self, book_id: int):
        if book_id in self.books:
            self.books[book_id]["available"] = True


app = Flask(__name__, template_folder="templates", static_folder="static")

# Inicializar serviço com dependências
user_service = MockUserService()
catalog_service = MockCatalogService()
service = LoanService(user_service, catalog_service)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/emprestimos")
def emprestimos():
    return render_template("emprestimo.html")


@app.route("/devolucoes")
def devolucoes():
    return render_template("devolucoes.html")


@app.route("/api/loans")
def get_loans():
    loans = service.list_loans()
    return jsonify(loans)


@app.route("/api/loans/<int:loan_id>/return", methods=["POST"])
def return_loan(loan_id):
    result = service.return_book(loan_id)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)