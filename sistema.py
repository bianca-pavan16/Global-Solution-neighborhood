


from dados import ocorrencias
from datetime import datetime


# CATEGORIAS DISPONÍVEIS
CATEGORIAS = {
    1: "Iluminação",
    2: "Acessibilidade",
    3: "Limpeza",
    4: "Conservação"
}


# 1. GERAR CÓDIGO AUTOMATICAMENTE
def gerar_codigo():

    maior_numero = 0

    for ocorrencia in ocorrencias:

        numero = int(ocorrencia["codigo"][2:])

        if numero > maior_numero:
            maior_numero = numero

    novo_numero = maior_numero + 1

    return f"OC{novo_numero:03d}"


# 2. VALIDAR DATA
def validar_data(data):

    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True

    except ValueError:
        return False


# 3. MENU PRINCIPAL
def exibir_menu():

    print("\n" + "=" * 45)
    print("       NEIGHBORHOOD ACTION DASHBOARD")
    print("=" * 45)

    print("1 - Cadastrar ocorrência")
    print("2 - Listar ocorrências")
    print("3 - Pesquisar ocorrência")
    print("4 - Filtrar ocorrências")
    print("5 - Atualizar status")
    print("6 - Consultar indicadores")
    print("0 - Sair")

    print("=" * 45)


# 4. CADASTRAR OCORRÊNCIA
def cadastrar_ocorrencia():

    print("\n" + "=" * 45)
    print("         CADASTRO DE OCORRÊNCIA")
    print("=" * 45)

    # Selecionar categoria
    print("\nCategorias disponíveis:")

    for indice, categoria in CATEGORIAS.items():
        print(f"{indice} - {categoria}")

    opcao_categoria = input(
        "\nDigite o número da categoria: "
    ).strip()

    if not opcao_categoria.isdigit():
        print("\nERRO: informe o número de uma categoria.")
        print("Exemplo: digite 1 para Iluminação.")
        return

    opcao_categoria = int(opcao_categoria)

    if opcao_categoria not in CATEGORIAS:
        print("\nERRO: categoria não encontrada.")
        print("Escolha uma opção entre 1 e 4.")
        return

    categoria = CATEGORIAS[opcao_categoria]

    # Solicitar informações
    descricao = input("\nDescrição da ocorrência: ").strip()

    localidade = input("Localidade genérica: ").strip()

    data_abertura = input(
        "Data de abertura (DD/MM/AAAA): "
    ).strip()

    # Validar campos obrigatórios
    if not descricao or not localidade or not data_abertura:
        print("\nERRO: existem campos obrigatórios vazios.")
        print("Preencha a descrição, a localidade e a data.")
        return

    # Validar formato e existência da data
    if not validar_data(data_abertura):
        print("\nERRO: data inválida.")
        print("Informe uma data real no formato DD/MM/AAAA.")
        print("Exemplo: 16/11/2026.")
        return

    # Gerar código após validar os dados
    codigo = gerar_codigo()

    # Criar dicionário da ocorrência
    nova_ocorrencia = {
        "codigo": codigo,
        "categoria": categoria,
        "descricao": descricao,
        "localidade": localidade,
        "data_abertura": data_abertura,
        "status": "Aberta"
    }

    # Adicionar ocorrência à lista principal
    ocorrencias.append(nova_ocorrencia)

    # Confirmar cadastro
    print("\n" + "=" * 45)
    print("     OCORRÊNCIA CADASTRADA COM SUCESSO!")
    print("=" * 45)

    print(f"Código: {codigo}")
    print(f"Categoria: {categoria}")
    print(f"Descrição: {descricao}")
    print(f"Localidade: {localidade}")
    print(f"Data de abertura: {data_abertura}")
    print("Status inicial: Aberta")

    print("=" * 45)
    print("Guarde o código para consultar a ocorrência.")


# 5. LISTAR OCORRÊNCIAS
def listar_ocorrencias():

    print("\n" + "=" * 45)
    print("          LISTA DE OCORRÊNCIAS")
    print("=" * 45)

    if len(ocorrencias) == 0:

        print("\nNenhuma ocorrência cadastrada.")
        print("Utilize a opção 1 para registrar uma nova ocorrência.")

    else:

        for ocorrencia in ocorrencias:

            print("\n" + "-" * 45)

            print(f"Código: {ocorrencia['codigo']}")
            print(f"Categoria: {ocorrencia['categoria']}")
            print(f"Descrição: {ocorrencia['descricao']}")
            print(f"Localidade: {ocorrencia['localidade']}")
            print(f"Data de abertura: {ocorrencia['data_abertura']}")
            print(f"Status: {ocorrencia['status']}")

        print("\n" + "=" * 45)
        print(f"Total de ocorrências cadastradas: {len(ocorrencias)}")
        print("=" * 45)


# 6. SISTEMA PRINCIPAL
def iniciar_sistema():

    while True:

        exibir_menu()

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":

            cadastrar_ocorrencia()

        elif opcao == "2":

            listar_ocorrencias()

        elif opcao == "3":

            print("\nFuncionalidade de pesquisa em integração.")

        elif opcao == "4":

            print("\nFuncionalidade de filtros em integração.")

        elif opcao == "5":

            print("\nFuncionalidade de atualização em integração.")

        elif opcao == "6":

            print("\nFuncionalidade de indicadores em integração.")

        elif opcao == "0":

            print("\nSistema encerrado. Obrigada por utilizar o Neighborhood Action Dashboard!")

            break

        else:

            print("\nERRO: opção inválida.")
            print("Digite um número entre 0 e 6.")


# EXECUÇÃO DO PROGRAMA
if __name__ == "__main__":

    iniciar_sistema()
