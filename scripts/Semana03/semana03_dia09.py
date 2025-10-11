"""
Engenharia de Dados – Semana 02, Dia 09
Tema: Correlação e Análise Exploratória Avançada
Autor: Carlos Ribbeiro
Objetivo: Calcular correlações, visualizar padrões e salvar resultados.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ClassesApoio import DataManager

#---- Carregamento dataset
manager = DataManager.DataManager()

file = r'C:\Users\User\PycharmProjects\PythonProject\data\limpos\producao_mes_sem_outliers_20251008.csv'
df = pd.read_csv(file)

#---- verificação basica

print('\n Estrutura Básica.')
print(df.info())
print('\n Primeiras linhas:')
print(df.head())

#Garantir que não ha outliers
print('Outliers remanescente por colunas:')
print(df[['Outlier_IQR_Prod', 'Outlier_IQR_Expo']].sum())

#Estatisticas descritivas gerais
print('\n Estatisticas descritivas globais.')
print(df[['Producao','Exportacoes']].describe())

#Estaticas por Commodity
stats_commodity = df.groupby('Commodity')[['Producao','Exportacoes']].agg(['mean','median','sum','std','min',"max"])
print('\n Estatistica por Commodity.')
print(stats_commodity)

#Estaticas por Mês
stats_mes = df.groupby('Mes')[['Producao','Exportacoes']].agg(['mean','sum'])
print('\n Estatistica por Commodity.')
print(stats_mes)

#Correlação entre Produção e Exportação
correlacao = df[['Producao','Exportacoes']].corr()
print('\n Correlação Produção x Exportação:')
print(correlacao)

#---- Calculo de correlações
correlacao = df[['Producao','Exportacoes']].corr(method='pearson')
print('Matriz de Correlação:\n',correlacao)

#Correlação por Commodities:
corr_por_commodities = (
    df.groupby('Commodity')[['Producao','Exportacoes']]
    .corr(method='pearson')
    .iloc[0::2, -1] # Extrai apenas a correlação Produção vs Exportações
    .reset_index(level=1, drop=True)
    .rename('Correlacao_PxE')
    .sort_values(ascending=True)
)
print(corr_por_commodities)

df = df.merge(corr_por_commodities,on='Commodity',how='left')
print(df)
df_filtrado = df[df['Correlacao_PxE']> 0.75]
df_filtrado_top5 = df_filtrado.nlargest(5,'Correlacao_PxE')
df_filter_commodity = corr_por_commodities[corr_por_commodities > 0.75]
df_filter_commodity_index = corr_por_commodities[corr_por_commodities > 0.75].reset_index()

print(f'Correlação filtrada \n{df_filtrado}\n')

print(f'Correlação Top5 \n{df_filtrado_top5}\n')

print(f'Correlação por Commodity alta: \n{df_filter_commodity}\n')

print(f'Correlação por Commodity alta indexada: \n{df_filter_commodity_index}\n')

df_filtrado = df[df['Correlacao_PxE'] > 0.75]
df_top5 = df_filtrado.nlargest(5, 'Correlacao_PxE')

print(f'\n🔝 Top 5 Commodities com maior correlação:\n{df_top5[["Commodity","Correlacao_PxE"]].drop_duplicates()}\n')

#==============================#
#   ETAPA 4: VISUALIZAÇÕES     #
#==============================#
plt.figure(figsize=(6,4))
sns.heatmap(correlacao, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Matriz de Correlação - Global')
plt.show()

plt.figure(figsize=(8,5))
sns.scatterplot(x='Producao', y='Exportacoes', hue='Commodity', data=df, alpha=0.7)
plt.title('Dispersão Produção vs Exportações por Commodity')
plt.show()

#==============================#
#   ETAPA 5: SALVAMENTO        #
#==============================#
path = r'C:\Users\User\PycharmProjects\PythonProject\data\resultados'
manager.save_files_clean(df, 'semana02_dia09_correlacao', path)

print('\n✅ Arquivo salvo com sucesso: semana02_dia09_correlacao.csv')