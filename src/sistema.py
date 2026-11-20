from datetime import datetime
from .dados import carregar_dados_iniciais

try:
    from .estruturas import (
        ocorrencias,
        adicionar_ocorrencia,
        buscar_por_codigo,
        atualizar_status_estrutura,
        consultar_historico_codigo
    )
    from .indicadores import exibir_indicadores
except ImportError:
    from estruturas import (
        ocorrencias,
        adicionar_ocorrencia,
        buscar_por_codigo,
        atualizar_status_estrutura,
        consultar_historico_codigo
    )
    from indicadores import exibir_indicadores
    from dados import carregar_dados_iniciais

# CATEGORIAS DISPONÍVEIS
CATEGORIAS = {
    1: "Iluminação",
    2: "Acessibilidade",
    3: "Limpeza",
    4: "Conservação"
}

# STATUS DISPONÍVEIS
STATUS = {
    1: "Aberta",
    2: "Em análise",
    3: "Concluída"
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


# 4. EXIBIR UMA OCORRÊNCIA
def exibir_ocorrencia(ocorrencia):

    print("\n" + "-" * 45)

    print(f"Código: {ocorrencia['codigo']}")
    print(f"Categoria: {ocorrencia['categoria']}")
    print(f"Descrição: {ocorrencia['descricao']}")
    print(f"Localidade: {ocorrencia['localidade']}")
    print(f"Data de abertura: {ocorrencia['data_abertura']}")
    print(f"Status: {ocorrencia['status']}")


# 5. CADASTRAR OCORRÊNCIA
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

    # Adicionar ocorrência e atualizar todas as estruturas

    sucesso, mensagem = adicionar_ocorrencia(nova_ocorrencia)

    if not sucesso:
        print(f"\nERRO: {mensagem}")
        return

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


# 6. LISTAR OCORRÊNCIAS
def listar_ocorrencias():

    print("\n" + "=" * 45)
    print("          LISTA DE OCORRÊNCIAS")
    print("=" * 45)

    if len(ocorrencias) == 0:

        print("\nNenhuma ocorrência cadastrada.")
        print("Utilize a opção 1 para registrar uma nova ocorrência.")

    else:

        for ocorrencia in ocorrencias:

            exibir_ocorrencia(ocorrencia)

        print("\n" + "=" * 45)
        print(f"Total de ocorrências cadastradas: {len(ocorrencias)}")
        print("=" * 45)


# 7. PESQUISAR OCORRÊNCIA PELO CÓDIGO
def pesquisar_ocorrencia():

    print("\n" + "=" * 45)
    print("         PESQUISA DE OCORRÊNCIA")
    print("=" * 45)

    codigo = input("\nDigite o código (exemplo: OC001): ").strip()

    if not codigo:
        print("\nERRO: informe o código da ocorrência.")
        return

    # A busca usa o dicionário, sem percorrer a lista inteira
    ocorrencia = buscar_por_codigo(codigo)

    if ocorrencia is None:
        print(f"\nOcorrência {codigo.upper()} não encontrada.")
        print("Confira o código ou use a opção 2 para ver a lista.")
        return

    exibir_ocorrencia(ocorrencia)

    # Mostrar o histórico, do evento mais recente ao mais antigo
    historico = consultar_historico_codigo(codigo)

    print("\nHistórico (do mais recente ao mais antigo):")

    if len(historico) == 0:
        print("Nenhum evento registrado.")

    for evento in historico:

        if evento["status_anterior"] is None:
            mudanca = f"{evento['acao']} -> {evento['status_novo']}"
        else:
            mudanca = (
                f"{evento['acao']}: {evento['status_anterior']} "
                f"-> {evento['status_novo']}"
            )

        print(f"{evento['data_hora']} | {mudanca}")

    print("=" * 45)


# 8. FILTRAR OCORRÊNCIAS
def filtrar_ocorrencias():

    print("\n" + "=" * 45)
    print("         FILTRAR OCORRÊNCIAS")
    print("=" * 45)

    print("1 - Por categoria")
    print("2 - Por status")
    print("0 - Voltar")

    tipo = input("\nEscolha o tipo de filtro: ").strip()

    if tipo == "1":

        print("\nCategorias disponíveis:")

        for indice, categoria in CATEGORIAS.items():
            print(f"{indice} - {categoria}")

        escolha = input("\nDigite o número da categoria: ").strip()

        if not escolha.isdigit() or int(escolha) not in CATEGORIAS:
            print("\nERRO: categoria não encontrada.")
            print("Escolha uma opção entre 1 e 4.")
            return

        campo = "categoria"
        valor = CATEGORIAS[int(escolha)]

    elif tipo == "2":

        print("\nStatus disponíveis:")

        for indice, status in STATUS.items():
            print(f"{indice} - {status}")

        escolha = input("\nDigite o número do status: ").strip()

        if not escolha.isdigit() or int(escolha) not in STATUS:
            print("\nERRO: status não encontrado.")
            print("Escolha uma opção entre 1 e 3.")
            return

        campo = "status"
        valor = STATUS[int(escolha)]

    elif tipo == "0":

        return

    else:

        print("\nERRO: opção inválida.")
        print("Digite 1, 2 ou 0.")
        return

    encontradas = 0

    print("\n" + "=" * 45)
    print(f"   RESULTADO DO FILTRO: {valor}")
    print("=" * 45)

    for ocorrencia in ocorrencias:

        if ocorrencia[campo] == valor:

            exibir_ocorrencia(ocorrencia)
            encontradas += 1

    if encontradas == 0:

        print("\nNenhuma ocorrência encontrada para este filtro.")

    else:

        print("\n" + "=" * 45)
        print(f"Total encontrado: {encontradas}")
        print("=" * 45)


# 9. ATUALIZAR STATUS
def atualizar_status():

    print("\n" + "=" * 45)
    print("          ATUALIZAR STATUS")
    print("=" * 45)

    codigo = input("\nDigite o código (exemplo: OC001): ").strip()

    ocorrencia = buscar_por_codigo(codigo)

    if ocorrencia is None:
        print(f"\nOcorrência {codigo.upper()} não encontrada.")
        print("Confira o código ou use a opção 2 para ver a lista.")
        return

    print(f"\nStatus atual: {ocorrencia['status']}")

    print("\nNovo status:")

    for indice, status in STATUS.items():
        print(f"{indice} - {status}")

    escolha = input("\nDigite o número do novo status: ").strip()

    if not escolha.isdigit() or int(escolha) not in STATUS:
        print("\nERRO: status não encontrado.")
        print("Escolha uma opção entre 1 e 3.")
        return

    # Atualiza o status e registra o evento no histórico
    sucesso, mensagem = atualizar_status_estrutura(
        codigo,
        STATUS[int(escolha)]
    )

    if not sucesso:
        print(f"\nERRO: {mensagem}")
        return

    print(f"\n{mensagem}")


# 10. SISTEMA PRINCIPAL
def iniciar_sistema():
    resumo = carregar_dados_iniciais()

    print(
        f"Dados carregados: "
        f"{resumo['ocorrencias_carregadas']} ocorrências e "
        f"{resumo['eventos_carregados']} eventos de histórico."
    )

    for aviso in resumo["avisos"]:
        print(f"Aviso: {aviso}")
    while True:

        exibir_menu()

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":

            cadastrar_ocorrencia()

        elif opcao == "2":

            listar_ocorrencias()

        elif opcao == "3":

            pesquisar_ocorrencia()

        elif opcao == "4":

            filtrar_ocorrencias()

        elif opcao == "5":

            atualizar_status()

        elif opcao == "6":

            exibir_indicadores()

        elif opcao == "0":

            print("\nSistema encerrado. Obrigada por utilizar o Neighborhood Action Dashboard!")

            break

        else:

            print("\nERRO: opção inválida.")
            print("Digite um número entre 0 e 6.")


# EXECUÇÃO DO PROGRAMA
if __name__ == "__main__":

    iniciar_sistema()
