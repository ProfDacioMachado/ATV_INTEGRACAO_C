import unittest
from unittest.mock import MagicMock
from relatorio_service import RelatorioService, DadosEmprestimo

class TestFabricioRelatorios(unittest.TestCase):

    def setUp(self):
        self.mock_repo = MagicMock()
        self.mock_repo.getAllEmprestimos.return_value = [
            DadosEmprestimo(1, 101, '2025-01-01'),
            DadosEmprestimo(2, 101, '2025-01-05'),
            DadosEmprestimo(3, 101, '2025-03-01'),
            DadosEmprestimo(4, 102, '2025-02-10'),
            DadosEmprestimo(5, 102, '2025-02-15'),
            DadosEmprestimo(6, 103, '2025-04-01'),
            DadosEmprestimo(7, 103, '2025-04-05'),
            DadosEmprestimo(8, 103, '2025-04-10'),
        ]
        self.mock_repo.getLivro.side_effect = lambda id: MagicMock(titulo=f"Livro {id}", autor="Autor X", id=id)
        self.service = RelatorioService(repositorio=self.mock_repo)

    def test_gerar_relatorio_livros_mais_emprestados_sucesso(self):
        relatorio = self.service.gerar_relatorio_livros_mais_emprestados()
        self.assertGreaterEqual(len(relatorio), 3)
        self.assertEqual(relatorio[0]['totalEmprestimos'], 3)
        self.assertEqual(relatorio[0]['titulo'], "Livro 101")
        
    def test_gerar_relatorio_livros_mais_emprestados_empates(self):
        relatorio = self.service.gerar_relatorio_livros_mais_emprestados()
        self.assertEqual(relatorio[0]['totalEmprestimos'], 3)
        self.assertEqual(relatorio[1]['totalEmprestimos'], 3)
        
    def test_contrato_dados_emprestimo(self):
        emprestimo_mock = self.mock_repo.getAllEmprestimos()[0]
        self.assertTrue(hasattr(emprestimo_mock, 'idUsuario'))
        self.assertTrue(hasattr(emprestimo_mock, 'idLivro'))
        self.assertTrue(hasattr(emprestimo_mock, 'dataEmprestimo'))

if __name__ == '__main__':
    unittest.main(verbosity=2)