import unittest
from unittest.mock import MagicMock
from relatorio_service import RelatorioService, DadosEmprestimo

class TestFabricioRelatorios(unittest.TestCase):

    def setUp(self):
        # Configurando o repositório mockado para garantir dados conhecidos
        self.mock_repo = MagicMock()
        self.mock_repo.getAllEmprestimos.return_value = [
            # Livro 1: 3 empréstimos (mais emprestado)
            DadosEmprestimo(1, 101, '2025-01-01'),
            DadosEmprestimo(2, 101, '2025-01-05'),
            DadosEmprestimo(3, 101, '2025-03-01'),
            # Livro 2: 2 empréstimos
            DadosEmprestimo(4, 102, '2025-02-10'),
            DadosEmprestimo(5, 102, '2025-02-15'),
            # Livro 3: 3 empréstimos (empate com Livro 1)
            DadosEmprestimo(6, 103, '2025-04-01'),
            DadosEmprestimo(7, 103, '2025-04-05'),
            DadosEmprestimo(8, 103, '2025-04-10'),
        ]
        self.mock_repo.getLivro.side_effect = lambda id: MagicMock(titulo=f"Livro {id}", autor="Autor X", id=id)
        self.service = RelatorioService(repositorio=self.mock_repo)

    # TU 1: Cálculo de Livros Mais Emprestados (Sucesso)
    def test_gerar_relatorio_livros_mais_emprestados_sucesso(self):
        relatorio = self.service.gerar_relatorio_livros_mais_emprestados()
        # O Livro 101 deve ser o primeiro ou o segundo, com 3 empréstimos
        self.assertGreaterEqual(len(relatorio), 3)
        self.assertEqual(relatorio[0]['totalEmprestimos'], 3)
        self.assertEqual(relatorio[0]['titulo'], "Livro 101")
        
    # TU 2: Cálculo de Livros Mais Emprestados (Empates)
    def test_gerar_relatorio_livros_mais_emprestados_empates(self):
        relatorio = self.service.gerar_relatorio_livros_mais_emprestados()
        # Verifica se Livro 101 e 103 estão entre os primeiros e têm o mesmo total
        self.assertEqual(relatorio[0]['totalEmprestimos'], 3)
        self.assertEqual(relatorio[1]['totalEmprestimos'], 3)
        
    # TC 1: Contrato de Dados de Empréstimo
    def test_contrato_dados_emprestimo(self):
        # Verifica se o objeto de empréstimo mockado (que simula a entrada da Equipe 3) 
        # possui os campos essenciais que o RelatorioService precisa.
        emprestimo_mock = self.mock_repo.getAllEmprestimos()[0]
        self.assertTrue(hasattr(emprestimo_mock, 'idUsuario'))
        self.assertTrue(hasattr(emprestimo_mock, 'idLivro'))
        self.assertTrue(hasattr(emprestimo_mock, 'dataEmprestimo'))

if __name__ == '__main__':
    unittest.main()