"""
Dia 03 – Trabalhando com Arquivos Externos (CSV → DataFrame)
🎯 Objetivos

Ler dados de um CSV maior (vários meses, várias commodities).

Explorar o DataFrame com .head(), .tail(), .info(), .shape, .describe().

Selecionar colunas e linhas.

Filtrar dados por condições.

Salvar em outro formato (JSON).

"""

import pandas as pd

#ler dados de um .csv

df = pd.read_csv("C:\\Users\\User\\PycharmProjects\\PythonProject\\data\\commodities_mes.csv")
#print("Arquivo carregado com sucesso")

#Explorando o arquivo
print(f'Lendo as primeiras 5 linhas\n',df.head(5))
print(f'Lendo as ultimas 5 linhas\n', df.tail(5))
print('Resumo de informações do data frame', df.info())
print('Resumo estatistico das colunas numéricas:\n', df.describe().round(2))

#Selecionando colunas
print('Colunas de Exportações:')
print(df["Exportacoes"])
print("\nProdução e Exportações:")
print(df[["Producao", "Exportacoes"]])

#Filtro de linha
soja = df[df['Commodity']=='Soja']
print('Dados da Soja')
print(soja)

filtro = df[df['Producao'] > 60000]
print("\nCommodities com produção acima de 60.000 MT:\n")
print(filtro)

#salvando em json
df.to_json("C:\\Users\\User\\PycharmProjects\\PythonProject\\data\\semana01_dia03.json",orient="records", indent=4)
print('\n Arquivo salvo tambem em formato Json')