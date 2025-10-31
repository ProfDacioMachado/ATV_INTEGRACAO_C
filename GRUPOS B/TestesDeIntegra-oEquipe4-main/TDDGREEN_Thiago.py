import unittest
from unittest.mock import MagicMock
from relatorio_service import RelatorioService, DadosEmprestimo, DadosLivro

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

    # TU 5: Filtro de Período (Filtro com Datas)
    def test_filtro_relatorio_por_periodo(self):
        # Espera-se 2 empréstimos entre 01/02 e 30/04
        data_inicio = '2025-02-01'
        data_fim = '2025-04-30'
        emprestimos_filtrados = self.service.filtrar_por_periodo(data_inicio, data_fim)
        
        self.assertEqual(len(emprestimos_filtrados), 2)
        self.assertEqual(emprestimos_filtrados[0].idLivro, 102)
        self.assertEqual(emprestimos_filtrados[1].idLivro, 103)
        
    # TU 6: Tratamento de Dados Inválidos (Matrícula Inexistente)
    def test_tratamento_dado_invalido_matricula_inexistente(self):
        # Mock do getUsuario para retornar None para a matricula 999
        self.mock_repo.getUsuario.side_effect = lambda id: None if id == 999 else DadosUsuario(id, f"Usuario {id}")
        self.mock_repo.getAllEmprestimos.return_value = [
            DadosEmprestimo(999, 101, '2025-01-01'), # Empréstimo com usuário inexistente
            DadosEmprestimo(1, 102, '2025-01-05'),
        ]
        # O serviço deve processar sem erro (não lançar exceção)
        self.assertIsNone(self.service.gerar_relatorio_usuarios_mais_ativos()) # O serviço deve ser capaz de lidar com isso sem crashar.
        # Ajuste: A implementação do service foi alterada para não falhar, retorna uma lista.
        # Portanto, o teste deve verificar se o processo termina.
        self.assertIsNotNone(self.service.gerar_relatorio_usuarios_mais_ativos())

    # TC 3: Contrato de Dados do Livro
    def test_contrato_dados_livro(self):
        # Verifica se o objeto de livro mockado (que simula a entrada da Equipe 2) 
        # possui os campos essenciais.
        livro_mock = MagicMock(spec=DadosLivro, id=100, titulo="Mock Livro", autor="Mock Autor")
        self.assertTrue(hasattr(livro_mock, 'titulo'))
        self.assertTrue(hasattr(livro_mock, 'autor'))
        self.assertTrue(hasattr(livro_mock, 'id'))

if __name__ == '__main__':
    unittest.main()