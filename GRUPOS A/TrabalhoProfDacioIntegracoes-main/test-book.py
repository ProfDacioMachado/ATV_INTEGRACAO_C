import unittest
import itertools
from book import Book 

class TestBook(unittest.TestCase):

    def setUp(self):
        
        Book.id_iter = itertools.count()
        
      
        self.livro1 = Book.adicionarLivro(
            "O Hobbit", 
            ["J.R.R. Tolkien"], 
            "1234567890", 1937, 2, 2
        ) # ID será 0
        
        self.livro2 = Book.adicionarLivro(
            "O Nome do Vento", 
            ["Patrick Rothfuss"], 
            "9876543210", 2007, 1, 0
        ) # ID será 1
        
        self.livro3 = Book.adicionarLivro(
            "Good Omens", 
            ["Terry Pratchett", "Neil Gaiman"], 
            "5555555555", 1990, 5, 5
        ) # ID será 2



    def test_criar_livro(self):
        
        self.assertEqual(self.livro1.titulo, "O Hobbit")
        self.assertEqual(self.livro1.autores, ["J.R.R. Tolkien"])
        self.assertEqual(self.livro1.ISBN, "1234567890")
        self.assertEqual(self.livro1.ano, 1937)
        self.assertEqual(self.livro1.status, "DISPONIVEL")
        self.assertEqual(self.livro1.bookId, 0) 

    def test_criar_livro_titulo_invalido(self):
        with self.assertRaises(ValueError) as context:
            Book.adicionarLivro(
                "", ["J.R.R. Tolkien"], "978-3-16-148410-0", 1954, 5, 3
            )
        self.assertEqual(str(context.exception), "Título inválido")

    def test_remover_livro(self):
     
        livros = [self.livro1, self.livro2]
        livros = Book.removerLivro(livros, "9876543210") 

        self.assertEqual(len(livros), 1)
        self.assertEqual(livros[0].titulo, "O Hobbit")

    def test_remover_livro_inexistente(self):
        livros = [self.livro1]
        with self.assertRaises(ValueError) as context:
            Book.removerLivro(livros, "0000000000")
        self.assertEqual(str(context.exception), "Livro não encontrado para remoção")

    def test_listar_livros_lista_vazia(self):
        livros = []
        resultado = Book.listarLivros(livros)
        self.assertEqual(resultado, [])

    def test_listar_livros_com_um_livro(self):
        livros = [self.livro1] 
        resultado = Book.listarLivros(livros)
        
        expected_output = [
            "ID: 0, Título: O Hobbit, Autores: J.R.R. Tolkien, ISBN: 1234567890, Status: DISPONIVEL"
        ]
        self.assertEqual(resultado, expected_output)
        
    def test_listar_livros_multiplos(self):
        livros = [self.livro1, self.livro2, self.livro3] 
        resultado = Book.listarLivros(livros)

        expected_output = [
            "ID: 0, Título: O Hobbit, Autores: J.R.R. Tolkien, ISBN: 1234567890, Status: DISPONIVEL",
            "ID: 1, Título: O Nome do Vento, Autores: Patrick Rothfuss, ISBN: 9876543210, Status: INDISPONIVEL",
            "ID: 2, Título: Good Omens, Autores: Terry Pratchett, Neil Gaiman, ISBN: 5555555555, Status: DISPONIVEL"
        ]
        self.assertEqual(resultado, expected_output)

    def test_listar_livros_input_invalido(self):
        with self.assertRaises(ValueError) as context:
            Book.listarLivros("não sou uma lista")
        self.assertEqual(str(context.exception), "A lista de livros deve ser uma lista válida")

    def test_emprestar_livro_deve_reduzir_copia_e_mudar_status(self):
        """
        Deve reduzir 1 cópia disponível e mudar status para INDISPONIVEL quando chegar a 0.
        """
        livro = Book.adicionarLivro(
            "Livro Emprestável",
            ["Autor TDD"],
            "9783161484100",
            2023,
            2,
            1
        )

        # Espera-se que o método emprestarLivro reduza copiasDisponiveis e atualize status
        livro.emprestarLivro()

        self.assertEqual(livro.copiasDisponiveis, 0)
        self.assertEqual(livro.status, "INDISPONIVEL")


    def test_devolver_livro_deve_aumentar_copia_e_mudar_status(self):
        """
        Deve aumentar 1 cópia disponível e mudar status para DISPONIVEL quando devolver.
        """
        livro = Book.adicionarLivro(
            "Livro Devolvido",
            ["Autor TDD"],
            "9783161484101",
            2022,
            2,
            0
        )

        # Espera-se que o método devolverLivro aumente copiasDisponiveis e atualize status
        livro.devolverLivro()

        self.assertEqual(livro.copiasDisponiveis, 1)
        self.assertEqual(livro.status, "DISPONIVEL")

    def test_alterar_livro(self):
        
        livro1 = Book.adicionarLivro("Livro 1", ["Autor 1"], "1234567890", 2000, 3, 3)
        livro2 = Book.adicionarLivro("Livro 2", ["Autor 2"], "0987654321", 2005, 2, 2)
        livros = [livro1, livro2]

        
        livros = Book.alterarLivro(
            livros, 
            isbn="0987654321", 
            novo_titulo="Livro 2 - Edição Atualizada", 
            novos_autores=["Autor 2", "Autor Extra"], 
            novo_ano=2010, 
            nova_quantidade=5
        )

        
        livro_alterado = next(l for l in livros if l.ISBN == "0987654321")
        self.assertEqual(livro_alterado.titulo, "Livro 2 - Edição Atualizada")
        self.assertEqual(livro_alterado.autores, ["Autor 2", "Autor Extra"])
        self.assertEqual(livro_alterado.ano, 2010)
        self.assertEqual(livro_alterado.copiasDisponiveis, 5)

    def test_alterar_livro_inexistente(self):
        
        livro = Book.adicionarLivro("Livro Único", ["Autor X"], "1234567890", 1999, 1, 1)
        livros = [livro]

        
        with self.assertRaises(ValueError) as context:
            Book.alterarLivro(livros, isbn="0000000000", novo_titulo="Novo Título")
        self.assertEqual(str(context.exception), "Livro não encontrado para alteração")



if __name__ == '__main__':
    unittest.main()