"""
Tema: “Operação Limpeza”
Simule valores nulos em pelo menos 2 linhas.
Preencha os valores nulos da coluna Producao com a média e os de Exportacoes com 0.
Renomeie todas as colunas para começarem com letra maiúscula e sem espaços.
Salve o resultado em data/limpos/semana02_dia05.csv.
Imprima um resumo (df.describe()) para verificar as médias e conferir se os valores substituídos impactaram o conjunto.

"""

# Simulando varios valores nulos
import os
import datetime

import pandas as pd

from scripts.Semana02.semana02_dia05 import file_path

# Buscar arquivo csv das exportações do ano 2025
file = r'C:\\Users\\User\\PycharmProjects\\PythonProject\\data\\commodities_mes.csv'

df = pd.read_csv(file)

novaseries = pd.DataFrame(
    [{'Mes': 'Jul', 'Commodity': 'Minerio de Ferro', 'Producao': 150000, 'Exportacoes': 100000},
     {'Mes': 'Ago', 'Commodity': 'Minerio de Ferro', 'Producao': 250000, 'Exportacoes': 200000},
     {'Mes': 'Set', 'Commodity': 'Minerio de Ferro', 'Producao': 300000, 'Exportacoes': 50000},
     {'Mes': 'Out', 'Commodity': 'Algodao', 'Producao': 50000, 'Exportacoes': 0},  # <- corrigido aqui
     {'Mes': 'Out', 'Commodity': 'Milho', 'Producao': 0, 'Exportacoes': 50000},
     {'Mes': 'Out', 'Commodity': 'Soja', 'Producao': 0, 'Exportacoes': 15000}]
)

df = pd.concat([df, novaseries], ignore_index=True)

mapa_trimestre = {'Jan': 'T1', 'Fev': 'T1', 'Mar': 'T1',
                  'Abr': 'T2', 'Mai': 'T2', 'Jun': 'T2',
                  'Jul': 'T3', 'Ago': 'T3', 'Set': 'T3',
                  'Out': 'T4', 'Nov': 'T4', 'Dez': 'T4'}
df['Trimestre'] = df['Mes'].map(mapa_trimestre)
print('Arquivo Atualizado com sucesso...')
df.loc[31, 'Producao'] = None
df.loc[32, 'Producao'] = None
df.loc[29, 'Exportacoes'] = None
print(df)

# preenchendo os valores nulos de Produção co a média
df['Producao'] = df['Producao'].fillna(df['Producao'].mean().round(2))
df['Exportacoes'] = df['Exportacoes'].fillna(0)
# Colocando os titulos em maiusculo sem espaços
df.columns = [col.strip().upper() for col in df.columns]

# Salvando arquivo
hoje = datetime.date.today().strftime("%Y%m%d")
file_save = r'C:\\Users\\User\\PycharmProjects\\PythonProject\\data\\limpos'
file_name = f'Commodities_mes_desafio{hoje}.csv'
file_path = os.path.join(file_save,file_name)
os.makedirs(file_save, exist_ok=True)
df.to_csv(file_path, index=False)
print(f'Arquivo salvo {file_save} e atualizado...')
print(df.describe())
