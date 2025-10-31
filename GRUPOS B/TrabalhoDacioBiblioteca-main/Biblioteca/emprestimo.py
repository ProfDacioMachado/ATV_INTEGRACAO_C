from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional

class LoanError(Exception):
    pass

class NotFoundError(LoanError):
    pass

class ValidationError(LoanError):
    pass

@dataclass
class Loan:
    loan_id: int
    user_id: int
    book_id: int
    borrowed_at: datetime
    returned_at: Optional[datetime] = None

    def to_dict(self):
        d = asdict(self)
        d["borrowed_at"] = self.borrowed_at.isoformat()
        d["returned_at"] = self.returned_at.isoformat() if self.returned_at else None
        return d

class LoanController:

    def __init__(self, user_store, book_store):
        self.user_store = user_store
        self.book_store = book_store
        self._loans: Dict[int, Loan] = {}
        self._next_id = 1

    def _validate_ids(self, user_id: int, book_id: int):
        if not isinstance(user_id, int) or not isinstance(book_id, int):
            raise ValidationError("IDs devem ser inteiros")
        if user_id <= 0 or book_id <= 0:
            raise ValidationError("IDs devem ser positivos")
        if not self.user_store.exists(user_id):
            raise NotFoundError("Usuário não encontrado")
        if not self.book_store.exists(book_id):
            raise NotFoundError("Livro não encontrado")

    def verificar_disponibilidade(self, book_id: int) -> bool:
        if not isinstance(book_id, int):
            raise ValidationError("book_id deve ser inteiro")
        if not self.book_store.exists(book_id):
            raise NotFoundError("Livro não encontrado")
        return self.book_store.is_available(book_id)

    def registrar_emprestimo(self, user_id: int, book_id: int) -> Loan:
        self._validate_ids(user_id, book_id)
        if not self.book_store.is_available(book_id):
            raise LoanError("Livro não disponível para empréstimo")
        loan = Loan(
            loan_id=self._next_id,
            user_id=user_id,
            book_id=book_id,
            borrowed_at=datetime.utcnow()
        )
        self._loans[self._next_id] = loan
        self._next_id += 1
        self.book_store.set_loaned(book_id, True)
        return loan

    def registrar_devolucao(self, user_id: int, book_id: int) -> Loan:
        self._validate_ids(user_id, book_id)
        for loan in self._loans.values():
            if loan.user_id == user_id and loan.book_id == book_id and loan.returned_at is None:
                loan.returned_at = datetime.utcnow()
                self.book_store.set_loaned(book_id, False)
                return loan
        raise LoanError("Empréstimo ativo não encontrado para devolução")

    def listar_emprestimos(self) -> List[Loan]:
        return list(self._loans.values())

    def obter_emprestimo(self, loan_id: int) -> Loan:
        if loan_id not in self._loans:
            raise NotFoundError("Empréstimo não encontrado")
        return self._loans[loan_id]

    def _clear_all(self):
        self._loans.clear()
        self._next_id = 1