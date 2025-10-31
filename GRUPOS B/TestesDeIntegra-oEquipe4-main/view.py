# Arquivo: View_and_Interface/view.py
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import controller as ctl
from Model import model as md

# Simula uma instância do Controller que será usada pela View
# O loginTru é falso por enquanto, pois o HTTP não mantém estado de sessão facilmente.
controler_instance = ctl.Controler(loginTru=False) 

class DespesaController(BaseHTTPRequestHandler):
    """
    Simula a View/Controller que processa requisições HTTP e interage com o Controller lógico (ctl).
    O nome 'DespesaController' é o nome que a função main passa para o HTTPServer.
    """

    def _set_headers(self, status=200, content_type='text/html'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        """Lida com requisições GET para exibir a interface ou resultados."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/':
            self._set_headers()
            self.wfile.write(self._build_main_html().encode('utf-8'))
        
        elif path == '/despesas':
            despesas = controler_instance.Get_Despesas()
            self._set_headers()
            self.wfile.write(self._build_despesas_html(despesas).encode('utf-8'))

        elif path == '/categorias':
            categorias = controler_instance.Get_Categorias_Cadastradas()
            self._set_headers()
            self.wfile.write(self._build_categorias_html(categorias).encode('utf-8'))

        else:
            self._set_headers(404)
            self.wfile.write("<h1>404 Not Found</h1>".encode('utf-8'))

    def do_POST(self):
        """Lida com requisições POST (simulando adição de dados)."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)
        
        path = urlparse(self.path).path

        if path == '/adicionar_conta':
            try:
                # Extrai os dados do POST (o controller espera bank, ag, cc, tipo)
                bank = params.get('banco', [''])[0]
                ag = params.get('agencia', [''])[0]
                cc = params.get('conta', [''])[0]
                tipo = params.get('tipo', [''])[0]
                
                if bank and ag and cc and tipo:
                    controler_instance.Ctr_Cadastra_Conta(bank, ag, cc, tipo)
                    self._redirect('/') # Redireciona para a página principal
                    return
            except Exception as e:
                print(f"Erro ao adicionar conta: {e}")

        self._set_headers(400)
        self.wfile.write("<h1>Erro ao processar POST</h1>".encode('utf-8'))


    def _redirect(self, path, status=303):
        """Função auxiliar para redirecionar após um POST bem-sucedido."""
        self.send_response(status)
        self.send_header('Location', path)
        self.end_headers()

    def _build_main_html(self):
        """Constrói a interface principal com o formulário de cadastro de conta."""
        bancos_cadastrados = controler_instance.get_Contas_Cadastradas()
        
        html = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head><title>Controle Financeiro</title>
        <style>body{{font-family:Arial;margin:20px;background:#f0f2f5;}} .container{{max-width:600px;margin:auto;background:#fff;padding:25px;border-radius:8px;box-shadow:0 0 10px rgba(0,0,0,0.1);}} h2{{color:#007bff;}} table{{width:100%;border-collapse:collapse;margin-top:20px;}} th,td{{padding:10px;text-align:left;border-bottom:1px solid #ddd;}} th{{background-color:#007bff;color:white;}} a{{margin-right:15px;text-decoration:none;color:#007bff;}} a:hover{{text-decoration:underline;}}</style>
        </head>
        <body>
        <div class="container">
            <h2>Gerenciador de Despesas - Inicial</h2>
            
            <div><a href="/">HOME</a><a href="/despesas">VER DESPESAS</a><a href="/categorias">VER CATEGORIAS</a></div>
            
            <h3>Cadastrar Nova Conta Bancária</h3>
            <form method="POST" action="/adicionar_conta">
                Banco: <input type="text" name="banco" required><br><br>
                Agência: <input type="text" name="agencia" required><br><br>
                Conta Corrente: <input type="text" name="conta" required><br><br>
                Tipo (C/P): <input type="text" name="tipo" required><br><br>
                <input type="submit" value="Cadastrar Conta">
            </form>

            <hr>
            <h3>Contas Cadastradas</h3>
            <table>
                <tr><th>Banco</th><th>Agência</th><th>Conta</th><th>Tipo</th></tr>
        """
        for conta in bancos_cadastrados:
            html += f"<tr><td>{conta.banco}</td><td>{conta.agencia}</td><td>{conta.cc}</td><td>{conta.tipo}</td></tr>"

        html += """
            </table>
        </div>
        </body>
        </html>
        """
        return html

    def _build_despesas_html(self, despesas):
        """Constrói a visualização de Despesas (Simplificado)."""
        html = """
        <!DOCTYPE html>
        <html><head><title>Despesas</title></head><body>
            <h2>Lista de Despesas</h2>
            <a href="/">Voltar</a>
            <ul>
        """
        if not despesas:
            html += "<li>Nenhuma despesa registrada.</li>"
        else:
            for d in despesas:
                html += f"<li>{d.descricao} - R$ {d.valor:.2f} ({d.categoria.nome} / {d.conta.banco})</li>"
        
        html += """
            </ul></body></html>
        """
        return html

    def _build_categorias_html(self, categorias):
        """Constrói a visualização de Categorias."""
        html = """
        <!DOCTYPE html>
        <html><head><title>Categorias</title></head><body>
            <h2>Categorias Cadastradas</h2>
            <a href="/">Voltar</a>
            <ul>
        """
        for c in categorias:
            html += f"<li>{c.nome}</li>"
        
        html += """
            </ul></body></html>
        """
        return html