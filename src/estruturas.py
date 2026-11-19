"""
Estruturas de dados do Neighborhood Action Dashboard.

Mantém a lista de ocorrências, a fila de análise, a pilha de
histórico, o dicionário por código e a hierarquia por localidade.
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

STATUS_VALIDOS = ["Aberta", "Em análise", "Concluída"]
# ============================================================
# ESTRUTURAS DE DADOS
# ============================================================
ocorrencias = []
fila_analise = []
pilha_historico = []
ocorrencias_por_codigo = {}
hierarquia_bairros = {}
# ============================================================
# VALIDAÇÃO E PADRONIZAÇÃO
# ============================================================
def validar_ocorrencia(ocorrencia):
    """Verifica os campos obrigatórios e os valores informados."""
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
            return False, f"O campo '{campo}' não foi informado."
        valor = ocorrencia[campo]
        # Usa OR e NOT para rejeitar campos vazios ou inválidos.
        if not isinstance(valor, str) or not valor.strip():
            return False, f"O campo '{campo}' deve ser preenchido."
    codigo = ocorrencia["codigo"].strip().upper()
    categoria = ocorrencia["categoria"].strip()
    status = ocorrencia["status"].strip()
    data_abertura = ocorrencia["data_abertura"].strip()
    # Usa AND porque as três regras do código são obrigatórias.
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
        return False, "Data inválida. Use o formato DD/MM/AAAA."

    return True, "Ocorrência válida."


def normalizar_ocorrencia(ocorrencia):
    """Remove espaços extras e padroniza os campos."""
    ocorrencia["codigo"] = ocorrencia["codigo"].strip().upper()
    ocorrencia["categoria"] = ocorrencia["categoria"].strip()
    ocorrencia["descricao"] = ocorrencia["descricao"].strip()
    ocorrencia["localidade"] = ocorrencia["localidade"].strip()
    ocorrencia["data_abertura"] = ocorrencia["data_abertura"].strip()
    ocorrencia["status"] = ocorrencia["status"].strip()
    return ocorrencia

# ============================================================
# DICIONÁRIO DE BUSCA
# ============================================================

def buscar_por_codigo(codigo):
    """Busca uma ocorrência diretamente pelo código."""
    if not isinstance(codigo, str) or not codigo.strip():
        return None

    return ocorrencias_por_codigo.get(codigo.strip().upper())

# ============================================================
# FILA DE DEMANDAS
# ============================================================

def enfileirar_demanda(codigo):
    """Coloca uma ocorrência cadastrada no final da fila."""
    if not isinstance(codigo, str) or not codigo.strip():
        return False

    codigo = codigo.strip().upper()

    if codigo not in ocorrencias_por_codigo:
        return False

    if codigo not in fila_analise:
        fila_analise.append(codigo)

    return True


def remover_da_fila(codigo):
    """Remove uma ocorrência da fila."""
    if not isinstance(codigo, str) or not codigo.strip():
        return False

    codigo = codigo.strip().upper()

    if codigo not in fila_analise:
        return False

    fila_analise.remove(codigo)
    return True


def consultar_proxima_demanda():
    """Retorna a primeira ocorrência da fila sem removê-la."""
    if len(fila_analise) == 0:
        return None

    return buscar_por_codigo(fila_analise[0])


def listar_fila_analise():
    """Retorna as ocorrências que aguardam análise."""
    demandas = []

    for codigo in fila_analise:
        ocorrencia = buscar_por_codigo(codigo)

        if ocorrencia is not None:
            demandas.append(ocorrencia)

    return demandas


def atualizar_fila(ocorrencia):
    """Mantém na fila somente ocorrências com status Aberta."""
    codigo = ocorrencia["codigo"]

    if ocorrencia["status"] == "Aberta":
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
    data_hora=None
):
    """Cria um evento para o histórico."""
    if data_hora is None:
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    return {
        "codigo": codigo.strip().upper(),
        "acao": acao,
        "status_anterior": status_anterior,
        "status_novo": status_novo,
        "data_hora": data_hora
    }


def validar_evento_historico(evento):
    """Verifica os campos básicos de um evento."""
    if not isinstance(evento, dict):
        return False

    for campo in ["codigo", "acao", "data_hora"]:
        if campo not in evento:
            return False

        if not isinstance(evento[campo], str) or not evento[campo].strip():
            return False

    return True


def empilhar_historico(evento):
    """Coloca um evento válido no topo da pilha."""
    if not validar_evento_historico(evento):
        return False

    evento["codigo"] = evento["codigo"].strip().upper()
    pilha_historico.append(evento)
    return True


def desempilhar_historico():
    """Remove e retorna o evento mais recente da pilha."""
    if len(pilha_historico) == 0:
        return None

    return pilha_historico.pop()


def consultar_ultimo_evento():
    """Retorna o evento mais recente sem removê-lo."""
    if len(pilha_historico) == 0:
        return None

    return pilha_historico[-1]


def consultar_historico_codigo(codigo):
    """Retorna os eventos de um código, do mais recente ao mais antigo."""
    if not isinstance(codigo, str) or not codigo.strip():
        return []

    codigo = codigo.strip().upper()
    historico = []

    for evento in reversed(pilha_historico):
        if evento["codigo"] == codigo:
            historico.append(evento)

    return historico

# ============================================================
# HIERARQUIA
# ============================================================

def adicionar_na_hierarquia(ocorrencia):
    """Organiza uma ocorrência por localidade e categoria."""
    localidade = ocorrencia["localidade"]
    categoria = ocorrencia["categoria"]

    if localidade not in hierarquia_bairros:
        hierarquia_bairros[localidade] = {}

    if categoria not in hierarquia_bairros[localidade]:
        hierarquia_bairros[localidade][categoria] = []

    lista_categoria = hierarquia_bairros[localidade][categoria]

    if ocorrencia not in lista_categoria:
        lista_categoria.append(ocorrencia)


def consultar_por_bairro(localidade):
    """Retorna as categorias e ocorrências de uma localidade."""
    if not isinstance(localidade, str) or not localidade.strip():
        return {}

    return hierarquia_bairros.get(localidade.strip(), {})


def consultar_por_bairro_categoria(localidade, categoria):
    """Retorna ocorrências de uma categoria e localidade."""
    if not isinstance(localidade, str) or not isinstance(categoria, str):
        return []

    localidade = localidade.strip()
    categoria = categoria.strip()

    if not localidade or not categoria:
        return []

    categorias = hierarquia_bairros.get(localidade, {})
    return categorias.get(categoria, [])

# ============================================================
# CADASTRO E ATUALIZAÇÃO
# ============================================================

def adicionar_ocorrencia(ocorrencia, registrar_historico=True):
    """Cadastra uma ocorrência e atualiza todas as estruturas."""
    valida, mensagem = validar_ocorrencia(ocorrencia)

    if not valida:
        return False, mensagem

    normalizar_ocorrencia(ocorrencia)
    codigo = ocorrencia["codigo"]

    if codigo in ocorrencias_por_codigo:
        return False, f"O código {codigo} já está cadastrado."

    ocorrencias.append(ocorrencia)
    ocorrencias_por_codigo[codigo] = ocorrencia
    atualizar_fila(ocorrencia)
    adicionar_na_hierarquia(ocorrencia)

    if registrar_historico:
        evento = criar_evento_historico(
            codigo,
            "Cadastro",
            None,
            ocorrencia["status"]
        )
        empilhar_historico(evento)

    return True, f"Ocorrência {codigo} cadastrada com sucesso."


def atualizar_status_estrutura(codigo, novo_status):
    """Atualiza o status, a fila e o histórico da ocorrência."""
    if not isinstance(codigo, str) or not codigo.strip():
        return False, "Código inválido."

    if not isinstance(novo_status, str) or not novo_status.strip():
        return False, "Status inválido."

    codigo = codigo.strip().upper()
    novo_status = novo_status.strip()

    if novo_status not in STATUS_VALIDOS:
        return False, "O status deve ser Aberta, Em análise ou Concluída."

    ocorrencia = buscar_por_codigo(codigo)

    if ocorrencia is None:
        return False, f"Ocorrência {codigo} não encontrada."

    status_anterior = ocorrencia["status"]

    if status_anterior == novo_status:
        return False, f"A ocorrência {codigo} já possui esse status."

    ocorrencia["status"] = novo_status
    atualizar_fila(ocorrencia)

    evento = criar_evento_historico(
        codigo,
        "Atualização de status",
        status_anterior,
        novo_status
    )
    empilhar_historico(evento)

    return True, f"Status da ocorrência {codigo} atualizado para '{novo_status}'."


def iniciar_analise_proxima_demanda():
    """Inicia a análise da primeira demanda da fila."""
    if len(fila_analise) == 0:
        return False, "Não existem demandas aguardando análise."

    return atualizar_status_estrutura(fila_analise[0], "Em análise")

# ============================================================
# CARREGAMENTO E VERIFICAÇÃO
# ============================================================

def reconstruir_estruturas(lista_ocorrencias):
    """Reconstrói as estruturas com dados lidos do CSV."""
    if not isinstance(lista_ocorrencias, list):
        return {
            "carregadas": 0,
            "rejeitadas": 1,
            "erros": ["Os dados devem estar em uma lista."]
        }

    limpar_estruturas()
    carregadas = 0
    erros = []

    for linha, ocorrencia in enumerate(lista_ocorrencias, start=1):
        sucesso, mensagem = adicionar_ocorrencia(
            ocorrencia,
            registrar_historico=False
        )

        if sucesso:
            carregadas += 1
        else:
            erros.append(f"Linha {linha}: {mensagem}")

    return {
        "carregadas": carregadas,
        "rejeitadas": len(erros),
        "erros": erros
    }


def carregar_eventos_historico(eventos):
    """Carrega os eventos simulados na pilha."""
    if not isinstance(eventos, list):
        return 0

    quantidade = 0

    for evento in eventos:
        if empilhar_historico(evento):
            quantidade += 1

    return quantidade


def limpar_estruturas():
    """Limpa as estruturas sem trocar suas referências."""
    ocorrencias.clear()
    fila_analise.clear()
    pilha_historico.clear()
    ocorrencias_por_codigo.clear()
    hierarquia_bairros.clear()


def verificar_consistencia():
    """Verifica se as estruturas estão sincronizadas."""
    erros = []

    if len(ocorrencias) != len(ocorrencias_por_codigo):
        erros.append("Lista e dicionário possuem quantidades diferentes.")

    for ocorrencia in ocorrencias:
        codigo = ocorrencia["codigo"]
        localidade = ocorrencia["localidade"]
        categoria = ocorrencia["categoria"]

        if ocorrencias_por_codigo.get(codigo) is not ocorrencia:
            erros.append(f"O código {codigo} não aponta para o registro correto.")

        if ocorrencia["status"] == "Aberta" and codigo not in fila_analise:
            erros.append(f"A ocorrência {codigo} deveria estar na fila.")

        if ocorrencia["status"] != "Aberta" and codigo in fila_analise:
            erros.append(f"A ocorrência {codigo} não deveria estar na fila.")

        categorias = hierarquia_bairros.get(localidade, {})
        lista_categoria = categorias.get(categoria, [])

        if ocorrencia not in lista_categoria:
            erros.append(f"A ocorrência {codigo} não está na hierarquia.")

    for codigo in fila_analise:
        if codigo not in ocorrencias_por_codigo:
            erros.append(
                f"O código {codigo} está na fila, mas não foi cadastrado."
            )

    return len(erros) == 0, erros
