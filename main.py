menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
LARGURA_EXTRATO = 60

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor para depósito: "))

        if valor > 0:
            saldo += valor
            extrato += "Depósito ".ljust(LARGURA_EXTRATO//2)
            extrato +=  f" R$ {valor:.2f} (+)".rjust(LARGURA_EXTRATO//2)
            extrato += "\n"

        else:
            print("Valor informado é inválido.")

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))

        if valor > saldo:
            print("Erro! Ssaldo suficiente.")

        elif valor > limite:
            print("Erro! saque excede o limite.")

        elif numero_saques >= LIMITE_SAQUES:
            print("Erro! Você chegou ao limite de saques.")

        elif valor > 0:
            saldo -= valor
            extrato += "Saque ".ljust(LARGURA_EXTRATO//2)
            extrato += f" R$ {valor:.2f} (-)".rjust(LARGURA_EXTRATO//2)
            extrato += "\n"
            numero_saques += 1

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "e":
        print("\n"+ " EXTRATO ".center(LARGURA_EXTRATO,"="))
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"Saldo: R$ {saldo:.2f}".rjust(LARGURA_EXTRATO," "))
        print("".center(LARGURA_EXTRATO,"="))

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")