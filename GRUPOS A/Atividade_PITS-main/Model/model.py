from Model import User as usr
import configparser

usuarios = []
usuarios.append(usr.User("João Silva", "12345", "ALUNO", "joao@email.com", "joao", "senha123"))
usuarios.append(usr.User("Maria Santos", "67890", "PROFESSOR", "maria@email.com", "maria", "senha456"))
usuarios.append(usr.User("Pedro Costa", "11111", "FUNCIONARIO", "pedro@email.com", "pedro", "senha789"))

for i, usuario in enumerate(usuarios, start=1):
    usuario.set_id(i)

config = configparser.ConfigParser()
config.read("user.data", encoding="utf-8")

def get_Usuario_data():
  user = config["credenciais"]["user"]
  senha = config["credenciais"]["senha"]
  return user, senha

def criar_usuario(nome, matricula, tipo, email=None):
    novo_usuario = usr.User(nome, matricula, tipo, email)
    
    valido, erros = novo_usuario.validar_todos_campos()
    if not valido:
        return False, erros
    
    for usuario in usuarios:
        if usuario.get_matricula() == matricula:
            return False, ["Matrícula já existe"]
    
    if email:
        for usuario in usuarios:
            if usuario.get_email() == email:
                return False, ["Email já existe"]
    
    novo_usuario.set_id(len(usuarios) + 1)
    usuarios.append(novo_usuario)
    return True, "Usuário criado com sucesso"

def buscar_usuario_por_id(id):
    for usuario in usuarios:
        if usuario.get_id() == id:
            return usuario
    return None

def buscar_usuario_por_matricula(matricula):
    for usuario in usuarios:
        if usuario.get_matricula() == matricula:
            return usuario
    return None

def listar_usuarios():
    return usuarios

def atualizar_usuario(id, nome=None, matricula=None, tipo=None, email=None, status=None):
    usuario = buscar_usuario_por_id(id)
    if not usuario:
        return False, "Usuário não encontrado"
    
    if nome is not None:
        usuario.set_nome(nome)
    if matricula is not None:
        if matricula != usuario.get_matricula():
            for u in usuarios:
                if u.get_matricula() == matricula and u.get_id() != id:
                    return False, ["Matrícula já existe"]
        usuario.set_matricula(matricula)
    if tipo is not None:
        usuario.set_tipo(tipo)
    if email is not None:
        if email != usuario.get_email() and email:
            for u in usuarios:
                if u.get_email() == email and u.get_id() != id:
                    return False, ["Email já existe"]
        usuario.set_email(email)
    if status is not None:
        usuario.set_status(status)
    
    valido, erros = usuario.validar_todos_campos()
    if not valido:
        return False, erros
    
    return True, "Usuário atualizado com sucesso"

def excluir_usuario(id):
    usuario = buscar_usuario_por_id(id)
    if not usuario:
        return False, "Usuário não encontrado"
    
    usuarios.remove(usuario)
    return True, "Usuário excluído com sucesso"

def buscar_usuarios_por_tipo(tipo):
    return [usuario for usuario in usuarios if usuario.get_tipo() == tipo]

def buscar_usuarios_por_status(status):
    return [usuario for usuario in usuarios if usuario.get_status() == status]
