from Model import model as md
from Model import User as user

class Controler():
  def __init__(self, loginTru):
   self.loginTrue = loginTru

  def Atutenticar(self, login, senha):
    Usuario_Autenticado = user.User(login=login, senha=senha)
    return Usuario_Autenticado.autenticar()

  def Ctr_Criar_Usuario(self, nome, matricula, tipo, email=None):
    return md.criar_usuario(nome, matricula, tipo, email)

  def Ctr_Buscar_Usuario_Por_Id(self, id):
    return md.buscar_usuario_por_id(id)

  def Ctr_Buscar_Usuario_Por_Matricula(self, matricula):
    return md.buscar_usuario_por_matricula(matricula)

  def Ctr_Listar_Usuarios(self):
    return md.listar_usuarios()

  def Ctr_Atualizar_Usuario(self, id, nome=None, matricula=None, tipo=None, email=None, status=None):
    return md.atualizar_usuario(id, nome, matricula, tipo, email, status)

  def Ctr_Excluir_Usuario(self, id):
    return md.excluir_usuario(id)

  def Ctr_Buscar_Usuarios_Por_Tipo(self, tipo):
    return md.buscar_usuarios_por_tipo(tipo)

  def Ctr_Buscar_Usuarios_Por_Status(self, status):
    return md.buscar_usuarios_por_status(status)


class Ctrl_User(user.User):
  def __init__(self, login, senha):
    super().__init__(login=login, senha=senha)

  def autenticar(self):
      return super().autenticar()