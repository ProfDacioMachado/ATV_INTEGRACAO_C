from Model.book import Book

class Controler:
    def __init__(self):
        self.livros = []

    def Ctr_Adicionar_Livro(self, dados):
        novo = Book.adicionarLivro(
            dados["titulo"],
            dados["autores"],
            dados["isbn"],
            int(dados["ano"]),
            int(dados["copiasTotal"]),
            int(dados["copiasDisponiveis"])
        )
        self.livros.append(novo)

    def Get_Livros(self):
        return self.livros

    def Remover_Livro(self, isbn):
        self.livros = Book.removerLivro(self.livros, isbn)

    def Alterar_Livro(self, isbn, novo_titulo=None, novos_autores=None, novo_ano=None, nova_quantidade=None):
        self.livros = Book.alterarLivro(self.livros, isbn, novo_titulo, novos_autores, novo_ano, nova_quantidade)
