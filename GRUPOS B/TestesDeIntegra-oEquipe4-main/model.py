# Arquivo: Model/model.py

# --- Classes de Entidades ---

class Despesa:
    def __init__(self, descricao, valor, mes, categoria, conta):
        self.descricao = descricao
        self.valor = valor
        self.mes = mes
        self.categoria = categoria
        self.conta = conta

    def get_valor(self):
        return self.valor

class Categoria:
    def __init__(self, nome):
        self.nome = nome

class Conta:
    def __init__(self, banco, agencia, cc, tipo):
        self.banco = banco
        self.agencia = agencia
        self.cc = cc
        self.tipo = tipo
    
    def get_bank(self):
        return self.banco

# --- Simulação de Base de Dados (Listas Globais) ---

despesas_list = []
bancos_list = []
categorias_list = []

# Adicionando mocks iniciais
categorias_list.append(Categoria("Alimentação"))
categorias_list.append(Categoria("Transporte"))

bancos = [
    Conta("Banco do Brasil", "0001", "1234-5", "Corrente"),
    Conta("Itaú", "1234", "6789-0", "Poupança")
]

# Variável usada no Ctr_Adiciona_Despesa (corrigida para o nome global)
desepesa = despesas_list 

# --- Funções de Manipulação de Dados (CRUD) ---

def adiocionar_despesa(despesa_new):
    despesas_list.append(despesa_new)

def clac_total_mensal(mes):
    total = sum(d.valor for d in despesas_list if d.mes == mes)
    return total

def adiocionar_categoria(nome):
    categorias_list.append(Categoria(nome))

def adiocionar_conta(dados_inseridos):
    bank, ag, cc, tipo = dados_inseridos
    bancos.append(Conta(bank, ag, cc, tipo))
    bancos_list.append(Conta(bank, ag, cc, tipo)) # Mantenho a referência para 'bancos_list' do controller