from Model import model as md
from View_and_Interface import view as vw
import controller as ctl
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

def main():
    print("Starting Service...\n")

    # Configura o servidor HTTP na porta 8000.
    # A classe vw.DespesaController é o manipulador de requisições.
    servidor = HTTPServer(("localhost", 8000), vw.DespesaController)
    print("Servidor rodando em http://localhost:8000")
    
    # Inicia o servidor, mantendo-o ativo para lidar com requisições.
    servidor.serve_forever()

if __name__ == "__main__":
    main()