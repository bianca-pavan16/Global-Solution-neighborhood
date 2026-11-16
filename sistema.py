

from dados import ocorrencias


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


# 2. MENU PRINCIPAL
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


# 3. CADASTRAR OCORRÊNCIA
def cadastrar_ocorrencia():

    print("\n--- CADASTRO DE OCORRÊNCIA ---")

    # Gerar código automaticamente
    codigo = gerar_codigo()

    print("Código gerado:", codigo)

    # Exibir categorias disponíveis
    print("\nSelecione a categoria:")

    for indice, categoria in CATEGORIAS.items():
        print(f"{indice} - {categoria}")

    opcao_categoria = input(
        "Digite o número da categoria: "
    ).strip()

    # Validar se a entrada é numérica
    if not opcao_categoria.isdigit():
        print("Erro: digite um número válido.")
        return

    opcao_categoria = int(opcao_categoria)

    # Validar se a categoria existe
    if opcao_categoria not in CATEGORIAS:
        print("Erro: categoria inexistente.")
        return

    # Recuperar nome da categoria
    categoria = CATEGORIAS[opcao_categoria]

    # Solicitar demais informações
    descricao = input("Descrição: ").strip()

    localidade = input("Localidade genérica: ").strip()

    data_abertura = input(
        "Data de abertura (DD/MM/AAAA): "
    ).strip()

    # Validar campos obrigatórios
    if descricao == "" or localidade == "" or data_abertura == "":
        print("Erro: todos os campos são obrigatórios.")
        return

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

    print("\nOcorrência cadastrada com sucesso!")
    print("Código:", codigo)
    print("Categoria:", categoria)


# 4. LISTAR OCORRÊNCIAS
def listar_ocorrencias():

    print("\n--- LISTA DE OCORRÊNCIAS ---")

    # Verificar se existem registros
    if len(ocorrencias) == 0:

        print("Nenhuma ocorrência cadastrada.")

    else:

        for ocorrencia in ocorrencias:

            print("\n" + "-" * 40)

            print("Código:", ocorrencia["codigo"])
            print("Categoria:", ocorrencia["categoria"])
            print("Descrição:", ocorrencia["descricao"])
            print("Localidade:", ocorrencia["localidade"])
            print("Data de abertura:", ocorrencia["data_abertura"])
            print("Status:", ocorrencia["status"])

        print("\n" + "-" * 40)
        print("Total de ocorrências:", len(ocorrencias))


# 5. SISTEMA PRINCIPAL
def iniciar_sistema():

    while True:

        exibir_menu()

        opcao = input("Escolha uma opção: ").strip()

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

            print("\nEncerrando o sistema. Até mais!")
            break

        else:

            print("\nOpção inválida. Escolha uma opção de 0 a 6.")


# EXECUÇÃO DO PROGRAMA
if __name__ == "__main__":

    iniciar_sistema()
