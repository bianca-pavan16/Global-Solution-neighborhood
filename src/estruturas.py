"""
Estruturas de dados do Neighborhood Action Dashboard.

Este arquivo mantém:
- a lista de ocorrências;
- a fila de demandas aguardando análise;
- a pilha de histórico;
- o dicionário de busca por código;
- a hierarquia localidade -> categoria -> ocorrências.
"""

from datetime import datetime


# ============================================================
# VALORES ACEITOS PELO SISTEMA
# ============================================================

CATEGORIAS_VALIDAS = [
    "Iluminação",
    "Acessibilidade",
    "Limpeza",
    "Conservação"
]

STATUS_VALIDOS = [
    "Aberta",
    "Em análise",
    "Concluída"
]


# ============================================================
# ESTRUTURAS DE DADOS
# ============================================================

# Lista com todas as ocorrências cadastradas.
ocorrencias = []

# Fila com os códigos das demandas que ainda aguardam análise.
# A fila segue a regra FIFO: primeiro a entrar, primeiro a sair.
fila_analise = []

# Pilha com os eventos de cadastro e atualização.
# A pilha segue a regra LIFO: último a entrar, primeiro a sair.
pilha_historico = []

# Dicionário usado para encontrar uma ocorrência pelo código.
ocorrencias_por_codigo = {}

# Hierarquia:
# localidade -> categoria -> ocorrências
hierarquia_bairros = {}


# ============================================================
# VALIDAÇÃO E PADRONIZAÇÃO
# ============================================================

def validar_ocorrencia(ocorrencia):
    """
    Verifica os campos obrigatórios e os valores
    informados em uma ocorrência.
    """

    if not isinstance(ocorrencia, dict):
        return False, "A ocorrência deve ser um dicionário."

    campos_obrigatorios = [
        "codigo",
        "categoria",
        "descricao",
        "localidade",
        "data_abertura",
        "status"
    ]

    for campo in campos_obrigatorios:
        if campo not in ocorrencia:
            return False, (
                f"O campo obrigatório '{campo}' não foi informado."
            )

        valor = ocorrencia[campo]

        # A condição usa OR e NOT.
        # O campo é inválido se não for texto ou estiver vazio.
        if not isinstance(valor, str) or not valor.strip():
            return False, (
                f"O campo '{campo}' deve ser preenchido."
            )

    codigo = ocorrencia["codigo"].strip().upper()
    categoria = ocorrencia["categoria"].strip()
    status = ocorrencia["status"].strip()
    data_abertura = ocorrencia["data_abertura"].strip()

    # As três condições precisam ser verdadeiras.
    codigo_valido = (
        codigo.startswith("OC")
        and len(codigo) == 5
        and codigo[2:].isdigit()
    )

    if not codigo_valido:
        return False, "Código inválido. Use o formato OC001."

    if categoria not in CATEGORIAS_VALIDAS:
        return False, f"Categoria inválida: {categoria}."

    if status not in STATUS_VALIDOS:
        return False, f"Status inválido: {status}."

    try:
        datetime.strptime(data_abertura, "%d/%m/%Y")
    except ValueError:
        return False, (
            "Data inválida. Use o formato DD/MM/AAAA."
        )

    return True, "Ocorrência válida."


def normalizar_ocorrencia(ocorrencia):
    """
    Remove espaços extras e deixa o código em letras maiúsculas.
    """

    ocorrencia["codigo"] = (
        ocorrencia["codigo"].strip().upper()
    )
    ocorrencia["categoria"] = (
        ocorrencia["categoria"].strip()
    )
    ocorrencia["descricao"] = (
        ocorrencia["descricao"].strip()
    )
    ocorrencia["localidade"] = (
        ocorrencia["localidade"].strip()
    )
    ocorrencia["data_abertura"] = (
        ocorrencia["data_abertura"].strip()
    )
    ocorrencia["status"] = (
        ocorrencia["status"].strip()
    )

    return ocorrencia


# ============================================================
# BUSCA POR CÓDIGO
# ============================================================

def buscar_por_codigo(codigo):
    """
    Procura uma ocorrência pelo código.

    Retorna a ocorrência encontrada ou None.
    """

    if not isinstance(codigo, str) or not codigo.strip():
        return None

    codigo = codigo.strip().upper()

    return ocorrencias_por_codigo.get(codigo)


# ============================================================
# FILA DE DEMANDAS
# ============================================================

def enfileirar_demanda(codigo):
    """
    Coloca o código de uma ocorrência no final da fila.
    """

    if not isinstance(codigo, str):
        return False

    codigo = codigo.strip().upper()

    if codigo not in ocorrencias_por_codigo:
        return False

    if codigo not in fila_analise:
        fila_analise.append(codigo)

    return True


def remover_da_fila(codigo):
    """
    Remove o código de uma ocorrência da fila.
    """

    if not isinstance(codigo, str):
        return False

    codigo = codigo.strip().upper()

    if codigo not in fila_analise:
        return False

    fila_analise.remove(codigo)

    return True


def desenfileirar_demanda():
    """
    Remove e retorna o primeiro código da fila.

    Esta função demonstra o funcionamento FIFO.
    """

    if len(fila_analise) == 0:
        return None

    return fila_analise.pop(0)


def consultar_proxima_demanda():
    """
    Retorna a primeira ocorrência da fila sem removê-la.
    """

    if len(fila_analise) == 0:
        return None

    primeiro_codigo = fila_analise[0]

    return buscar_por_codigo(primeiro_codigo)


def listar_fila_analise():
    """
    Retorna as ocorrências que ainda aguardam análise.
    """

    demandas = []

    for codigo in fila_analise:
        ocorrencia = buscar_por_codigo(codigo)

        if ocorrencia is not None:
            demandas.append(ocorrencia)

    return demandas


def atualizar_fila(ocorrencia):
    """
    Atualiza a fila conforme o status da ocorrência.

    Uma ocorrência aberta aguarda análise e fica na fila.
    Uma ocorrência em análise ou concluída sai da fila.
    """

    codigo = ocorrencia["codigo"]
    status = ocorrencia["status"]

    if status == "Aberta":
        enfileirar_demanda(codigo)
    else:
        remover_da_fila(codigo)


# ============================================================
# PILHA DE HISTÓRICO
# ============================================================

def criar_evento_historico(
    codigo,
    acao,
    status_anterior=None,
    status_novo=None,
    observacao=""
):
    """
    Cria um evento de histórico com data e horário.
    """

    evento = {
        "codigo": codigo.strip().upper(),
        "acao": acao,
        "status_anterior": status_anterior,
        "status_novo": status_novo,
        "data_hora": datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        ),
        "observacao": observacao
    }

    return evento


def empilhar_historico(evento):
    """
    Coloca um evento no topo da pilha.
    """

    if not isinstance(evento, dict):
        return False

    campos_obrigatorios = [
        "codigo",
        "acao",
        "data_hora"
    ]

    for campo in campos_obrigatorios:
        if campo not in evento:
            return False

    pilha_historico.append(evento)

    return True


def desempilhar_historico():
    """
    Remove e retorna o evento mais recente da pilha.

    Esta função demonstra o funcionamento LIFO.
    """

    if len(pilha_historico) == 0:
        return None

    return pilha_historico.pop()


def consultar_ultimo_evento():
    """
    Retorna o evento mais recente sem removê-lo.
    """

    if len(pilha_historico) == 0:
        return None

    return pilha_historico[-1]


def consultar_historico_codigo(codigo):
    """
    Retorna o histórico de uma ocorrência.

    Os eventos mais recentes aparecem primeiro.
    """

    if not isinstance(codigo, str):
        return []

    codigo = codigo.strip().upper()
    historico_encontrado = []

    for evento in reversed(pilha_historico):
        if evento["codigo"] == codigo:
            historico_encontrado.append(evento)

    return historico_encontrado


def listar_historico():
    """
    Retorna todos os eventos, começando pelo mais recente.
    """

    return list(reversed(pilha_historico))


# ============================================================
# HIERARQUIA
# ============================================================

def adicionar_na_hierarquia(ocorrencia):
    """
    Organiza uma ocorrência na estrutura:

    localidade -> categoria -> ocorrências
    """

    localidade = ocorrencia["localidade"]
    categoria = ocorrencia["categoria"]

    # Cria a localidade caso ainda não exista.
    if localidade not in hierarquia_bairros:
        hierarquia_bairros[localidade] = {}

    # Cria a categoria dentro da localidade.
    if categoria not in hierarquia_bairroshierarquia_bairros[localidade][categoria] = []

    lista_categoria = (
        hierarquia_bairros[localidade][categoria]
    )

    # Evita adicionar a mesma ocorrência duas vezes.
    if ocorrencia not in lista_categoria:
        lista_categoria.append(ocorrencia)

    return True


def remover_da_hierarquia(ocorrencia):
    """
    Remove uma ocorrência da hierarquia.
    """

    if not isinstance(ocorrencia, dict):
        return False

    localidade = ocorrencia.get("localidade")
    categoria = ocorrencia.get("categoria")

    if localidade not in hierarquia_bairros:
        return False

    categorias_localidade = hierarquia_bairros[localidade]

    if categoria not in categorias_localidade:
        return False

    lista_categoria = categorias_localidade[categoria]

    if ocorrencia not in lista_categoria:
        return False

    lista_categoria.remove(ocorrencia)

    # Remove a categoria se não houver mais ocorrências.
    if len(lista_categoria) == 0:
        del categorias_localidade[categoria]

    # Remove a localidade se não houver mais categorias.
    if len(categorias_localidade) == 0:
        del hierarquia_bairros[localidade]

    return True


def consultar_por_bairro(localidade):
    """
    Retorna as categorias e ocorrências de uma localidade.
    """

    if not isinstance(localidade, str):
        return {}

    localidade = localidade.strip()

    if not localidade:
        return {}

    return hierarquia_bairros.get(localidade, {})


def consultar_por_bairro_categoria(
    localidade,
    categoria
):
    """
    Retorna as ocorrências de uma categoria dentro
    de uma localidade.
    """

    if (
        not isinstance(localidade, str)
        or not isinstance(categoria, str)
    ):
        return []

    localidade = localidade.strip()
    categoria = categoria.strip()

    categorias_localidade = hierarquia_bairros.get(
        localidade,
        {}
    )

    return categorias_localidade.get(categoria, [])


# ============================================================
# CADASTRO
# ============================================================

def adicionar_ocorrencia(
    ocorrencia,
    registrar_historico=True
):
    """
    Cadastra uma ocorrência e atualiza as estruturas.

    A função atualiza:
    - lista;
    - fila;
    - pilha;
    - dicionário;
    - hierarquia.
    """

    valida, mensagem = validar_ocorrencia(ocorrencia)

    if not valida:
        return False, mensagem

    normalizar_ocorrencia(ocorrencia)

    codigo = ocorrencia["codigo"]

    if codigo in ocorrencias_por_codigo:
        return False, (
            f"O código {codigo} já está cadastrado."
        )

    # Lista principal.
    ocorrencias.append(ocorrencia)

    # Dicionário de busca.
    ocorrencias_por_codigo[codigo] = ocorrencia

    # Fila de demandas.
    atualizar_fila(ocorrencia)

    # Hierarquia de localidades.
    adicionar_na_hierarquia(ocorrencia)

    # Pilha de histórico.
    if registrar_historico:
        evento = criar_evento_historico(
            codigo=codigo,
            acao="Cadastro",
            status_anterior=None,
            status_novo=ocorrencia["status"],
            observacao="Ocorrência cadastrada."
        )

        empilhar_historico(evento)

    return True, (
        f"Ocorrência {codigo} cadastrada com sucesso."
    )


# ============================================================
# ATUALIZAÇÃO DE STATUS
# ============================================================

def atualizar_status_estrutura(codigo, novo_status):
    """
    Atualiza o status de uma ocorrência.

    A função também atualiza a fila e registra
    a alteração no histórico.
    """

    if not isinstance(codigo, str) or not codigo.strip():
        return False, "Código inválido."

    if (
        not isinstance(novo_status, str)
        or not novo_status.strip()
    ):
        return False, "Status inválido."

    codigo = codigo.strip().upper()
    novo_status = novo_status.strip()

    if novo_status not in STATUS_VALIDOS:
        return False, (
            "O status deve ser Aberta, "
            "Em análise ou Concluída."
        )

    ocorrencia = buscar_por_codigo(codigo)

    if ocorrencia is None:
        return False, (
            f"Ocorrência {codigo} não encontrada."
        )

    status_anterior = ocorrencia["status"]

    if status_anterior == novo_status:
        return False, (
            f"A ocorrência {codigo} já está com "
            f"o status '{novo_status}'."
        )

    ocorrencia["status"] = novo_status

    atualizar_fila(ocorrencia)

    evento = criar_evento_historico(
        codigo=codigo,
        acao="Atualização de status",
        status_anterior=status_anterior,
        status_novo=novo_status,
        observacao=(
            f"Status alterado de '{status_anterior}' "
            f"para '{novo_status}'."
        )
    )

    empilhar_historico(evento)

    return True, (
        f"Status da ocorrência {codigo} atualizado "
        f"para '{novo_status}'."
    )


def iniciar_analise_proxima_demanda():
    """
    Coloca a primeira demanda da fila em análise.
    """

    if len(fila_analise) == 0:
        return False, (
            "Não existem demandas aguardando análise."
        )

    codigo = fila_analise[0]

    return atualizar_status_estrutura(
        codigo,
        "Em análise"
    )


# ============================================================
# RECONSTRUÇÃO DAS ESTRUTURAS
# ============================================================

def reconstruir_estruturas(
    lista_ocorrencias,
    registrar_historico=True
):
    """
    Reconstrói as estruturas usando uma lista de ocorrências.

    Esta função pode ser usada depois da leitura do CSV.
    Registros inválidos são rejeitados e informados.
    """

    if not isinstance(lista_ocorrencias, list):
        return {
            "carregadas": 0,
            "rejeitadas": 1,
            "erros": [
                {
                    "linha": None,
                    "codigo": "DESCONHECIDO",
                    "erro": (
                        "Os dados devem estar em uma lista."
                    )
                }
            ]
        }

    limpar_estruturas()

    quantidade_carregada = 0
    erros = []

    for numero_linha, ocorrencia in enumerate(
        lista_ocorrencias,
        start=1
    ):
        sucesso, mensagem = adicionar_ocorrencia(
            ocorrencia,
            registrar_historico
        )

        if sucesso:
            quantidade_carregada += 1
        else:
            if isinstance(ocorrencia, dict):
                codigo = ocorrencia.get(
                    "codigo",
                    "SEM CÓDIGO"
                )
            else:
                codigo = "REGISTRO INVÁLIDO"

            erros.append({
                "linha": numero_linha,
                "codigo": codigo,
                "erro": mensagem
            })

    return {
        "carregadas": quantidade_carregada,
        "rejeitadas": len(erros),
        "erros": erros
    }


def carregar_eventos_historico(eventos):
    """
    Carrega eventos simulados na pilha de histórico.
    """

    if not isinstance(eventos, list):
        return 0

    quantidade = 0

    for evento in eventos:
        if empilhar_historico(evento):
            quantidade += 1

    return quantidade


# ============================================================
# LIMPEZA E RESUMO
# ============================================================

def limpar_estruturas():
    """
    Limpa todas as estruturas sem trocar os objetos.
    """

    ocorrencias.clear()
    fila_analise.clear()
    pilha_historico.clear()
    ocorrencias_por_codigo.clear()
    hierarquia_bairros.clear()


def obter_resumo_estruturas():
    """
    Retorna a quantidade de itens em cada estrutura.
    """

    total_hierarquia = 0

    for categorias in hierarquia_bairros.values():
        for lista_categoria in categorias.values():
            total_hierarquia += len(lista_categoria)

    return {
        "total_ocorrencias": len(ocorrencias),
        "total_fila": len(fila_analise),
        "total_historico": len(pilha_historico),
        "total_dicionario": len(
            ocorrencias_por_codigo
        ),
        "total_hierarquia": total_hierarquia
    }


# ============================================================
# VERIFICAÇÃO DE CONSISTÊNCIA
# ============================================================

def verificar_consistencia():
    """
    Verifica se as estruturas estão sincronizadas.

    Retorna:
        (True, []), quando estiver tudo correto.
        (False, erros), quando encontrar inconsistências.
    """

    erros = []

    # A lista e o dicionário devem ter a mesma quantidade.
    if len(ocorrencias) != len(ocorrencias_por_codigo):
        erros.append(
            "A lista e o dicionário possuem "
            "quantidades diferentes."
        )

    # Todas as ocorrências da lista devem estar no dicionário.
    for ocorrencia in ocorrencias:
        codigo = ocorrencia["codigo"]

        if codigo not in ocorrencias_por_codigo:
            erros.append(
                f"A ocorrência {codigo} não está "
                "no dicionário."
            )

    # A fila deve conter somente ocorrências abertas.
    for codigo in fila_analise:
        ocorrencia = buscar_por_codigo(codigo)

        if ocorrencia is None:
            erros.append(
                f"O código {codigo} está na fila, "
                "mas não existe no dicionário."
            )
        elif ocorrencia["status"] != "Aberta":
            erros.append(
                f"A ocorrência {codigo} está na fila, "
                "mas não está aberta."
            )

    # Toda ocorrência aberta deve estar na fila.
    for ocorrencia in ocorrencias:
        codigo = ocorrencia["codigo"]

        if (
            ocorrencia["status"] == "Aberta"
            and codigo not in fila_analise
        ):
            erros.append(
                f"A ocorrência aberta {codigo} "
                "não está na fila."
            )

    # Verificar as ocorrências da hierarquia.
    total_hierarquia = 0

    for localidade in hierarquia_bairros:
        categorias = hierarquia_bairros[localidade]

        for categoria in categorias:
            lista_categoria = categorias[categoria]

            for ocorrencia in lista_categoria:
                total_hierarquia += 1

                if ocorrencia not in ocorrencias:
                    erros.append(
                        "A hierarquia possui uma ocorrência "
                        "que não está na lista principal."
                    )

                if ocorrencia["localidade"] != localidade:
                    erros.append(
                        f"A ocorrência "
                        f"{ocorrencia['codigo']} está na "
                        "localidade incorreta."
                    )

                if ocorrencia["categoria"] != categoria:
                    erros.append(
                        f"A ocorrência "
                        f"{ocorrencia['codigo']} está na "
                        "categoria incorreta."
                    )

    if total_hierarquia != len(ocorrencias):
        erros.append(
            "A quantidade da hierarquia é diferente "
            "da quantidade da lista."
        )

    if len(erros) == 0:
        return True, []

    return False, erros
