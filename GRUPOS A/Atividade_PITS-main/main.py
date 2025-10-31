from View_and_Interface import view as vw
from http.server import HTTPServer

def main():
  print("Starting User Management Service...\n")
  
  servidor = HTTPServer(("localhost", 8000), vw.UsuarioController)
  print("Servidor rodando em http://localhost:8000")
  print("Acesse http://localhost:8000/usuarios para gerenciar usuários")
  servidor.serve_forever()

if __name__ == "__main__":
  main()
