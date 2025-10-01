import os

import pandas as pd



#Criar uma nova serie de dados para atualizar o arquivo csv de exportações

df = pd.read_csv(r'C:\\Users\\User\\PycharmProjects\\PythonProject\\data\\commodities_mes.csv')
print(df.info())

nova_linha =pd.DataFrame([
    {'Mes': 'Abr', 'Commodity' : 'Milho', 'Producao' : 62000,'Exportacoes': 21000},
    {'Mes': 'Abr', 'Commodity' : 'Soja', 'Producao' : 32000,'Exportacoes': 29000},
    {'Mes': 'Abr', 'Commodity' : 'Algodão', 'Producao' : 92000,'Exportacoes': 51000}
])


df = pd.concat([df, nova_linha], ignore_index=True)
print(df)

#Filtrar Commodities acima da média
#descobrir a média
#print(df.describe().round(2))
acimaMedia = df[df['Exportacoes']>= 24416.67]
print(acimaMedia)
soma_por_commodity = df.groupby('Mes')['Producao'].sum()
print(soma_por_commodity)
soma_mes_commodity = df.groupby(['Mes','Commodity'])['Exportacoes'].sum()
print(soma_mes_commodity)

#salvar arquivos
file_acimaMedia = os.path.join(r'C:\\Users\\User\\PycharmProjects\\PythonProject\\data','acimaMedia.csv')
acimaMedia.to_csv(file_acimaMedia,index=True)