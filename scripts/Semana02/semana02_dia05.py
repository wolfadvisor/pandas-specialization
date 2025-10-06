"""
Objetivos da segunda semana
Aprender a:
Detectar e tratar valores ausentes (NaN, None, etc.)
Substituir valores faltantes com médias, medianas ou valores fixos
Renomear colunas e ajustar nomes de índices
Salvar o dataset limpo e verificar a integridade
"""
import datetime
import os
from operator import index

import pandas as pd

file = r'C:\Users\User\PycharmProjects\PythonProject\data\commodities_mes.csv'

df = pd.read_csv(file)
# print(df.info())
""" Informações do arquivo
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 27 entries, 0 to 26
Data columns (total 6 columns):
 #   Column       Non-Null Count  Dtype 
---  ------       --------------  ----- 
 0   Unnamed: 0   27 non-null     int64 
 1   Mes          27 non-null     object
 2   Commodity    27 non-null     object
 3   Producao     27 non-null     int64 
 4   Exportacoes  27 non-null     int64 
 5   Trimestre    27 non-null     object
dtypes: int64(3), object(3)
memory usage: 1.4+ KB
None
"""
# Treinar valores faltantes (inserindo falhas)
df.loc[2, 'Exportacoes'] = None
df.loc[5, 'Producao'] = None
# print(df)

# Detectar valores nulos nas series
print(df.isna().sum())
""" Valores indentificados em Exportações e Produção  """
# Vamos analisar os dados podendo:Substituir por zero, Substituir pela média da coluna, ou remover a linha

# Substituir por zero
df_temp = df.copy()
df_temp1 = df.copy()

df_temp['Exportacoes'] = df_temp['Exportacoes'].fillna(0)
df_temp['Producao'] = df_temp['Producao'].fillna(df_temp['Producao'].mean().round(2))
df_temp1.dropna()
# print(df_temp)
# print()
# print(df_temp1)

# padronizar os nomes das colunas
df_temp.columns = [col.strip().upper() for col in df_temp.columns]
print(df_temp)
print(df_temp.info())
print(df_temp.describe())

# Criar nova pasta no diretorio
hoje = datetime.date.today().strftime("%Y%m%d")
path_save = r'C:\\Users\\User\\PycharmProjects\\PythonProject\\data\\limpos'
file_name = f'Commodities_mes_limpo{hoje}.csv'
file_path = os.path.join(path_save,file_name)
os.makedirs(path_save, exist_ok=True)
df_temp.to_csv(file_path, index=False)
