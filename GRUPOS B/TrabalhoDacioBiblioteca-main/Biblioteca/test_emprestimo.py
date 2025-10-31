import unittest
from emprestimo import LoanController, LoanError, NotFoundError, ValidationError
from usuario_mock import UserStoreMock
from livro_mock import BookStoreMock
from datetime import datetime
import time

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.users = UserStoreMock()
        self.books = BookStoreMock()
        self.users.add(1)
        self.users.add(2)
        self.books.add(10, "Livro A")
        self.books.add(20, "Livro B")
        self.controller = LoanController(self.users, self.books)
        self.controller._clear_all()

class TestLoanUnit(BaseTestCase):

    def test_successful_loan_changes_availability(self):
        loan = self.controller.registrar_emprestimo(1, 10)
        self.assertEqual(loan.user_id, 1)
        self.assertEqual(loan.book_id, 10)
        self.assertFalse(self.books.is_available(10))

    def test_cannot_loan_when_not_available(self):
        self.controller.registrar_emprestimo(1, 10)
        with self.assertRaises(LoanError):
            self.controller.registrar_emprestimo(2, 10)

    def test_successful_return_makes_available(self):
        self.controller.registrar_emprestimo(1, 10)
        ret = self.controller.registrar_devolucao(1, 10)
        self.assertIsNotNone(ret.returned_at)
        self.assertTrue(self.books.is_available(10))

    def test_return_without_active_loan_raises(self):
        with self.assertRaises(LoanError):
            self.controller.registrar_devolucao(1, 10)

    def test_nonexistent_user_raises(self):
        with self.assertRaises(NotFoundError):
            self.controller.registrar_emprestimo(999, 10)

    def test_nonexistent_book_raises(self):
        with self.assertRaises(NotFoundError):
            self.controller.registrar_emprestimo(1, 999)

    def test_ids_must_be_positive_integers(self):
        with self.assertRaises(ValidationError):
            self.controller.registrar_emprestimo(-1, 10)
        with self.assertRaises(ValidationError):
            self.controller.registrar_emprestimo(1, 0)
        with self.assertRaises(ValidationError):
            self.controller.registrar_emprestimo("a", 10)

    def test_listar_emprestimos_includes_active_and_returned(self):
        l1 = self.controller.registrar_emprestimo(1, 10)
        time.sleep(0.001)
        l2 = self.controller.registrar_emprestimo(2, 20)
        self.controller.registrar_devolucao(2, 20)
        all_loans = self.controller.listar_emprestimos()
        self.assertEqual(len(all_loans), 2)
        ids = [l.loan_id for l in all_loans]
        self.assertIn(l1.loan_id, ids)
        self.assertIn(l2.loan_id, ids)

    def test_same_user_cannot_loan_same_book_twice_without_return(self):
        self.controller.registrar_emprestimo(1, 10)
        with self.assertRaises(LoanError):
            self.controller.registrar_emprestimo(1, 10)

class TestLoanContracts(BaseTestCase):

    def test_loan_serialization_integrity(self):
        loan = self.controller.registrar_emprestimo(1, 10)
        d = loan.to_dict()
        for f in ["loan_id", "user_id", "book_id", "borrowed_at", "returned_at"]:
            self.assertIn(f, d)
        self.assertIsInstance(d["borrowed_at"], str)
        self.assertIsNone(d["returned_at"])

    def test_state_transition_available_to_loan_to_available(self):
        self.assertTrue(self.books.is_available(20))
        l = self.controller.registrar_emprestimo(2, 20)
        self.assertFalse(self.books.is_available(20))
        self.controller.registrar_devolucao(2, 20)
        self.assertTrue(self.books.is_available(20))

    def test_contract_field_types(self):
        loan = self.controller.registrar_emprestimo(1, 10)
        self.assertIsInstance(loan.loan_id, int)
        self.assertIsInstance(loan.user_id, int)
        self.assertIsInstance(loan.book_id, int)
        self.assertIsInstance(loan.borrowed_at, datetime)

    def test_bookstore_consistency_after_operations(self):
        self.controller.registrar_emprestimo(1, 10)
        self.assertFalse(self.books.get(10)["loaned"])
        self.controller.registrar_devolucao(1, 10)
        self.assertFalse(self.books.get(10)["loaned"])

    def test_multiple_loans_different_users_same_time(self):
        self.controller.registrar_emprestimo(1, 10)
        self.controller.registrar_emprestimo(2, 20)
        self.assertFalse(self.books.is_available(10))
        self.assertFalse(self.books.is_available(20))
        self.controller.registrar_devolucao(1, 10)
        self.controller.registrar_devolucao(2, 20)
        self.assertTrue(self.books.is_available(10))
        self.assertTrue(self.books.is_available(20))

if __name__ == "__main__":
    unittest.main()