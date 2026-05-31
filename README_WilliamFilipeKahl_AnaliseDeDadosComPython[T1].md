
#  MINI PROJETO - ANÁLISE DE DADOS COM PYTHON

**Curso:** Análise de Dados com Python [T1] | Módulo 1 - Semana 07
**Aluno:** William Filipe Kahl

## --- Objetivo

Projeto de análise exploratória de dados com aplicação de método ETL (Extract, Treatment, Load) de um dataset de varejo. O script realiza a importação e inspeção inicial dos dados até o tratamento, limpeza e geração de estatísticas descritivas, seguindo uma estrutura organizada em Sprints.

## --- Estrutura do Projeto

Meu_Projeto_Varejo/
|
|-- Base Varejo.csv     # Base de dados original (não incluída no repositório)
|-- main.py             # Script principal de análise
|-- requirements.txt    # Dependências do projeto
|-- README.md           # Detalhes do projeto


### SPRINTS

## --- Sprint 1 - Importação de Dados
- Leitura do arquivo CSV com `csv.reader`
- Identificação de colunas válidas
- Importação com pandas
- Análise inicial:
  - head()
  - dtypes
  - valores nulos
  - dimensão dos dados
- Remoção automática de colunas sem nome('Unnamed')
- Exibição das primeiras linhas, tipos de dados, valores nulos, e total de registros


## --- Sprint 2 - Tratamento de Dados
- Conversão da coluna 'DATA' para o tipo 'datetime' ('dd/mm/yyyy')
- Conversão das colunas de identificadores ('CO_ID', 'CL_OD', 'PR_ID', 'CL_EC', 'CL_FHL') para inteiro
- Padronização das colunas de texto ('CL_GENERO', 'CL_SEG', 'PR_CAT', 'PR_NOME') para letras maiúsculas sem espaços extras


## --- Sprint 3 - Identificação e limpeza de nulos e duplicadas
- Identificação de valores nulos por coluna
- Contagem de linhas duplicadas
- Tratamento de categorias inválidas ('#N/D') substituídas por "SEM CATEGORIA"
- Remoção de de registros com 'DATA' inválida (NaT)
- Remoção de linhas 100% duplicadas
- Validação do identificador 'CO_ID" (intervalo e unicidade)


## --- Sprint 4 - Estatísticas Descritivas
- Análise do número de filhos por cliente ('CL_FHL'), considerando apenas um registro por 'CL_ID':

Métrica | Descrição
- Média | Média de filhos por cliente
- Mediana | Mediana de filhos por cliente
- Desvio Padrão | Dispersão em torno da média
- Moda | Valor(es) mais frequente(s)
- Mínimo / Máximo | Estremos da distribuição
- Quartis (Q1, Q2, Q3) | Divisão percentilar

Inclui ainda uma distribuição visual do número de filhos por cliente


## --- Sprint 5 - Relatório e Documentação
- Análise da base de dados com aplicação de agrupamento de dados com groupby e pivottable com 6 visões distintas:

Métrica | Descrição
- Agrupamento 1 | Itens comprados por Gênero
- Agrupamento 2 | Iens comprados por Categoria de Produto
- Agrupamento 3 | Itens comprados: Gênero x Categoria
- Agrupamento 4 | Total de compras por Ano e Mês
- Agrupamento 5 | Top 10 produtos mais comprados
- Agrupamento 6 | Clientes únicos por segmento

- Criação de uma base limpa em formato .csv para eventual utilização



## --- Pré-requisitos
- Python 3.8 ou superior
- Pandas
- NumPy


## --- Como Executar
1. Certifique-se de que a base de dados 'Base Varejo.csv' está no caminho correto
   (ajuste a variável 'base_dados' no início do script se necessário)


## --- Base de Dados

A base utilizada é um arquivo CSV com separador ';' e as seguintes colunas principais:

| coluna | Descrição |
| 'CO_ID' | Identificador da compra |
| 'CL_ID' | Identificador do cliente |
| 'PR_ID' | Identificador do produto |
| 'DATA' | Data da compra ('dd/mm/yyyy') |
| 'CL_GENERO' | Gênero do cliente |
| 'CL_SEG' | Segmento do cliente |
| 'CL_EC' | Estado civil (código) |
| 'CL_FHL' | Número de filhos |
|'PR_CAT' | Categoria de produto |
|'PR_NOME' | Nome do produto |


***O arquivo 'Base Varejo.csv' não está incluído neste repositório por conter dados sensíveis.***


## --- Autor

***William Filipe Kahl***
