import textwrap
from datetime import datetime

def menu():
    menu = """\n
    ================ MENU ================
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Criar nova conta
    [lc] Listar contas
    [nu] Cadastrar novo usuário
    [q] Sair
    => """
    return input(textwrap.dedent(menu))


def filtrar_usuario(cpf, usuarios):
    """ Busca um usuário pelo CPF e retorna os dados se encontrado. """
    return next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)


def filtrar_conta_por_cpf(cpf, contas):
    """ Busca conta pelo CPF do titular. """
    return next((conta for conta in contas if conta["usuario"]["cpf"] == cpf), None)


def depositar(saldo, valor, extrato, contas):
    cpf = input("Digite o CPF do titular da conta: ")
    conta = filtrar_conta_por_cpf(cpf, contas)

    if not conta:
        print("\nNão encontramos nenhuma conta vinculada a este CPF. Verifique-se de que digitou corretamente ou crie uma nova conta.")
        return saldo, extrato

    if valor > 0:
        saldo += valor
        extrato += f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Depósito: R$ {valor:.2f}\n"
        print("\nDepósito realizado com sucesso! Obrigado por ser nosso cliente.")
    else:
        print("\nO valor informado é inválido. Tente novamente com um número maior que zero porfavor.")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor > saldo:
        print("\nSaque não realizado! Seu saldo é insuficiente.")
    elif valor > limite:
        print("\nO valor solicitado excede o limite permitido para saque.")
    elif numero_saques >= limite_saques:
        print("\nVocê atingiu o número máximo de saques diários.")
    elif valor > 0:
        saldo -= valor
        extrato += f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("\nSaque realizado com sucesso!")
    else:
        print("\nO valor informado é inválido. Digite um número positivo.")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    if not extrato:
        print("Não há movimentações na conta.")
    else:
        print(extrato)
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("\nObrigado por ser nosso cliente!")
    print("==========================================")


def criar_usuario(usuarios):
    cpf = input("Digite o CPF (apenas números): ")
    if filtrar_usuario(cpf, usuarios):
        print("\nJá existe um usuário cadastrado com esse CPF.")
        return

    nome = input("Digite o nome completo: ")
    data_nascimento = input("Digite a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Digite o endereço (rua, número - bairro - cidade/estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("\nUsuário cadastrado com sucesso!")


def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("Digite o CPF do titular da conta: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        conta = {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
        contas.append(conta)
        print("\nConta criada com sucesso! Agora você pode realizar depósitos e saques.")
    else:
        print("\nCPF não encontrado. Certifique-se de que o usuário foi cadastrado antes de criar a conta.")


def listar_contas(contas):
    if not contas:
        print("\nNenhuma conta cadastrada no momento.")
        return

    for conta in contas:
        linha = f"""\
            Agência: {conta['agencia']}
            Conta: {conta['numero_conta']}
            Titular: {conta['usuario']['nome']}
        """
        print("=" * 50)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Digite o valor que deseja depositar: "))
            saldo, extrato = depositar(saldo, valor, extrato, contas)

        elif opcao == "s":
            valor = float(input("Digite o valor que deseja sacar: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(AGENCIA, numero_conta, usuarios, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("\nObrigado por usar nosso sistema bancário! Até a próxima.")
            break

        else:
            print("\nOpção inválida! Escolha uma opção do menu.")


if _name_ == "_main_":
    main()