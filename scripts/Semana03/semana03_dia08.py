# Dia 08 – Visualização de Dados com Matplotlib e Seaborn
# Objetivo: Criar gráficos de linha para evolução mensal das commodities

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

from matplotlib.pyplot import title
from pandas.conftest import index

from ClassesApoio.DataManager import DataManager

#Configurando estetica global do Seaborn
sns.set_theme(style='whitegrid',palette='pastel',context="talk")

#Carregando o DataSet Limpo.

filepath = r'C:/Users/User/PycharmProjects/PythonProject/data/limpos/producao_mes_arrumado.csv'

df= pd.read_csv(filepath)

#Agrupar dados por Mês e e Commodity e somar Produção e Exportação
#df['Exportacoes'] = df['Exportacoes'].map(lambda x:f'{x:.2f}MT')
df_groupby_Month_Commodity = df.groupby(['Mes','Commodity'],as_index=False)[['Producao','Exportacoes']].sum().round(2)
#print(df_groupby_Month_Commodity)

#Fazer um Ranking Top 3Mais produzidas e mais exportadas
top3Prod = df_groupby_Month_Commodity.groupby('Commodity')['Producao'].sum().nlargest(3).index
df_top3Prod = df_groupby_Month_Commodity[df_groupby_Month_Commodity['Commodity'].isin(top3Prod)].copy()
print(top3Prod)
print(df_top3Prod)
top3Export =df_groupby_Month_Commodity.groupby('Commodity')['Exportacoes'].sum().nlargest(3).index
df_top3Export =df_groupby_Month_Commodity[df_groupby_Month_Commodity['Exportacoes'].isin(top3Export)].copy()
#print(df.info())
print(top3Export)
print(df_top3Export)

#Colocar os meses em ordem cronologica
ordem_meses = ['Jan','Fev','Mar','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
df_top3Prod['Mes'] = pd.Categorical(df_top3Prod['Mes'],categories=ordem_meses, ordered=True)
df_top3Export['Mes'] = pd.Categorical(df_top3Export['Mes'], categories=ordem_meses,ordered=True)

#Plotar a evolução da produção e exportação

plt.figure(figsize=(10,6))
sns.lineplot(data=df_top3Prod,x='Mes',y='Producao',hue='Commodity',markers=0)
plt.title('Evolução Mensal da Produção de Commodity',fontsize=14)
plt.xlabel('Mês')
plt.ylabel('Produção (Toneladas)')
plt.legend(title='Commodity')
plt.tight_layout()
DataManager.save_plot(filename='evolucao-mensal-producao-commodities',show=True)
plt.show()

plt.figure(figsize=(10,6))
sns.lineplot(data=df_top3Prod,x='Mes',y='Exportacoes',hue='Commodity',markers='o')
plt.title('Evolução Mensal da Exportações de Commodity',fontsize=14)
plt.xlabel('Mês')
plt.ylabel('Exportações (Toneladas)')
plt.legend(title='Commodity')
plt.tight_layout()


DataManager.save_plot(filename='evolucao-mensal-exportacoes-commodities',show=True)
plt.show()