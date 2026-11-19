# Neighborhood Action Dashboard

Projeto da Global Solution 2026.2 (FIAP) — desafio CitizenTech.

Sistema em Python, executado no terminal, para registrar, consultar e acompanhar problemas de infraestrutura e conservação de um bairro (iluminação, acessibilidade, limpeza e conservação de espaços coletivos). É um protótipo acadêmico, com dados fictícios, sem integração com órgãos públicos.

**Equipe:** [nome da equipe e RMs dos integrantes]

## Como executar

1. Instale o Python 3.
2. Instale a biblioteca dos gráficos:

```
pip install matplotlib
```

3. Na pasta principal do projeto, execute:

```
python src/sistema.py
```

## Menu do sistema

| Opção | O que faz |
|-------|-----------|
| 1 | Cadastrar ocorrência (categoria, descrição, localidade e data; o código é gerado sozinho) |
| 2 | Listar todas as ocorrências |
| 3 | Pesquisar uma ocorrência pelo código e ver o histórico dela |
| 4 | Filtrar ocorrências por categoria ou por status |
| 5 | Atualizar o status (Aberta, Em análise ou Concluída) |
| 6 | Consultar indicadores (matriz, percentuais, pendências antigas e gráficos) |
| 0 | Sair |

## Estrutura de arquivos

```
src/
  sistema.py       menu e funcionalidades
  estruturas.py    estruturas de dados (lista, fila, pilha, dicionário e hierarquia)
  indicadores.py   cálculo e exibição dos indicadores e gráficos
graficos/          imagens geradas pelos gráficos
```

## Estruturas de dados

- **Lista:** guarda todas as ocorrências.
- **Fila:** ocorrências abertas aguardando análise.
- **Pilha:** histórico de mudanças (o evento mais recente é o primeiro a ser consultado).
- **Dicionário:** busca direta pelo código da ocorrência.
- **Hierarquia:** localidade, categoria e ocorrências.
- **Matriz:** cruza categoria e status nos indicadores.

## Observações

- Os dados ficam apenas na memória: ao fechar o programa, as ocorrências cadastradas são perdidas.
- O sistema usa somente informações fictícias e localizações genéricas, sem dados pessoais.
