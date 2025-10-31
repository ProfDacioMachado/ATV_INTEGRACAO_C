# Arquivo: Model/User.py

class User:
    def __init__(self, login, senha):
        self.login = login
        self.senha = senha

    def autenticar(self):
        # Lógica de autenticação mocada
        if self.login == "admin" and self.senha == "123":
            return True
        return False