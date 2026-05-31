#**************************************************************************
# MINI_PROJETO AVALIATIVO - Análise Exploratória de Dados com Python
# Curso: Análise de Dados com Python [T1] | Módulo 1 - Semana 07
# Aluno: William Filipe Kahl
#**************************************************************************

import csv
import pandas as pd
import numpy as np


# =========================================================================
# SPRINT 1 - IMPORTAÇÃO DOS DADOS
# Leitura da base de dados analisada com utilização do csvreader do módulo csv, para verificar a estrutura do arquivo e as colunas disponíveis.
# =========================================================================

print("\n [SPRINT 1] - Importação dos Dados")


# --- Localização do arquivo base de dados no pc do aluno, utilizando o caminho absoluto para garantir a leitura correta do arquivo.
base_dados = r"C:\Users\WilliamKahl\OneDrive - AdviceHealth\Área de Trabalho\Will\SCTech\Análise de Dados\Meu_Projeto_Varejo\Base Varejo.csv"
SEP = ";"


# --- Leitura do arquivo utilizando o csvreader para verificar a estrutura do arquivo e as colunas disponíveis.
arquivo_bruto = []
with open(base_dados, encoding="utf-8", newline="") as arquivo:
    reader = csv.reader(arquivo, delimiter=SEP)
    for linha in reader:
        arquivo_bruto.append(linha)

colunas_validas = [c for c in arquivo_bruto[0] if c.strip()]
print(f"\n Total de linhas no arquivo: {len(arquivo_bruto)}")
print(f"\n Colunas válidas: {colunas_validas}")


# --- Leitura do arquivo utilizando o pandas para análise exploratória dos dados, verificando as primeiras linhas do DataFrame, os tipos de dados, valores nulos e a quantidade de registros carregados.
df = pd.read_csv(base_dados, sep=SEP)

# Remove colnas vazias  sem nome ou com nome apenas de espaços em branco, que foram identificadas na leitura do arquivo bruto.
colunas_vazias = [c for c in df.columns if c.startswith("Unnamed") or c.strip() == ""]
df.drop(columns=colunas_vazias, inplace=True)


print(f"\n Primeiras linhas do DataFrame:\n{df.head()}")
print(f"\n Tipos de dados:\n{df.dtypes}")
print(f"\n Valores nulos por coluna:\n{df.isnull().sum()}")
print(f"\n Registros carregados: {df.shape[0]:,} linhas")
print(f" {df.shape[1]} colunas")


# =========================================================================
# SPRINT 2 - TRATAMENTO DOS DADOS (STRING, NUMÉRICOS, DATAS)
# Tratamento dos dados para garantir que as colunas estejam no formato correto, convertendo colunas de string para o tipo string, colunas numéricas para o tipo numérico e colunas de data para o tipo datetime, além de padronizar os valores de string para facilitar a análise posterior.
# =========================================================================

print("\n [SPRINT 2] - Tratamento dos Dados (String, Numéricos, Datas)")

# Converter coluna DATA de String para Datetime, utilizando o formato específico da data presente na base de dados.
df["DATA"] = pd.to_datetime(df["DATA"], format="%d/%m/%Y", errors="coerce")

# Converter colunas numéricas para números inteiros ou decimais corretos
df["CO_ID"] = df["CO_ID"].astype(int)   # identificar de número da compra
df["CL_ID"] = df["CL_ID"].astype(int)   # identificar do cliente
df["PR_ID"] = df["PR_ID"].astype(int)   # identificar do produto
df["CL_EC"] = df["CL_EC"].astype(int)   # identificar do estado civil do cliente (código)
df["CL_FHL"] = df["CL_FHL"].astype(int) # identificar do número de filhos do cliente

# Padronizar colunas de string, convertendo para letras minúsculas e removendo espaços em branco extras.
for col in ["CL_GENERO", "CL_SEG", "PR_CAT", "PR_NOME"]:
    df[col] = df[col].astype(str).str.strip().str.upper()

print("\n Tipos de dados após tratamento:")
print(df.dtypes.to_string())
print(f"\n Valores nulos por coluna após tratamento:\n{df.isnull().sum()}")
print(f"\n Datas invalidas (NaT) detectadas após tratamento: {df['DATA'].isna().sum()}")


# =========================================================================
# SPRINT 3 - IDENTIFICAÇÃO E LIMPEZA DE NULOS E DUPLICADAS
# =========================================================================

print("\n [SPRINT 3] - Identificação e Limpeza de Nulos e Duplicadas")

# --- Problema 1: valores nulos por coluna
print(f"\n Valores nulos por coluna (antes da limpeza):")
nulos = df.isnull().sum()
print(nulos.to_string())


# --- Problema 2: Linhas duplicadas
duplicadas = df.duplicated().sum()
print(f"\n Linhas duplicadas encontradas: {duplicadas:,}")

# --- Problema 3: categoria com valor inválido '#N/D'
categoria_invalida = (df["PR_CAT"] == "#N/D").sum()
print(f"\n Registros com PR_CAT = '#N/D': {categoria_invalida:,}")

# --- Limpeza dos dados: remoção de linhas duplicadas e substituição de valores inválidos na coluna PR_CAT por NaN.

# Limpeza 1: Tratar categorias inválidas com "SEM CATEGORIA"
# Justificativa: '#N/D' é um marcador de dado ausente (equivalente ao nulo do Excel exportado).
# Dessa forma, imputar 'SEM CATEGORIA' preserva os registros de compra (que tem cliente, data e produto válidos)
# mantendo a integridade dos dados para análises futuras, sem excluir registros potencialmente valiosos.
df["PR_CAT"] = df["PR_CAT"].apply(
    lambda x: "SEM CATEGORIA" if x in ("#N/D", "", "NAN", "NONE") else x
)
print(f"\n  Categorias após limpeza: {df['PR_CAT'].unique().tolist()}")

# Limpeza 2: Remover linhas com DATA inválida (NaT)
# Justificativa: sem data de compra, não é possível imputar um valor confiável.
# O registro perde utilizada em análises temporais e de comportamento de compra, portanto, a remoção é a melhor opção para manter a qualidade dos dados.
linhas_antes = len(df)
df = df.dropna(subset=["DATA"], inplace=False)
datas_removidas = linhas_antes - len(df)
print(f"\n Linhas removidas por DATA inválida: {datas_removidas:,}")


# Limpeza 3: Eliminar linhas 100% duplicadas
# Justificativa: o mesmo cliente, comprando o mesmo produto, na mesma data e compra (CO_ID),
# é um item de duplicação de dados, não uma compra dupla.
df.drop_duplicates(inplace=True)
print(f"\n Linhas após remoção de duplicadas: {len(df):,}")


#Validação do identificador de compra (CO_ID) para garantir que cada compra seja única, verificando se há CO_ID duplicados.
# Regra de negócio: CO_ID deve ser inteiro positivo (> 0)
invalidos_coid = (df["CO_ID"] <= 0).sum()
print(f"\n  CO_ID inválidos (<= 0): {invalidos_coid}")
print(f" Intervalo de CO_ID : {df['CO_ID'].min()} a {df['CO_ID'].max()}")
print(f" Compras únicas (CO_ID distintos): {df['CO_ID'].nunique()}")

print(f"\n Base limpa: {len(df):,} registros | {df.shape[1]} colunas")
print(f" Período coberto: {df['DATA'].min().date()} a {df['DATA'].max().date()}")


# =========================================================================
# SPRINT 4 - ESTATÍSTICAS DESCRITIVAS
# =========================================================================

print("\n [SPRINT 4] - Estatísticas Descritivas - Número de Filhos (CL_FHL)")

# CL_FHL tem uma linha por item comprado (não por cliente).
# Portanto, a média de filhos por compra é diferente da média de filhos por cliente.
# Para estatísticas de perfil do cliente usamos 1 registro por CL_ID.
filhos_por_cliente = df.drop_duplicates(subset=["CL_ID"])["CL_FHL"]

media = filhos_por_cliente.mean()
mediana = filhos_por_cliente.median()
desvio = filhos_por_cliente.std()
moda = filhos_por_cliente.mode().tolist()
maximo = filhos_por_cliente.max()
minimo = filhos_por_cliente.min()
contagem = filhos_por_cliente.count()
q1 = filhos_por_cliente.quantile(0.25)
q2 = filhos_por_cliente.quantile(0.50)
q3 = filhos_por_cliente.quantile(0.75)

print(f"\n clientes únicos analisados: {contagem:,}")
print(f" Média de filhos por cliente: {media:.4f}")
print(f" Mediana de filhos por cliente: {mediana:.1f}")
print(f" Desvio padrão de filhos por cliente: {desvio:.4f}")
print(f" Moda de filhos por cliente: {moda}")
print(f" Máximo de filhos por cliente: {maximo}")
print(f" Mínimo de filhos por cliente: {minimo}")
print(f" Quartil 1 de filhos por cliente: {q1:.1f}")
print(f" Quartil 2 de filhos por cliente: {q2:.1f}")
print(f" Quartil 3 de filhos por cliente: {q3:.1f}")

# Visualização da distribuição de filhos por cliente, utilizando uma barra proporcional ao número de clientes para cada quantidade de filhos.
print("\n Distribuição de filhos (clientes únicos):")
dist_filhos = filhos_por_cliente.value_counts().sort_index()
for qtd_filhos, n in dist_filhos.items():
    barra = "*" * (n * 30 // dist_filhos.max())  # escala de 1 asterisco para o total de clientes
    print(f" {qtd_filhos} filhos: {n:>5,} clientes {barra}")



# =========================================================================
# SPRINT 5 - RELATÓRIO E DOCUMENTAÇÃO
# =========================================================================

print("\n [SPRINT 5] - Relatório e Documentação")

# Agrupameento 1: Itens comprados por Gênero
print("\n [AG-1] Total de itens comprados por Gênero:")
ag_genero = (df.groupby("CL_GENERO")["CO_ID"]
             .count()
             .reset_index()
             .rename(columns={"CO_ID": "Quantidade de Itens"})
             .sort_values("Quantidade de Itens", ascending=False)
)
print(ag_genero.to_string(index=False))


# Agrupamento 2: Itens comprados por Categoria de Produto
print("\n [AG-2] Total de itens comprados por Categoria de Produto:")
ag_categoria = (df.groupby("PR_CAT")["CO_ID"]
                 .count()
                 .reset_index()
                 .rename(columns={"CO_ID": "Quantidade de Itens"})
                 .sort_values("Quantidade de Itens", ascending=False)
)
print(ag_categoria.to_string(index=False))


# Agrupamento 3:  Pivot Gênero x Categoria de Produto
print("\n [AG-3] Total de itens comprados: Gênero x Categoria de Produto:")
pivot = pd.pivot_table(
    df,
    values="CO_ID",
    index="CL_GENERO",
    columns="PR_CAT",
    aggfunc="count",
    fill_value=0
)
print(pivot.to_string())


# Agrupamento 4: Volume de compras por Ano-Mês (Top 10)
print("\n [AG-4] Volume de compras por Ano-Mês (Top 10 períodos):")
df["ANO_MES"] = df["DATA"].dt.to_period("M")
ag_ano_mes = (df.groupby("ANO_MES")["CO_ID"]
              .count()
              .reset_index()
              .rename(columns={"CO_ID": "Quantidade de Itens"})
              .sort_values("Quantidade de Itens", ascending=False)
              .head(10)
)
print(ag_ano_mes.to_string(index=False))


# Agrupamento 5: Top 10 produtos mais comprados
print("\n [AG-5] Top 10 produtos mais comprados:")
ag_produtos = (df.groupby("PR_NOME")["CO_ID"]
               .count()
               .reset_index()
               .rename(columns={"CO_ID": "Quantidade de Itens"})
               .sort_values("Quantidade de Itens", ascending=False)
               .head(10)
)
print(ag_produtos.to_string(index=False))


# Agrupamento 6: Clientes únicos por Segmento
print("\n [AG-6] Clientes únicos por Segmento:")
ag_segmento = (df.groupby("CL_SEG")["CL_ID"]
              .count()
              .reset_index()
              .rename(columns={"CL_ID": "Clientes Únicos"})
              .sort_values("Clientes Únicos", ascending=False)
)
print(ag_segmento.to_string(index=False))


# Exportação do relatório final para um arquivo CSV, contendo a base limpa
df_limpo = df.drop(columns=["ANO_MES"])  # remover coluna auxiliar de agrupamento
df_limpo.to_csv("Base_Varejo_Limpa.csv", index=False, sep=SEP, encoding="utf-8")
print("\n Relatório final exportado para Base_Varejo_Limpa.csv")



