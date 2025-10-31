from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from html import escape
import controller as ctl

def _esc(v):
    return escape("" if v is None else str(v))

comTrole = ctl.Controler()


class LivroController(BaseHTTPRequestHandler):
    def do_GET(self):
        # Página inicial -> redireciona para o menu
        if self.path == "/":
            self.send_response(302)
            self.send_header("Location", "/menu")
            self.end_headers()

        # Página do menu
        elif self.path == "/menu":
            with open("View_and_Interface/menu.html", "rb") as f:
                conteudo = f.read()
            self._send_html(conteudo)

        # Página de cadastro
        elif self.path == "/cadastrar_livro":
            with open("View_and_Interface/cadastrar_livro.html", "rb") as f:
                conteudo = f.read()
            self._send_html(conteudo)

        # Página de listagem
        elif self.path == "/listar_livros":
            livros = comTrole.Get_Livros()
            resposta = ""
            for livro in livros:
                autores = ", ".join(livro.autores)
                resposta += f"""
                <div class="card mb-3 p-4 shadow-sm border-0">
                    <h5 class="card-title text-primary">{_esc(livro.titulo)}</h5>
                    <p class="mb-1"><b>Autores:</b> {_esc(autores)}</p>
                    <p class="mb-1"><b>ISBN:</b> {_esc(livro.ISBN)}</p>
                    <p class="mb-1"><b>Ano:</b> {_esc(livro.ano)}</p>
                    <p class="mb-1"><b>Cópias:</b> {_esc(livro.copiasDisponiveis)}/{_esc(livro.copiasTotal)}</p>
                    <p class="mb-2"><b>Status:</b> {_esc(livro.status)}</p>

                    <div class="d-flex gap-2">
                        <form method="GET" action="/alterar_livro">
                            <input type="hidden" name="isbn" value="{_esc(livro.ISBN)}">
                            <button class="btn btn-warning btn-sm" type="submit">✏️ Editar</button>
                        </form>
                        <form method="POST" action="/remover_livro" onsubmit="return confirm('Deseja realmente remover este livro?');">
                            <input type="hidden" name="isbn" value="{_esc(livro.ISBN)}">
                            <button class="btn btn-danger btn-sm" type="submit">🗑️ Remover</button>
                        </form>
                    </div>
                </div>
                """


            with open("View_and_Interface/listar_livros.html", "r", encoding="utf-8") as f:
                conteudo = f.read()
            conteudo = conteudo.replace("<!--LIVROS-->", resposta)
            self._send_html(conteudo.encode("utf-8"))

        # Página de alteração
        elif self.path.startswith("/alterar_livro"):
            query = urlparse(self.path).query
            params = parse_qs(query)
            isbn = params.get("isbn", [""])[0]

            livro = next((l for l in comTrole.Get_Livros() if l.ISBN == isbn), None)
            if not livro:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Livro nao encontrado")
                return

            with open("View_and_Interface/alterar_livro.html", "r", encoding="utf-8") as f:
                conteudo = f.read()
            conteudo = (conteudo
                        .replace("<!--TITULO-->", _esc(livro.titulo))
                        .replace("<!--AUTORES-->", _esc(", ".join(livro.autores)))
                        .replace("<!--ISBN-->", _esc(livro.ISBN))
                        .replace("<!--ANO-->", _esc(livro.ano))
                        .replace("<!--COPIASTOTAL-->", _esc(livro.copiasTotal)))
            self._send_html(conteudo.encode("utf-8"))

    def do_POST(self):
        # Cadastro de novo livro
        if self.path == "/cadastrar":
            tamanho = int(self.headers["Content-Length"])
            dados = self.rfile.read(tamanho).decode("utf-8")
            params = parse_qs(dados)

            dados_livro = {
                "titulo": params.get("titulo", [""])[0],
                "autores": [a.strip() for a in params.get("autores", [""])[0].split(",")],
                "isbn": params.get("isbn", [""])[0],
                "ano": params.get("ano", [""])[0],
                "copiasTotal": params.get("copiasTotal", [""])[0],
                "copiasDisponiveis": params.get("copiasDisponiveis", [""])[0],
            }

            comTrole.Ctr_Adicionar_Livro(dados_livro)

            with open("View_and_Interface/livro_cadastrado.html", "r", encoding="utf-8") as f:
                conteudo = f.read()

            conteudo = conteudo.replace("<!--TITULO-->", _esc(dados_livro["titulo"]))
            conteudo = conteudo.replace("<!--ISBN-->", _esc(dados_livro["isbn"]))
            self._send_html(conteudo.encode("utf-8"))

        # Remover livro
        elif self.path == "/remover_livro":
            tamanho = int(self.headers["Content-Length"])
            dados = self.rfile.read(tamanho).decode("utf-8")
            params = parse_qs(dados)
            isbn = params.get("isbn", [""])[0]

            comTrole.Remover_Livro(isbn)
            self.send_response(302)
            self.send_header("Location", "/listar_livros")
            self.end_headers()

        # Alterar livro
        elif self.path == "/alterar_livro":
            tamanho = int(self.headers["Content-Length"])
            dados = self.rfile.read(tamanho).decode("utf-8")
            params = parse_qs(dados)

            isbn = params.get("isbn", [""])[0]
            novo_titulo = params.get("titulo", [""])[0]
            novos_autores = [a.strip() for a in params.get("autores", [""])[0].split(",")]
            novo_ano = int(params.get("ano", ["0"])[0])
            nova_qtd = int(params.get("copiasTotal", ["0"])[0])

            comTrole.Alterar_Livro(isbn, novo_titulo, novos_autores, novo_ano, nova_qtd)

            self.send_response(302)
            self.send_header("Location", "/listar_livros")
            self.end_headers()

    def _send_html(self, conteudo):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(conteudo)


if __name__ == "__main__":
    servidor = HTTPServer(("localhost", 8080), LivroController)
    print("Servidor rodando em http://localhost:8080")
    servidor.serve_forever()
