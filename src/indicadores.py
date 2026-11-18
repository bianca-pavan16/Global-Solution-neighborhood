
try:
    from .dados import ocorrencias
except ImportError:
    from dados import ocorrencias
from datetime import datetime, date
import matplotlib.pyplot as plt
import os


# CATEGORIAS E STATUS UTILIZADOS NO SISTEMA

CATEGORIAS = [
    "Iluminação",
    "Acessibilidade",
    "Limpeza",
    "Conservação"
]

STATUS = [
    "Aberta",
    "Em análise",
    "Concluída"
]


# 1. CRIAR MATRIZ DE CATEGORIAS E STATUS

def criar_matriz():

    matriz = []

    for categoria in CATEGORIAS:

        linha = []

        for status in STATUS:

            quantidade = 0

            for ocorrencia in ocorrencias:

                if (ocorrencia["categoria"] == categoria
                        and ocorrencia["status"] == status):

                    quantidade += 1

            linha.append(quantidade)

        matriz.append(linha)

    return matriz


# 2. CALCULAR TOTAL POR CATEGORIA

def calcular_por_categoria(matriz):

    totais = []

    for indice, categoria in enumerate(CATEGORIAS):

        total = sum(matriz[indice])

        totais.append(total)

    return totais


# 3. CALCULAR TOTAL POR STATUS

def calcular_por_status(matriz):

    totais = []

    for indice_status in range(len(STATUS)):

        total = 0

        for linha in matriz:

            total += linha[indice_status]

        totais.append(total)

    return totais


# 4. CALCULAR PERCENTUAIS

def calcular_percentuais(valores, total_geral):

    percentuais = []

    for valor in valores:

        if total_geral > 0:
            percentual = (valor / total_geral) * 100

        else:
            percentual = 0

        percentuais.append(percentual)

    return percentuais


# 5. IDENTIFICAR PENDÊNCIAS ANTIGAS

def calcular_pendencias_antigas():

    hoje = date.today()

    quantidade_antigas = 0

    for ocorrencia in ocorrencias:

        if ocorrencia["status"] != "Concluída":

            try:

                data_abertura = datetime.strptime(
                    ocorrencia["data_abertura"],
                    "%d/%m/%Y"
                ).date()

                dias_aberta = (hoje - data_abertura).days

                if dias_aberta > 7:
                    quantidade_antigas += 1

            except ValueError:

                print(
                    f"Aviso: data inválida na ocorrência "
                    f"{ocorrencia['codigo']}."
                )

    return quantidade_antigas


# 6. GERAR GRÁFICOS

def gerar_graficos(totais_categoria, totais_status):

    # Criar pasta para armazenar os gráficos
    os.makedirs("graficos", exist_ok=True)

    # GRÁFICO 1 - OCORRÊNCIAS POR CATEGORIA

    plt.figure(figsize=(9, 5))

    plt.bar(CATEGORIAS, totais_categoria)

    plt.title("Quantidade de ocorrências por categoria")
    plt.xlabel("Categorias")
    plt.ylabel("Quantidade")

    plt.xticks(rotation=15)
    plt.tight_layout()

    plt.savefig(
        "graficos/ocorrencias_por_categoria.png"
    )

    plt.show()
    plt.close()


    # GRÁFICO 2 - DISTRIBUIÇÃO POR STATUS

    plt.figure(figsize=(8, 6))

    if sum(totais_status) > 0:

        plt.pie(
            totais_status,
            labels=STATUS,
            autopct="%1.1f%%",
            startangle=90
        )

        plt.title("Distribuição de ocorrências por status")

    else:

        plt.text(
            0.5, 0.5,
            "Nenhuma ocorrência cadastrada",
            ha="center",
            va="center"
        )

    plt.tight_layout()

    plt.savefig(
        "graficos/ocorrencias_por_status.png"
    )

    plt.show()
    plt.close()

    print("\nGráficos salvos na pasta 'graficos'.")


# 7. INTERPRETAR OS RESULTADOS

def interpretar_resultados(
    totais_categoria,
    totais_status,
    pendencias_antigas,
    total_geral
):

    print("\n" + "=" * 55)
    print("             ANÁLISE DOS RESULTADOS")
    print("=" * 55)

    if total_geral == 0:

        print("\nAinda não existem ocorrências para analisar.")
        return

    # Categoria com maior quantidade
    maior_categoria = max(
        range(len(totais_categoria)),
        key=lambda i: totais_categoria[i]
    )

    print(
        f"\nCategoria com mais ocorrências: "
        f"{CATEGORIAS[maior_categoria]} "
        f"({totais_categoria[maior_categoria]} registros)."
    )

    # Status com maior quantidade
    maior_status = max(
        range(len(totais_status)),
        key=lambda i: totais_status[i]
    )

    print(
        f"Status predominante: {STATUS[maior_status]} "
        f"({totais_status[maior_status]} registros)."
    )

    # Percentual de ocorrências concluídas
    percentual_concluidas = (
        totais_status[2] / total_geral
    ) * 100

    print(
        f"Percentual de ocorrências concluídas: "
        f"{percentual_concluidas:.1f}%."
    )

    # Pendências antigas
    print(
        f"Pendências com mais de 7 dias: "
        f"{pendencias_antigas}."
    )

    print("\nInterpretação:")

    if percentual_concluidas >= 70:

        print(
            "O percentual de conclusão é elevado. "
            "A maioria das demandas foi resolvida."
        )

    elif percentual_concluidas >= 40:

        print(
            "O percentual de conclusão é intermediário. "
            "Ainda existem oportunidades de melhoria."
        )

    else:

        print(
            "O percentual de conclusão é baixo. "
            "É importante acompanhar as demandas pendentes."
        )

    if pendencias_antigas > 0:

        print(
            "Existem pendências antigas que precisam "
            "de atenção e acompanhamento."
        )

    else:

        print(
            "Não foram identificadas pendências com "
            "mais de 7 dias."
        )

    print("=" * 55)


# 8. EXIBIR TODOS OS INDICADORES

def exibir_indicadores():

    print("\n" + "=" * 55)
    print("          INDICADORES DO BAIRRO")
    print("=" * 55)

    total_geral = len(ocorrencias)

    if total_geral == 0:

        print("\nNenhuma ocorrência cadastrada.")
        print("Cadastre ocorrências antes de consultar os indicadores.")
        return

    # Criar matriz
    matriz = criar_matriz()

    # Calcular totais
    totais_categoria = calcular_por_categoria(matriz)

    totais_status = calcular_por_status(matriz)

    # Calcular percentuais
    percentuais_categoria = calcular_percentuais(
        totais_categoria,
        total_geral
    )

    percentuais_status = calcular_percentuais(
        totais_status,
        total_geral
    )

    # Calcular indicador adicional
    pendencias_antigas = calcular_pendencias_antigas()


    # EXIBIR MATRIZ

    print("\nMATRIZ DE CATEGORIAS E STATUS")

    print(
        f"\n{'Categoria':<20}"
        f"{'Aberta':>8}"
        f"{'Análise':>10}"
        f"{'Concluída':>12}"
        f"{'Total':>8}"
    )

    print("-" * 58)

    for indice, categoria in enumerate(CATEGORIAS):

        print(
            f"{categoria:<20}"
            f"{matriz[indice][0]:>8}"
            f"{matriz[indice][1]:>10}"
            f"{matriz[indice][2]:>12}"
            f"{totais_categoria[indice]:>8}"
        )

    print("-" * 58)

    print(
        f"{'TOTAL':<20}"
        f"{totais_status[0]:>8}"
        f"{totais_status[1]:>10}"
        f"{totais_status[2]:>12}"
        f"{total_geral:>8}"
    )


    # EXIBIR PERCENTUAIS POR CATEGORIA

    print("\nTOTAL E PERCENTUAL POR CATEGORIA")

    for indice, categoria in enumerate(CATEGORIAS):

        print(
            f"{categoria}: {totais_categoria[indice]} "
            f"ocorrências ({percentuais_categoria[indice]:.1f}%)"
        )


    # EXIBIR PERCENTUAIS POR STATUS

    print("\nTOTAL E PERCENTUAL POR STATUS")

    for indice, status in enumerate(STATUS):

        print(
            f"{status}: {totais_status[indice]} "
            f"ocorrências ({percentuais_status[indice]:.1f}%)"
        )


    # EXIBIR INDICADOR ADICIONAL

    print("\nINDICADOR ADICIONAL")

    print(
        f"Pendências abertas há mais de 7 dias: "
        f"{pendencias_antigas}"
    )


    # INTERPRETAR RESULTADOS

    interpretar_resultados(
        totais_categoria,
        totais_status,
        pendencias_antigas,
        total_geral
    )


    # PERGUNTAR SE DESEJA GERAR GRÁFICOS

    opcao = input(
        "\nDeseja visualizar os gráficos? (S/N): "
    ).strip().upper()

    if opcao == "S":

        gerar_graficos(
            totais_categoria,
            totais_status
        )

    elif opcao == "N":

        print("\nConsulta de indicadores finalizada.")

    else:

        print("\nOpção inválida. Os indicadores foram calculados, "
              "mas os gráficos não foram exibidos.")
