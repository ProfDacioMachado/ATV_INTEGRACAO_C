import itertools

class Book:
    """Classe que representa um livro e suas operações básicas em estoque."""
    id_iter = itertools.count()

    def __init__(self, titulo, autores, isbn, ano, copiasTotal, copiasDisponiveis):
        self.bookId = next(Book.id_iter)
        self.titulo = titulo
        self.autores = autores
        self.ISBN = isbn
        self.edicao = None
        self.ano = ano
        self.copiasTotal = copiasTotal
        self.copiasDisponiveis = copiasDisponiveis
        self._atualizar_status()

    @staticmethod
    def adicionarLivro(titulo, autores, isbn, ano, copiasTotal, copiasDisponiveis):
        """Cria um novo livro com validações de dados."""
        Book._validar_titulo(titulo)
        Book._validar_autores(autores)
        Book._validar_isbn(isbn)
        Book._validar_ano(ano)
        Book._validar_estoque(copiasTotal, copiasDisponiveis)

        return Book(titulo, autores, isbn, ano, copiasTotal, copiasDisponiveis)

    @staticmethod
    def removerLivro(listaLivros, isbn):
        """Remove um livro de uma lista com base no ISBN."""
        if not isinstance(listaLivros, list):
            raise ValueError("A lista de livros deve ser uma lista válida")

        if not any(livro.ISBN == isbn for livro in listaLivros):
            raise ValueError("Livro não encontrado para remoção")

        return [livro for livro in listaLivros if livro.ISBN != isbn]

    @staticmethod
    def listarLivros(listaLivros):
        """Retorna uma lista formatada com informações dos livros."""
        if not isinstance(listaLivros, list):
            raise ValueError("A lista de livros deve ser uma lista válida")

        return [
            (
                f"ID: {livro.bookId}, Título: {livro.titulo}, "
                f"Autores: {', '.join(livro.autores)}, ISBN: {livro.ISBN}, "
                f"Status: {livro.status}"
            )
            for livro in listaLivros
        ]

    def emprestarLivro(self):
        """Reduz 1 cópia disponível e atualiza o status."""
        if self.copiasDisponiveis <= 0:
            raise ValueError("Não há cópias disponíveis para empréstimo.")
        self.copiasDisponiveis -= 1
        self._atualizar_status()

    def devolverLivro(self):
        """Aumenta 1 cópia disponível e atualiza o status."""
        if self.copiasDisponiveis >= self.copiasTotal:
            raise ValueError("Todas as cópias já estão disponíveis.")
        self.copiasDisponiveis += 1
        self._atualizar_status()

    def _atualizar_status(self):
        """Atualiza o status com base na disponibilidade."""
        self.status = "DISPONIVEL" if self.copiasDisponiveis > 0 else "INDISPONIVEL"

    @staticmethod
    def _validar_titulo(titulo):
        if not titulo or len(titulo) > 200:
            raise ValueError("Título inválido")

    @staticmethod
    def _validar_autores(autores):
        if not isinstance(autores, list) or not autores:
            raise ValueError("Autor inválido")
        for autor in autores:
            if not autor or len(autor) > 100:
                raise ValueError("Autor inválido")

    @staticmethod
    def _validar_isbn(isbn):
        isbn_limpo = isbn.replace("-", "")
        if len(isbn_limpo) not in (10, 13):
            raise ValueError("ISBN inválido")

    @staticmethod
    def _validar_ano(ano):
        if not isinstance(ano, int):
            raise ValueError("Ano inválido")

    @staticmethod
    def _validar_estoque(copiasTotal, copiasDisponiveis):
        if copiasTotal < 0:
            raise ValueError("Número total de cópias inválido")
        if copiasDisponiveis < 0 or copiasDisponiveis > copiasTotal:
            raise ValueError("Número de cópias disponíveis inválido")
    @staticmethod
    def alterarLivro(listaLivros, isbn, novo_titulo=None, novos_autores=None, novo_ano=None, nova_quantidade=None):
        """Altera os dados de um livro existente na lista com base no ISBN."""

        if not isinstance(listaLivros, list):
            raise ValueError("A lista de livros deve ser uma lista válida")

        # Busca o livro pelo ISBN
        livro = next((l for l in listaLivros if l.ISBN == isbn), None)
        if not livro:
            raise ValueError("Livro não encontrado para alteração")

        # Atualiza atributos se foram fornecidos
        if novo_titulo is not None:
            Book._validar_titulo(novo_titulo)
            livro.titulo = novo_titulo

        if novos_autores is not None:
            Book._validar_autores(novos_autores)
            livro.autores = novos_autores

        if novo_ano is not None:
            Book._validar_ano(novo_ano)
            livro.ano = novo_ano

        if nova_quantidade is not None:
            # Valida e atualiza o estoque
            Book._validar_estoque(nova_quantidade, livro.copiasDisponiveis)

            # Atualiza o total de cópias
            livro.copiasTotal = nova_quantidade

            # Ajusta disponíveis: se aumentar total, todas ficam disponíveis
            livro.copiasDisponiveis = max(livro.copiasDisponiveis, nova_quantidade)

            livro._atualizar_status()

        return listaLivros