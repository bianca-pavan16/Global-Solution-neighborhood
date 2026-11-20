"""Carrega as ocorrências e o histórico salvos na pasta dados/."""

import csv
from datetime import datetime
from pathlib import Path

try:
    from .estruturas import (
        CATEGORIAS_VALIDAS,
        reconstruir_estruturas,
        carregar_eventos_historico,
        ocorrencias,
    )
except ImportError:
    from estruturas import (
        CATEGORIAS_VALIDAS,
        reconstruir_estruturas,
        carregar_eventos_historico,
        ocorrencias,
    )


PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_DADOS = PASTA_PROJETO / "dados"

STATUS_CSV = {
    "aberta": "Aberta",
    "em análise": "Em análise",
    "concluída": "Concluída",
}

CATEGORIAS_CSV = {
    categoria.casefold(): categoria
    for categoria in CATEGORIAS_VALIDAS
}


def carregar_dados_iniciais():
    """Importa os dois CSVs e retorna um resumo do carregamento."""

    caminho_ocorrencias = PASTA_DADOS / "ocorrencias.csv"

    with caminho_ocorrencias.open(
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:
        linhas = list(csv.DictReader(arquivo))

    registros = []

    for linha in linhas:
        categoria_original = (linha.get("categoria") or "").strip()
        status_original = (linha.get("status") or "").strip()

        categoria = CATEGORIAS_CSV.get(
            categoria_original.casefold(),
            ""
        )
        status = STATUS_CSV.get(
            status_original.casefold(),
            ""
        )

        try:
            data_abertura = datetime.strptime(
                linha["data_abertura"],
                "%Y-%m-%d"
            ).strftime("%d/%m/%Y")
        except (KeyError, ValueError):
            data_abertura = linha.get("data_abertura", "")

        registros.append({
            "codigo": (linha.get("id") or "").strip(),
            "categoria": categoria,
            "descricao": (linha.get("descricao") or "").strip(),
            "localidade": (linha.get("local") or "").strip(),
            "data_abertura": data_abertura,
            "status": status,
        })

    resultado = reconstruir_estruturas(registros)

    avisos = [
        f"Ocorrência rejeitada: {erro}"
        for erro in resultado["erros"]
    ]

    eventos, erros_eventos = _ler_historico()
    quantidade_eventos = carregar_eventos_historico(eventos)
    avisos.extend(erros_eventos)

    return {
        "ocorrencias_carregadas": resultado["carregadas"],
        "ocorrencias_rejeitadas": resultado["rejeitadas"],
        "eventos_carregados": quantidade_eventos,
        "avisos": avisos,
    }


def _ler_historico():
    """Lê os eventos e converte os campos para o formato do sistema."""

    caminho_historico = PASTA_DADOS / "historico_novo.csv"

    with caminho_historico.open(
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:
        linhas = list(csv.DictReader(arquivo))

    codigos_existentes = {
        ocorrencia["codigo"]
        for ocorrencia in ocorrencias
    }

    eventos = []
    avisos = []
    ids_eventos = set()

    for numero, linha in enumerate(linhas, start=2):
        evento_id = (linha.get("evento_id") or "").strip()
        codigo = (linha.get("ocorrencia_id") or "").strip().upper()

        if not evento_id or evento_id in ids_eventos:
            avisos.append(
                f"Linha {numero} do histórico: ID vazio ou duplicado."
            )
            continue

        if codigo not in codigos_existentes:
            avisos.append(
                f"Linha {numero} do histórico: ocorrência {codigo} não encontrada."
            )
            continue

        status_anterior = STATUS_CSV.get(
            (linha.get("status_anterior") or "").strip().casefold(),
            ""
        )
        status_novo = STATUS_CSV.get(
            (linha.get("status_novo") or "").strip().casefold(),
            ""
        )

        if not status_anterior or not status_novo:
            avisos.append(
                f"Linha {numero} do histórico: status inválido."
            )
            continue

        try:
            data_evento = datetime.strptime(
                linha["data_evento"],
                "%Y-%m-%d"
            )
        except (KeyError, ValueError):
            avisos.append(
                f"Linha {numero} do histórico: data inválida."
            )
            continue

        eventos.append({
            "codigo": codigo,
            "acao": (linha.get("descricao_evento") or "").strip(),
            "status_anterior": status_anterior,
            "status_novo": status_novo,
            "data_hora": data_evento.strftime("%d/%m/%Y") + " 00:00:00",
        })

        ids_eventos.add(evento_id)

    return eventos, avisos
