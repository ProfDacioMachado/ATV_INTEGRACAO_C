# Arquivo: test_thiago.py
import unittest
from unittest.mock import MagicMock
from relatorio_service import RelatorioService, DadosEmprestimo, DadosLivro, DadosUsuario

class TestThiagoRelatorios(unittest.TestCase):

    def setUp(self):
        self.mock_repo = MagicMock()
        self.mock_repo.getAllEmprestimos.return_value = [
            DadosEmprestimo(1, 101, '2025-01-01'),
            DadosEmprestimo(2, 102, '2025-03-15'),
            DadosEmprestimo(3, 103, '2025-04-10'),
            DadosEmprestimo(4, 104, '2025-05-20'),
        ]
        self.mock_repo.getUsuario.return_value = MagicMock(matricula=99, nome="Usuario Mock")
        self.service = RelatorioService(repositorio=self.mock_repo)

    def test_filtro_relatorio_por_periodo(self):
        data_inicio = '2025-02-01'
        data_fim = '2025-04-30'
        emprestimos_filtrados = self.service.filtrar_por_periodo(data_inicio, data_fim)
        
        self.assertEqual(len(emprestimos_filtrados), 2)
        self.assertEqual(emprestimos_filtrados[0].idLivro, 102)
        self.assertEqual(emprestimos_filtrados[1].idLivro, 103)
        
    def test_tratamento_dado_invalido_matricula_inexistente(self):
        # Configuração do Mock para simular a falha de lookup do Usuário 999
        self.mock_repo.getUsuario.side_effect = lambda id: None if id == 999 else DadosUsuario(id, f"Usuario {id}")
        self.mock_repo.getAllEmprestimos.return_value = [
            DadosEmprestimo(999, 101, '2025-01-01'), # Empréstimo com usuário que retorna None
            DadosEmprestimo(1, 102, '2025-01-05'), # Empréstimo com usuário válido
        ]
        
        relatorio = self.service.gerar_relatorio_usuarios_mais_ativos()
        
        # O processo não deve quebrar (SUCCESS)
        self.assertIsNotNone(relatorio)
        # Deve haver 2 itens no relatório: 1 válido e 1 tratado
        self.assertEqual(len(relatorio), 2)
        # Verifica se o serviço tratou o erro substituindo o nome
        self.assertTrue(any(item['nome'] == 'Usuário Desconhecido' for item in relatorio))


    def test_contrato_dados_livro(self):
        livro_mock = MagicMock(spec=DadosLivro, id=100, titulo="Mock Livro", autor="Mock Autor")
        self.assertTrue(hasattr(livro_mock, 'titulo'))
        self.assertTrue(hasattr(livro_mock, 'autor'))
        self.assertTrue(hasattr(livro_mock, 'id'))

if __name__ == '__main__':
    unittest.main(verbosity=2)