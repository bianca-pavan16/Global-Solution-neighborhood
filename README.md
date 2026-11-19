<img width="2385" height="642" alt="logo-fiap" src="https://github.com/user-attachments/assets/6cdf16e6-4004-4369-87b2-bfb088f69153" />

# FIAP - Faculdade de Informática e Administração Paulista

[FIAP - Faculdade de Informática e Administração Paulista](https://www.fiap.com.br/)

# Neighborhood Action Dashboard

**Global Solution 2026.2 – CitizenTech**

## Nome do grupo

Neighborhood Action

## 👨‍🎓 Integrantes

- **Abner Miranda Romão** – RM 576928
- **Bianca Pavan Andre** – RM 574521
- **Beatriz Lopes de Lima** – RM 575983
- **Gabriel Eduardo Alvite Mendes** – RM 576675
- **Reinaldo Dias Esteves Macieira Junior** – RM 576318

  
## 👩‍🏫 Professores

### Tutor

- André Tritiak

### Coordenador

- Valter Santiago

## 📜 Descrição

O **Neighborhood Action Dashboard** é um projeto desenvolvido para a Global Solution do segundo semestre de 2026 da FIAP, dentro do desafio CitizenTech, que propõe a utilização da tecnologia para solucionar problemas reais das cidades e comunidades.

A proposta consiste no desenvolvimento de um sistema para registrar, organizar e acompanhar ocorrências relacionadas à infraestrutura e à conservação dos bairros, contribuindo para uma gestão mais organizada das demandas urbanas.

O sistema permite cadastrar problemas cotidianos, como:

- Iluminação pública;
- Acessibilidade;
- Limpeza urbana;
- Conservação de espaços coletivos.

Por meio de um sistema desenvolvido em Python, o usuário pode registrar novas ocorrências, consultar registros existentes, pesquisar pelo código identificador, filtrar informações por categoria ou status e atualizar o andamento das solicitações.

Além do gerenciamento das ocorrências, o projeto conta com um módulo de indicadores que realiza a análise dos dados registrados, apresentando informações como:

- Quantidade total de ocorrências por categoria;
- Distribuição das ocorrências por status;
- Percentuais e proporções;
- Matriz de cruzamento entre categorias e situações;
- Identificação de pendências antigas;
- Gráficos para facilitar a visualização e interpretação dos dados.

O projeto utiliza diferentes estruturas de dados para organizar e gerenciar as informações, demonstrando como conceitos de programação podem ser aplicados a uma necessidade real da sociedade.

**Objetivo:** demonstrar como a tecnologia e a análise de dados podem apoiar a identificação de prioridades, melhorar o acompanhamento de demandas e contribuir para a construção de cidades mais organizadas, acessíveis e sustentáveis.

*Observação: o projeto é um protótipo acadêmico, desenvolvido com dados fictícios e sem integração com órgãos públicos.*

## 📁 Estrutura de pastas

Abaixo está a organização dos diretórios e arquivos do projeto:

- **`src/`**: contém os arquivos principais do sistema e suas funcionalidades.
  - **`sistema.py`**: arquivo principal, responsável pelo menu de navegação, cadastro, consulta, pesquisa, filtros e atualização das ocorrências.
  - **`estruturas.py`**: implementação das estruturas de dados utilizadas no projeto, incluindo lista, fila, pilha, dicionário e hierarquia.
  - **`indicadores.py`**: responsável pelo processamento dos dados, cálculo dos indicadores, percentuais, matriz de categorias e geração dos gráficos.
- **`graficos/`**: armazena as imagens geradas a partir dos indicadores e análises das ocorrências.
- **`README.md`**: documentação principal do projeto, contendo informações sobre a solução, tecnologias utilizadas e instruções para execução.

## 📎 Links e Observações

### 🔗 Links do Projeto

- [**Repositório GitHub**](https://github.com/bianca-pavan16/Global-Solution-neighborhood) 
- [**Vídeo de apresentação**](https://youtu.be/0uySB2yZWN0)


### 🧠 Decisões Técnicas

Para o desenvolvimento do Neighborhood Action Dashboard, a equipe optou pela linguagem Python, considerando sua versatilidade, facilidade de implementação e capacidade de trabalhar com estruturas de dados e análise de informações.

As principais tecnologias e recursos utilizados foram:

**Python 3**

Linguagem utilizada para desenvolver a lógica do sistema, implementar as funcionalidades de gerenciamento das ocorrências e organizar os dados.

**Matplotlib**

Biblioteca utilizada para a criação dos gráficos, permitindo representar visualmente os indicadores e facilitar a interpretação das informações.

**Estruturas de dados**

Foram utilizadas diferentes estruturas para organizar e manipular os registros:

- **Lista:** armazena o conjunto de ocorrências cadastradas.
- **Fila:** organiza as ocorrências abertas que aguardam análise.
- **Pilha:** mantém o histórico das alterações de status.
- **Dicionário:** permite localizar diretamente uma ocorrência por seu código identificador.
- **Hierarquia:** organiza as informações por localidade, categoria e ocorrências.
- **Matriz:** permite cruzar categorias e status para a elaboração dos indicadores.

**Organização modular**

O código foi dividido em arquivos independentes, separando as responsabilidades do sistema, das estruturas de dados e dos indicadores. Essa organização facilita a manutenção, compreensão e evolução do projeto.

**Armazenamento dos dados**

Nesta versão, os registros são mantidos em memória durante a execução do programa. Portanto, as informações cadastradas são perdidas quando o sistema é encerrado.

## 📢 Observações Gerais

**Participação na Competição:**

- [ ] Sim, aceitamos participar.
- [ x ] Não vamos participar.

**Outras observações:**

O projeto possui finalidade acadêmica e utiliza dados fictícios e localidades genéricas. Não são coletados dados pessoais nem realizadas integrações com sistemas externos.

## 🔧 Como executar o código

### 1. Pré-requisitos

Para executar o projeto, é necessário ter instalado:

- Python 3;
- Visual Studio Code ou outra IDE de preferência;
- Terminal ou prompt de comando;
- Git (opcional, para clonar o repositório).

### 2. Clonar o repositório

Abra o terminal e execute:

```bash
git clone https://github.com/bianca-pavan16/Global-Solution-neighborhood.git
```

Entre na pasta do projeto:

```bash
cd Global-Solution-neighborhood
```

### 3. Instalar as dependências

O projeto utiliza a biblioteca Matplotlib para gerar os gráficos.

Execute o comando:

```bash
python -m pip install matplotlib
```

Caso utilize Windows e o comando `python` não funcione, tente:

```bash
py -m pip install matplotlib
```

### 4. Executar o sistema

Na pasta principal do projeto, execute:

```bash
python src/sistema.py
```

No Windows, também é possível utilizar:

```bash
py src/sistema.py
```

### 5. Utilizar o sistema

Após executar o programa, será apresentado um menu com as seguintes opções:

| Opção | Funcionalidade                                                    |
| ----- | ----------------------------------------------------------------- |
| 1     | Cadastrar uma nova ocorrência                                     |
| 2     | Listar todas as ocorrências                                       |
| 3     | Pesquisar ocorrência pelo código e consultar histórico            |
| 4     | Filtrar ocorrências por categoria ou status                       |
| 5     | Atualizar o status de uma ocorrência                              |
| 6     | Consultar indicadores, percentuais, pendências antigas e gráficos |
| 0     | Encerrar o sistema                                                |

O usuário poderá navegar pelas opções do menu, registrar novas ocorrências e acompanhar as informações cadastradas.

**Importante:** os dados são armazenados apenas durante a execução. Ao fechar o programa, os registros cadastrados são perdidos.

---

## 📋 Licença

Projeto desenvolvido para fins acadêmicos no âmbito da Global Solution 2026.2 da FIAP.

