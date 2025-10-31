import unittest
from unittest.mock import MagicMock
from relatorio_service import RelatorioService

class TestMiguelRelatorios(unittest.TestCase):

    def setUp(self):
        self.mock_repo = MagicMock()
        self.service = RelatorioService(repositorio=self.mock_repo)

    # TU 9: Exceção de Parâmetros (Parâmetros Inválidos)
    def test_lanca_excecao_parametros_invalidos(self):
        with self.assertRaises(ValueError):
            self.service.gerar_relatorio_com_params(None)
        with self.assertRaises(ValueError):
            self.service.gerar_relatorio_com_params(123)
        
    # TU 10: Contagem de Livros Disponíveis vs. Emprestados (Novo Relatório)
    def test_contagem_status_acervo_correta(self):
        # 2 emprestados, 2 disponíveis (vindo do mock padrão do service)
        contagem = self.service.contar_status_acervo()
        self.assertEqual(contagem['disponivel'], 2)
        self.assertEqual(contagem['emprestado'], 2)

    # TC 5: Contrato de Acesso a Repositório
    def test_contrato_interface_acesso_repositorio(self):
        # Verifica se o repositório possui o método que a camada de Serviço espera
        self.assertTrue(hasattr(self.service.repo, 'getAllEmprestimos'))
        self.assertTrue(hasattr(self.service.repo, 'getUsuario'))
        self.assertTrue(hasattr(self.service.repo, 'getLivro'))
        
        # Testando se o método pode ser chamado
        self.service.repo.getAllEmprestimos()
        self.service.repo.getAllEmprestimos.assert_called_once()

if __name__ == '__main__':
    unittest.main()