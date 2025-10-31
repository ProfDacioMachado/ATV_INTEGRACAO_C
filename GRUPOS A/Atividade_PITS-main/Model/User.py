from datetime import datetime
import re

class User():
    def __init__(self, nome=None, matricula=None, tipo=None, email=None, login=None, senha=None):
        self.id = None
        self.nome = nome
        self.matricula = matricula
        self.tipo = tipo
        self.email = email
        self.ativoDeRegistro = datetime.now().isoformat()
        self.status = "ATIVO"
        self.login = login
        self.senha = senha

    def get_id(self):
        return self.id
    
    def get_nome(self):
        return self.nome
    
    def get_matricula(self):
        return self.matricula
    
    def get_tipo(self):
        return self.tipo
    
    def get_email(self):
        return self.email
    
    def get_ativoDeRegistro(self):
        return self.ativoDeRegistro
    
    def get_status(self):
        return self.status
    
    def get_login(self):  
        return self.login
    
    def get_senha(self):  
        return self.senha

    def set_id(self, id):
        self.id = id
    
    def set_nome(self, nome):
        self.nome = nome
    
    def set_matricula(self, matricula):
        self.matricula = matricula
    
    def set_tipo(self, tipo):
        self.tipo = tipo
    
    def set_email(self, email):
        self.email = email
    
    def set_status(self, status):
        self.status = status
    
    def set_login(self, login):
        self.login = login
    
    def set_senha(self, senha):
        self.senha = senha
    
    def validar_nome(self):
        if not self.nome or len(self.nome.strip()) == 0:
            return False, "Nome é obrigatório"
        if len(self.nome) < 1 or len(self.nome) > 100:
            return False, "Nome deve ter entre 1 e 100 caracteres"
        return True, "Nome válido"
    
    def validar_matricula(self):
        if not self.matricula or len(self.matricula.strip()) == 0:
            return False, "Matrícula é obrigatória"
        if len(self.matricula) < 5 or len(self.matricula) > 20:
            return False, "Matrícula deve ter entre 5 e 20 caracteres"
        if not re.match(r'^[a-zA-Z0-9]+$', self.matricula):
            return False, "Matrícula deve conter apenas caracteres alfanuméricos"
        return True, "Matrícula válida"
    
    def validar_tipo(self):
        tipos_validos = ["ALUNO", "PROFESSOR", "FUNCIONARIO"]
        if not self.tipo or self.tipo not in tipos_validos:
            return False, f"Tipo deve ser um dos seguintes: {', '.join(tipos_validos)}"
        return True, "Tipo válido"
    
    def validar_email(self):
        if self.email and len(self.email.strip()) > 0:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, self.email):
                return False, "Formato de email inválido"
        return True, "Email válido"
    
    def validar_status(self):
        status_validos = ["ATIVO", "INATIVO", "SUSPENSO"]
        if self.status not in status_validos:
            return False, f"Status deve ser um dos seguintes: {', '.join(status_validos)}"
        return True, "Status válido"
    
    def validar_todos_campos(self):
        validacoes = [
            self.validar_nome(),
            self.validar_matricula(),
            self.validar_tipo(),
            self.validar_email(),
            self.validar_status()
        ]
        
        erros = []
        for valido, mensagem in validacoes:
            if not valido:
                erros.append(mensagem)
        
        return len(erros) == 0, erros
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'matricula': self.matricula,
            'tipo': self.tipo,
            'email': self.email,
            'ativoDeRegistro': self.ativoDeRegistro,
            'status': self.status
        }
    
