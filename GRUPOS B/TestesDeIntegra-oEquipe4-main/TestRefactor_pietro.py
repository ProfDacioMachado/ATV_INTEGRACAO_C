import unittest
from unittest.mock import MagicMock
from relatorio_service import RelatorioService, DadosEmprestimo, DadosUsuario

class TestPietroRelatorios(unittest.TestCase):

    def setUp(self):
        self.mock_repo = MagicMock()
        self.mock_repo.getAllEmprestimos.return_value = [
            DadosEmprestimo(1, 101, '2025-01-01'),
            DadosEmprestimo(1, 102, '2025-01-05'),
            DadosEmprestimo(1, 103, '2025-03-01'),
            DadosEmprestimo(2, 104, '2025-02-10'),
        ]
        self.mock_repo.getUsuario.side_effect = lambda id: DadosUsuario(id, f"Usuario {id}")
        self.service = RelatorioService(repositorio=self.mock_repo)

    def test_gerar_relatorio_usuarios_mais_ativos_sucesso(self):
        relatorio = self.service.gerar_relatorio_usuarios_mais_ativos()
        self.assertEqual(relatorio[0]['matricula'], 1) 
        self.assertEqual(relatorio[0]['totalEmprestimos'], 3)
        
    def test_gerar_relatorio_usuarios_mais_ativos_zero_emprestimos(self):
        self.mock_repo.getAllEmprestimos.return_value = []
        relatorio = self.service.gerar_relatorio_usuarios_mais_ativos()
        self.assertEqual(relatorio, [])

    def test_contrato_dados_usuario(self):
        usuario_mock = self.mock_repo.getUsuario(99)
        self.assertTrue(hasattr(usuario_mock, 'nome'))
        self.assertTrue(hasattr(usuario_mock, 'matricula'))

if __name__ == '__main__':
    unittest.main(verbosity=2)