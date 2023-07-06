
LARGURA_TELA = 60
LIMITE_SAQUES = 3
AGENCIA = "0001"

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
            Usuário: {conta_ativa['usuario']['nome']}
            Conta: {conta_ativa['numero'] }

            [d] Depositar
            [s] Sacar
            [x] Extrato
            [v] Voltar

            => """
    return input(menu)


def menu_contas(contas):
    title("SELECIONAR CONTA")
    cpf = input("informe o cpf: ")
    conta_f = buscar_conta(cpf, contas)
    
    if(len(conta_f) == 1):
        return conta_f[0]
    
    if(len(conta_f) == 0):
        print("Erro! Conta não cadastrada para usuário")
        return None

    print("Contas encontradas para o usuario: ")
    for conta in conta_f:
        print(f"AG {conta['agencia']} CC {conta['numero']}")
    print("")
    numero = int(input("Digite o número da conta para ativar:"))
    
    for conta in contas:
        if conta["numero"] == numero:
            return conta
        
    erro("Erro! Conta não encontrada")

def main():

    usuarios = []
    contas = []
    conta_ativa = None

    while True:
        opcao = menu(conta_ativa)        
        if opcao == "d":
            valor = float(input("Informe o valor para depósito: "))
            deposito(conta_ativa, valor)
        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saque (conta = conta_ativa, valor=valor)
        elif opcao == "e":
            conta_ativa = menu_contas(contas)
        elif opcao == "x":
            extrato(conta_ativa["saldo"], extrato = conta_ativa["extrato"])
        elif opcao == "c":
            criar_usuario(usuarios)
        elif opcao == "n":
            criar_conta(usuarios, contas, AGENCIA)
        elif opcao == "l":
            listar_cadastros(usuarios, contas)
        elif opcao == "v":
            conta_ativa = None
        elif opcao == "q":
            break

        else:
            erro("Operação inválida, por favor selecione novamente a operação desejada.")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = buscar_usuario(cpf, usuarios)
    if usuario:
        erro("Erro! Usuário já cadastrado")
        return
    
    nome = input("Nome: ")
    data_nascimento = input("Data de nascimento : ")
    endereco = input("Endereço completo:")

    usuarios.append({"nome" : nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    sucesso("Usuário adicionado!")

def buscar_usuario(cpf, usuarios):
    usuarios_encontrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_encontrados[0] if usuarios_encontrados else None

def buscar_conta(cpf, contas):
    return [conta for conta in contas if conta["usuario"]["cpf"] == cpf]

def criar_conta(usuarios, contas, agencia):
    numero = (contas[-1]['numero'] if len(contas) else 0) +1
    cpf = input("Informe o CPF: ")
    usuario = buscar_usuario(cpf, usuarios)
    if usuario:
        contas.append({"numero": numero, "agencia": agencia, "usuario": usuario, "saldo": 0.0, "numero_saques" : 0, "limite" : 500, "extrato" : ""})
        sucesso("Conta criada com sucesso.")
    else:
        erro("Erro! Usuário não encontrado")


def listar_cadastros(usuarios, contas):
    title(" CADASTROS ")
    for usuario in usuarios:
        print(f"{usuario['nome']}".ljust(LARGURA_TELA," "))
        contas_f = buscar_conta(usuario['cpf'], contas)
        for conta in contas_f:
            print(f"AG {conta['agencia']}  CC {conta['numero']}".rjust(LARGURA_TELA," "))
    footer()


def saque(*, conta, valor):
    global LIMITE_SAQUES
    if valor > conta["saldo"]:
        erro("Erro! Saldo suficiente.")

    elif valor > conta["limite"]:
        erro("Erro! Saque excede o limite.")

    elif conta["numero_saques"] >= LIMITE_SAQUES:
        erro("Erro! Você chegou ao limite de saques.")

    elif valor > 0:
        conta["saldo"] -= valor
        conta["extrato"] += "Saque ".ljust(LARGURA_TELA//2)
        conta["extrato"] += f" R$ {valor:.2f} (-)".rjust(LARGURA_TELA//2)
        conta["extrato"] += "\n"
        conta["numero_saques"] += 1

    else:
        erro("Operação falhou! O valor informado é inválido.")
    return conta["saldo"], conta["extrato"]

def deposito(conta, valor, /):
    global LARGURA_TELA
    if valor > 0:
        conta["saldo"] += valor
        conta["extrato"] += "Depósito ".ljust(LARGURA_TELA//2)
        conta["extrato"] +=  f" R$ {valor:.2f} (+)".rjust(LARGURA_TELA//2)
        conta["extrato"] += "\n"

    else:
        erro("Erro! Valor informado é inválido.")

    return conta["saldo"], conta["extrato"]


def extrato(saldo, /, *, extrato):
    title("EXTRATO")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"Saldo: R$ {saldo:.2f}".rjust(LARGURA_TELA," "))
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