from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import controler as ctl
from html import escape


def _esc(v):
    return escape("" if v is None else str(v))


comTrole = ctl.Controler(True)


class UsuarioController(BaseHTTPRequestHandler):

    def do_GET(self):
        print(f"GET request para: {self.path}")  # Debug log
        
        if self.path == "/":
            self.send_response(302)
            self.send_header("Location", "/usuarios")
            self.end_headers()

        elif self.path == "/usuarios":
            with open("View_and_Interface/usuarios.html", "rb") as f:
                conteudo = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo)

        elif self.path == "/cadastrar_usuario":
            with open("View_and_Interface/cadastrar_usuario.html", "rb") as f:
                conteudo = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo)

        elif self.path == "/editar_usuario" or self.path.startswith("/editar_usuario?"):
            try:
                with open("View_and_Interface/editar_usuario.html", "rb") as f:
                    conteudo = f.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(conteudo)
            except FileNotFoundError:
                print("❌ Arquivo editar_usuario.html não encontrado")
                self.send_response(404)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("<h1>Arquivo não encontrado</h1>".encode("utf-8"))
            except Exception as e:
                print(f"❌ Erro ao carregar editar_usuario.html: {e}")
                self.send_response(500)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("<h1>Erro interno do servidor</h1>".encode("utf-8"))

        elif self.path.startswith("/listar_usuarios"):
            usuarios = comTrole.Ctr_Listar_Usuarios()
            resposta = ""
            for usuario in usuarios:
                status_class = f"status-{usuario.get_status().lower()}"
                tipo_class = f"tipo-{usuario.get_tipo().lower()}"
                resposta += f'''
                <tr>
                    <td>{usuario.get_id()}</td>
                    <td>{_esc(usuario.get_nome())}</td>
                    <td>{_esc(usuario.get_matricula())}</td>
                    <td><span class="{tipo_class}">{_esc(usuario.get_tipo())}</span></td>
                    <td>{_esc(usuario.get_email() or '')}</td>
                    <td><span class="{status_class}">{_esc(usuario.get_status())}</span></td>
                    <td>{_esc(usuario.get_ativoDeRegistro())}</td>
                    <td>
                        <a href="/editar_usuario?id={usuario.get_id()}" class="btn btn-warning">Editar</a>
                        <button onclick="excluirUsuario({usuario.get_id()})" class="btn btn-danger">Excluir</button>
                    </td>
                </tr>
                '''
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(resposta.encode("utf-8"))

        elif self.path.startswith("/buscar_usuario"):
            try:
                query_params = parse_qs(self.path.split('?')[1] if '?' in self.path else '')
                id_usuario = int(query_params.get('id', [0])[0])
                
                if id_usuario <= 0:
                    raise ValueError("ID inválido")
                
                usuario = comTrole.Ctr_Buscar_Usuario_Por_Id(id_usuario)
                if usuario:
                    usuario_dict = usuario.to_dict()
                    import json
                    resposta = json.dumps(usuario_dict, ensure_ascii=False)
                    self.send_response(200)
                    self.send_header("Content-type", "application/json; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(resposta.encode("utf-8"))
                else:
                    self.send_response(404)
                    self.send_header("Content-type", "application/json; charset=utf-8")
                    self.end_headers()
                    self.wfile.write('{"erro": "Usuário não encontrado"}'.encode("utf-8"))
            except (ValueError, IndexError) as e:
                self.send_response(400)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write('{"erro": "ID inválido"}'.encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write('{"erro": "Erro interno do servidor"}'.encode("utf-8"))

    def do_POST(self):
        if self.path == "/criar_usuario":
            tamanho = int(self.headers["Content-Length"])
            dados = self.rfile.read(tamanho).decode("utf-8")
            params = parse_qs(dados)

            nome = params.get("nome", [""])[0]
            matricula = params.get("matricula", [""])[0]
            tipo = params.get("tipo", [""])[0]
            email = params.get("email", [""])[0] or None

            sucesso, resultado = comTrole.Ctr_Criar_Usuario(nome, matricula, tipo, email)
            
            if sucesso:
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("Usuário criado com sucesso!".encode("utf-8"))
            else:
                self.send_response(400)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                if isinstance(resultado, list):
                    erro_msg = "; ".join(resultado)
                else:
                    erro_msg = str(resultado)
                self.wfile.write(erro_msg.encode("utf-8"))

        elif self.path == "/atualizar_usuario":
            tamanho = int(self.headers["Content-Length"])
            dados = self.rfile.read(tamanho).decode("utf-8")
            params = parse_qs(dados)

            id_usuario = int(params.get("id", [0])[0])
            nome = params.get("nome", [""])[0]
            matricula = params.get("matricula", [""])[0]
            tipo = params.get("tipo", [""])[0]
            email = params.get("email", [""])[0] or None
            status = params.get("status", [""])[0]

            sucesso, resultado = comTrole.Ctr_Atualizar_Usuario(id_usuario, nome, matricula, tipo, email, status)
            
            if sucesso:
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("Usuário atualizado com sucesso!".encode("utf-8"))
            else:
                self.send_response(400)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                if isinstance(resultado, list):
                    erro_msg = "; ".join(resultado)
                else:
                    erro_msg = str(resultado)
                self.wfile.write(erro_msg.encode("utf-8"))

        elif self.path == "/excluir_usuario":
            tamanho = int(self.headers["Content-Length"])
            dados = self.rfile.read(tamanho).decode("utf-8")
            params = parse_qs(dados)

            id_usuario = int(params.get("id", [0])[0])
            sucesso, resultado = comTrole.Ctr_Excluir_Usuario(id_usuario)
            
            if sucesso:
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("Usuário excluído com sucesso!".encode("utf-8"))
            else:
                self.send_response(400)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(str(resultado).encode("utf-8"))
