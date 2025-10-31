# Arquivo: controller.py
# Contém a classe Controler que lida com a lógica de negócio e intermediação.

from Model import model as md
from Model import User as user

class Controler():
    def __init__(self, loginTru):
        self.loginTrue = loginTru
    
    def Ctr_Adiciona_Despesa(self, despesa_new):
        md.adiocionar_despesa(despesa_new)
        # O print abaixo foi baseado no seu código original, mas md.despesas_list[1] pode não existir.
        # Mantendo a estrutura original:
        # print(md.desepesa[1].get_valor()) 
        pass 
        
    def Get_Despesas(self):
        return md.despesas_list

    def Get_Total_Mensal(self, mes):
        return md.clac_total_mensal(mes)

    def Atutenticar(self, login, senha):
        Usuario_Autenticado = user.User(login, senha)
        return Usuario_Autenticado.autenticar()

    def get_Contas_Cadastradas(self):
        # md.bancos_list é atualizada ao adicionar contas
        return md.bancos_list

    def get_Bancos_List(self):
        list = []  
        for bn in md.bancos: # md.bancos contém os mocks iniciais e contas cadastradas
            list.append (bn.get_bank())
        return list
        
    def Ctr_Adiciona_Categoria(self, categoria):
        md.adiocionar_categoria(categoria)

    def Get_Categorias_Cadastradas(self):
        return md.categorias_list

    def Ctr_Cadastra_Conta(self, bank, ag, cc, tipo):
        dados_inseridos = [bank, ag, cc, tipo]
        md.adiocionar_conta(dados_inseridos)


# @Alunos --> moc de implementação correta para versões futuras;
class Ctrl_User(user.User):
    def __init__(self, login, senha):
        super().__init__(login, senha)

    def autenticar(self):
        return super().autenticar()