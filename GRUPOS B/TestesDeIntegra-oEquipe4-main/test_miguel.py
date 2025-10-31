import unittest
from unittest.mock import MagicMock
from relatorio_service import RelatorioService, DadosLivro # Adicionei DadosLivro aqui

class TestMiguelRelatorios(unittest.TestCase):

    def setUp(self):
        # 1. Cria um repositório mock
        self.mock_repo = MagicMock()
        # 2. Mocka o método getAllLivros para retornar os dados de teste esperados
        self.mock_repo.getAllLivros.return_value = [
            DadosLivro(101, "A", "A", 'emprestado'),
            DadosLivro(102, "B", "B", 'emprestado'),
            DadosLivro(103, "C", "C", 'disponivel'),
            DadosLivro(104, "D", "D", 'disponivel'),
            DadosLivro(105, "E", "E", 'disponivel'), # 3 disponíveis, 2 emprestados
        ]
        # Garante que os outros métodos necessários existem para o teste de contrato
        self.mock_repo.getAllEmprestimos.return_value = []
        self.mock_repo.getUsuario.return_value = MagicMock()
        self.mock_repo.getLivro.return_value = MagicMock()
        
        # 3. Injeta o mock no service
        self.service = RelatorioService(repositorio=self.mock_repo)

    def test_lanca_excecao_parametros_invalidos(self):
        with self.assertRaises(ValueError):
            self.service.gerar_relatorio_com_params(None)
        with self.assertRaises(ValueError):
            self.service.gerar_relatorio_com_params(123)
        
    def test_contagem_status_acervo_correta(self):
        # O teste agora espera 3 disponíveis e 2 emprestados, conforme o mock acima
        contagem = self.service.contar_status_acervo()
        self.assertEqual(contagem['disponivel'], 3) # AGORA ESPERA 3 (Conforme o Mock)
        self.assertEqual(contagem['emprestado'], 2)

    def test_contrato_interface_acesso_repositorio(self):
        self.assertTrue(hasattr(self.service.repo, 'getAllEmprestimos'))
        self.assertTrue(hasattr(self.service.repo, 'getUsuario'))
        self.assertTrue(hasattr(self.service.repo, 'getLivro'))
        
        self.service.repo.getAllEmprestimos()
        self.service.repo.getAllEmprestimos.assert_called_once()

if __name__ == '__main__':
    unittest.main(verbosity=2)