"""
Desafio – Dia 02

Objetivo: Fixar operações com Series, criação de DataFrame e exportação de dados.

Use a Series de produção e exportação do Brasil.

Crie uma terceira Series chamada Consumo Interno Estimado = 70% do saldo interno.

Monte um DataFrame consolidado com:

Produção - Exportações - Saldo Interno - Consumo Interno Estimado

Estoque Final = Saldo Interno - Consumo Estimado

Salve esse DataFrame como CSV (data/desafio_dia02.csv).

Extra: Calcule a commodity com maior estoque final e exiba no terminal.
"""
import os

import pandas as pd

prodBR = pd.Series([25000, 35000, 55000, 75000,0],
                   index=['Milho', 'Soja', 'Açucar', 'Minerio de Ferro','Café'],
                   name='Prod_Commodities_BR')
exportaBR = pd.Series([15000, 25000, 10000, 5000,0],
                      index=['Milho', 'Soja','Açucar', 'Minerio de Ferro', 'Café'],
                      name='Export_Commodity_BR')

saldoBr = prodBR - exportaBR
consumo_interno = saldoBr * 0.70
estoque_final = saldoBr - consumo_interno

df = pd.DataFrame({
    "Produção": prodBR,
    "Exportação": exportaBR,
    "Saldo Interno": saldoBr,
    "Consumo Interno": consumo_interno,
    "Estoque Final": estoque_final
})
#salvando as séries emcsv
path_csv = r'C:\\Users\\User\\PycharmProjects\\PythonProject\\data'
os.makedirs(path_csv,exist_ok=True)
#Nome do arquivo
file_exporta = os.path.join(path_csv,"exportaBr.csv")
file_df = os.path.join(path_csv,"commoditiesBR.csv")
#Salvando as séries e o Dataframe
exportaBR.to_csv(file_exporta,index=True)
df.to_csv(file_df,index=True)
#Debug salvamento
print(f"✅ Arquivo salvo em: {path_csv}")
print("Existe mesmo?", os.path.exists(path_csv))

maior_estoque = df['Estoque Final'].idxmax()
linha_max = df.loc[df['Exportação'].idxmax()]
print(maior_estoque)
print(linha_max)
#print(df)
