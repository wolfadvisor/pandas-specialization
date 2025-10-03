"""
Dia 04 – Agrupamento e Análise Exploratória de Commodities:
Objetivos
Usar groupby para calcular métricas por Mês e por Commodity.
Calcular estatísticas como soma, média, máximo e mínimo.
Criar tabelas dinâmicas (pivot tables) no pandas.
Salvar resultados em múltiplos formatos (CSV e Excel).
"""

import pandas as pd

file = r'C:\\Users\\User\\PycharmProjects\\PythonProject\\data\\commodities_mes.csv'
# Lendo o data set atualizado
df =  pd.read_csv(file)
print('DATASET Carregado com sucesso!')
print(df.head()) # Demonstra os 5 primeiros itens
print(df.info())

#Estatisticas de Exportação por Commodity:
exportByCommodity = df.groupby('Commodity')['Exportacoes'].agg(['sum','mean','max','min'])
print('\nEstatisticas de exportações por Commodity.')
print(exportByCommodity.round(2))

#Dados de Produção Mensal
productionByMonth = df.groupby("Mes")['Producao'].agg(['sum','mean'])
print(productionByMonth.round(2))

#PivotTable Mês x Commodity
pivot_export = pd.pivot_table(df, values="Exportacoes", index="Mes", columns="Commodity", aggfunc="sum", fill_value=0)
print("\nPivot Table - Exportações por Mês e Commodity:")
print(pivot_export)

#PivotTable: Mês x Commmodity => Produção e Exportação
pivot_full = pd.pivot_table(df, values=['Producao','Exportacoes'], index='Mes',columns='Commodity',aggfunc='sum',fill_value=0)
print(pivot_full)

#Salvando e atuaizando arquivos em varios formatos
exportByCommodity.to_csv(r'C:\\Users\\User\\PycharmProjects\\PythonProject\\data\\estatisticas_export')
productionByMonth.to_csv(r'C:\\Users\\User\\PycharmProjects\\PythonProject\\data\\producao_mes')
pivot_export.to_excel(r'C:\\Users\\User\\PycharmProjects\\PythonProject\\data\\pivot_export.xlsx')

print('\n✅ Arquivos salvos com sucesso (CSV e Excel).')