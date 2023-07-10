from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

LARGURA_TELA = 60
LIMITE_SAQUES = 3
AGENCIA = "0001"

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, agencia, numero, cliente):
        self._saldo = 0
        self._agencia = agencia
        self._numero = numero
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, agencia, numero, cliente ):
        return cls(agencia, numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            erro("Erro! Saldo suficiente.")

        elif valor > 0:
            self._saldo -= valor
            sucesso("Saque realizado com sucesso!")
            return True

        else:
            erro("Erro! O valor informado é inválido.")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            sucesso("Depósito realizado com sucesso!")
        else:
            erro("Erro! O valor informado é inválido.")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, agencia, numero, cliente, limite=500, limite_saques=3):
        super().__init__(agencia, numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao.__class__.__name__ == Saque.__name__]
        )

        if valor > self._limite:
            erro("Erro! Saque excede o limite.")

        elif numero_saques >= self._limite_saques:
            erro("Erro! Você chegou ao limite de saques.")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @property
    @abstractproperty
    def data(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        self._data = datetime.now().strftime("%d-%m-%Y %H:%M")

    @property
    def valor(self):
        return self._valor
    
    @property
    def data(self):
        return self._data

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        self._data = datetime.now().strftime("%d-%m-%Y %H:%M")

    @property
    def valor(self):
        return self._valor
    
    @property
    def data(self):
        return self._data

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)



def menu(conta_ativa):
    if(conta_ativa == None):
        title("MENU")
        menu = """

            [c] Cadastrar Usuário
            [n] Cadastrar Conta
            [l] Listar Cadastros
            [e] Escolher Conta
            [q] Sair

            => """
    else:
        title("CONTA")
        menu = f"""
            {conta_ativa}

            [d] Depositar
            [s] Sacar
            [x] Extrato
            [v] Voltar

            => """
    return input(menu)


def menu_contas(clientes):
    title("SELECIONAR CONTA")
    cpf = input("informe o cpf: ")
    cliente = buscar_cliente(cpf, clientes)
    
    if(len(cliente.contas) == 1):
        return cliente.contas[0]
    
    if(len(cliente.contas) == 0):
        erro("Erro! Conta não cadastrada para cliente")
        return None

    print("Contas encontradas para o usuario: ")
    for conta in cliente.contas:
        print(f"AG {conta.agencia} CC {conta.numero}")
    print("")
    numero = int(input("Digite o número da conta para ativar:"))
    
    for conta in cliente.contas:
        if conta.numero == numero:
            return conta
        
    erro("Erro! Conta não encontrada")

def main():

    clientes = []
    conta_ativa = None

    while True:
        opcao = menu(conta_ativa)        
        if opcao == "d":
            valor = float(input("Informe o valor para depósito: "))
            transacao = Deposito(valor)
            conta_ativa.cliente.realizar_transacao(conta_ativa, transacao)
        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            transacao = Saque(valor)
            conta_ativa.cliente.realizar_transacao(conta_ativa, transacao)
        elif opcao == "e":
            conta_ativa = menu_contas(clientes)
        elif opcao == "x":
            extrato(conta_ativa)
        elif opcao == "c":
            criar_cliente(clientes)
        elif opcao == "n":
            criar_conta(clientes, AGENCIA)
        elif opcao == "l":
            listar_cadastros(clientes)
        elif opcao == "v":
            conta_ativa = None
        elif opcao == "q":
            break

        else:
            erro("Operação inválida, por favor selecione novamente a operação desejada.")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = buscar_cliente(cpf, clientes)
    if cliente:
        erro("Erro! Cliente já cadastrado")
        return
    
    nome = input("Nome: ")
    data_nascimento = input("Data de nascimento : ")
    endereco = input("Endereço completo:")

    cliente = PessoaFisica(nome = nome, data_nascimento = data_nascimento, cpf = cpf, endereco = endereco)
    clientes.append(cliente)

    sucesso("Cliente adicionado!")

def buscar_cliente(cpf, clientes):
    clientes_encontrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_encontrados[0] if clientes_encontrados else None

def proxima_conta(clientes):
    max = 0
    for cliente in clientes:
        for conta in cliente.contas:
            max = conta.numero if conta.numero > max else max
    max += 1
    return max

def criar_conta(clientes, agencia):
    numero = proxima_conta(clientes)
    cpf = input("Informe o CPF: ")
    cliente = buscar_cliente(cpf, clientes)
    if cliente:
        conta = ContaCorrente(agencia, numero, cliente, 500, LIMITE_SAQUES)
        cliente.contas.append(conta)
        sucesso("Conta criada com sucesso.")
    else:
        erro("Erro! Cliente não encontrado")


def listar_cadastros(clientes):
    title(" CADASTROS ")
    for cliente in clientes:
        print(f"{cliente.nome}".ljust(LARGURA_TELA," "))
        for conta in cliente.contas:
            print(f"AG {conta.agencia}  CC {conta.numero}".rjust(LARGURA_TELA," "))
    footer()


def extrato(conta):
    global LARGURA_TELA
    title("EXTRATO")
    if not len(conta.historico.transacoes):
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in conta.historico.transacoes:
            extrato = f"{transacao.data} ".ljust(LARGURA_TELA//2)
            extrato += f" R$ {transacao.valor:.2f} ({('+' if isinstance(transacao, Deposito)  else '-')})".rjust(LARGURA_TELA//2)
            print(extrato)
    print(f"Saldo: R$ {conta.saldo:.2f}".rjust(LARGURA_TELA," "))
    footer()


def title(text):
    print("\n"+ f" {text} ".center(LARGURA_TELA,"="))
def footer():
    print("".center(LARGURA_TELA,"="))
def erro(text):
    print("".center(LARGURA_TELA,"#"))
    print(text.center(LARGURA_TELA," "))
    print("".center(LARGURA_TELA,"#"))
def sucesso(text):
    print("".center(LARGURA_TELA,"-"))
    print(text.center(LARGURA_TELA," "))
    print("".center(LARGURA_TELA,"-"))

main()