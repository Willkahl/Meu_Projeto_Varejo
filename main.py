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
# 
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