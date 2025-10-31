# Arquivo: relatorio_service.py

class DadosEmprestimo:
    def __init__(self, idUsuario, idLivro, dataEmprestimo):
        self.idUsuario = idUsuario
        self.idLivro = idLivro
        self.dataEmprestimo = dataEmprestimo

class DadosUsuario:
    def __init__(self, matricula, nome):
        self.matricula = matricula
        self.nome = nome

class DadosLivro:
    def __init__(self, id, titulo, autor, status='disponivel'):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.status = status

class RepositorioMock:
    """Simula o acesso a dados de outras equipes/DB."""
    
    def getAllEmprestimos(self):
        # Dados mockados para simular 2 emprestimos do Livro 101, 1 do Livro 102
        return [
            DadosEmprestimo(1, 101, '2025-01-01'),
            DadosEmprestimo(2, 101, '2025-01-05'),
            DadosEmprestimo(1, 102, '2025-02-10'),
        ]
    
    def getUsuario(self, idUsuario):
        if idUsuario == 1:
            return DadosUsuario(1, "Fabricio Leitor")
        if idUsuario == 2:
            return DadosUsuario(2, "Pietro Leitor")
        return DadosUsuario(idUsuario, f"Usuario {idUsuario}") # Default
        
    def getLivro(self, idLivro):
        if idLivro == 101:
            return DadosLivro(101, "A Magia do Código", "Autor A")
        elif idLivro == 102:
            return DadosLivro(102, "Testes Essenciais", "Autor B")
        return None

    def getAllLivros(self):
        return [
            DadosLivro(101, "A Magia do Código", "Autor A", 'emprestado'),
            DadosLivro(102, "Testes Essenciais", "Autor B", 'emprestado'),
            DadosLivro(103, "Clean Code", "Autor C", 'disponivel'),
            DadosLivro(104, "Design Patterns", "Autor D", 'disponivel'),
        ]


class RelatorioService:
    def __init__(self, repositorio=None):
        self.repo = repositorio if repositorio else RepositorioMock()

    def gerar_relatorio_livros_mais_emprestados(self):
        emprestimos = self.repo.getAllEmprestimos()
        contagem = {}
        for emp in emprestimos:
            contagem[emp.idLivro] = contagem.get(emp.idLivro, 0) + 1
        
        relatorio = []
        for idLivro, total in sorted(contagem.items(), key=lambda item: item[1], reverse=True):
            livro = self.repo.getLivro(idLivro)
            if livro:
                 relatorio.append({'titulo': livro.titulo, 'autor': livro.autor, 'totalEmprestimos': total})
            else:
                 relatorio.append({'titulo': 'Livro Desconhecido', 'autor': 'N/A', 'totalEmprestimos': total})
        return relatorio

    def gerar_relatorio_usuarios_mais_ativos(self):
        emprestimos = self.repo.getAllEmprestimos()
        contagem = {}
        for emp in emprestimos:
            contagem[emp.idUsuario] = contagem.get(emp.idUsuario, 0) + 1
            
        relatorio = []
        for idUsuario, total in sorted(contagem.items(), key=lambda item: item[1], reverse=True):
            usuario = self.repo.getUsuario(idUsuario)
            
            # --- CORREÇÃO TDD GREEN APLICADA ---
            if usuario: 
                relatorio.append({'nome': usuario.nome, 'matricula': usuario.matricula, 'totalEmprestimos': total})
            else:
                # Trata o caso onde o usuário não existe no sistema
                relatorio.append({'nome': 'Usuário Desconhecido', 'matricula': idUsuario, 'totalEmprestimos': total})
            # --- FIM DA CORREÇÃO ---
            
        return relatorio

    def filtrar_por_periodo(self, data_inicio, data_fim):
        emprestimos = self.repo.getAllEmprestimos()
        return [emp for emp in emprestimos if data_inicio <= emp.dataEmprestimo <= data_fim]
    
    def gerar_relatorio_com_dados_vazios(self):
        return []

    def formatar_relatorio(self, dados):
        return {"relatorio": dados}

    def contar_status_acervo(self):
        livros = self.repo.getAllLivros()
        disponivel = sum(1 for livro in livros if livro.status == 'disponivel')
        emprestado = sum(1 for livro in livros if livro.status == 'emprestado')
        return {'disponivel': disponivel, 'emprestado': emprestado}
        
    def gerar_relatorio_com_params(self, param):
        if not param or not isinstance(param, str):
             raise ValueError("Parâmetro inválido ou ausente.")
        return []