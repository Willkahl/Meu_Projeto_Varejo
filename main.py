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
print(f" Total de linhas no arquivo: {len(arquivo_bruto)}")
print(f" Colunas válidas: {colunas_validas}")


# --- Leitura do arquivo utilizando o pandas para análise exploratória dos dados, verificando as primeiras linhas do DataFrame, os tipos de dados, valores nulos e a quantidade de registros carregados.
df = pd.read_csv(base_dados, sep=SEP)

print(f"\n Primeiras linhas do DataFrame:\n{df.head()}")
print(f"\n Tipos de dados:\n{df.dtypes}")
print(f"\n Valores nulos por coluna:\n{df.isnull().sum()}")
print(f"\n Registros carregados: {df.shape[0]:,} linhas")
print(f" {df.shape[1]} colunas")