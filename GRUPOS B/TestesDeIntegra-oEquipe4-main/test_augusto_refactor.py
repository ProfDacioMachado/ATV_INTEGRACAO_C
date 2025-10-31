import unittest
from unittest.mock import MagicMock
from relatorio_service import RelatorioService

class TestAugustoRelatorios(unittest.TestCase):

    def setUp(self):
        self.mock_repo = MagicMock()
        self.service = RelatorioService(repositorio=self.mock_repo)
        self.dados_exemplo = [{'id': 1, 'nome': 'Teste'}]

    def test_formatacao_relatorio_segue_schema(self):
        relatorio_formatado = self.service.formatar_relatorio(self.dados_exemplo)
        self.assertIsInstance(relatorio_formatado, dict)
        self.assertIn('relatorio', relatorio_formatado)
        self.assertEqual(relatorio_formatado['relatorio'], self.dados_exemplo)

    def test_geracao_relatorio_vazio(self):
        self.mock_repo.getAllEmprestimos.return_value = []
        relatorio = self.service.gerar_relatorio_livros_mais_emprestados()
        self.assertEqual(relatorio, [])

    def test_contrato_schema_saida_livros_mais_emprestados(self):
        relatorio_mock = self.service.gerar_relatorio_livros_mais_emprestados()
        
        if relatorio_mock:
            primeiro_item = relatorio_mock[0]
            self.assertIn('titulo', primeiro_item)
            self.assertIn('autor', primeiro_item)
            self.assertIn('totalEmprestimos', primeiro_item)
            self.assertIsInstance(primeiro_item['totalEmprestimos'], int)

if __name__ == '__main__':
    unittest.main(verbosity=2)