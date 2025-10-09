"""

Mini-desafio – Dia 07
Detecte outliers em Producao e Exportacoes usando o método IQR.
Crie uma nova coluna “Outlier” com True/False.
Substitua os outliers de Producao pela mediana.
Normalize ambas as colunas (Producao_Norm e Exportacoes_Norm).
Salve o arquivo como semana02_dia07_desafio.csv.

"""

import pandas as pd
from ClassesApoio import DataManager

manager = DataManager.DataManager()

# Ler arquivo
file = r'C:\\Users\\User\\PycharmProjects\\PythonProject\\data\\limpos\\producao_mes_arrumado.csv'

df = pd.read_csv(file)

sort = df.sort_values(by=['Mes'], ascending=True, inplace=True)

# Criando e verificando Outlier IQR Produção

Q1 = df['Producao'].quantile(0.25)

Q3 = df['Producao'].quantile(0.75)

IQR = Q3 - Q1

liminf = Q1 - 1.5 * IQR
limsup = Q3 + 1.5 * IQR

df['Outlier_IQR_Prod'] = (df['Producao'] < liminf) | (df['Producao'] > limsup)
print(df['Outlier_IQR_Prod'])
print(df)
# Criando e Verificando Outiliers IQr Exportações

Q1 = df['Exportacoes'].quantile(0.25)

Q3 = df['Exportacoes'].quantile(0.75)

IQR = Q3 - Q1

liminf = Q1 - 1.5 * IQR
limsup = Q3 + 1.5 * IQR

df['Outlier_IQR_Expo'] = (df['Exportacoes'] < liminf) | (df['Exportacoes'] > limsup)
print(df['Outlier_IQR_Expo'])
print(df)

# Desvio Padrao de Produção

media = df['Producao'].mean()
desvio = df['Producao'].std()

df['Z_Score'] = (df['Producao'] - media) / desvio

mediana = df.loc[abs(df['Z_Score']) > 3, 'Producao'] = df['Producao'].median()
print(mediana)
df.loc[df['Outlier_IQR_Prod'], 'Producao'] = df['Producao'].median()
print(df)

# salvar o resultado limpo sem outliers
# manager.save_files_clean(df,None,None)

# Normalizando Produção
df['Prod_Normalizado'] = (df['Producao'] - df['Producao'].min()) / (df['Producao'].max() - df['Producao'].min())

# Normalização atraves do Desvio Padrão
df['Z_Score_Normalizado'] = abs((df['Exportacoes'] - df['Exportacoes'].mean()) / df['Exportacoes'].std())

manager.save_files_clean(df, 'semana02_dia07_desafio', r'C:\Users\User\PycharmProjects\PythonProject\data')
