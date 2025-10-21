# Importando as classes

from ClassesApoio import DataManager as dm
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# === Instanciar a classe
data_manager = dm()
df = data_manager.carregar_fase1()

# === Conferencia de daos
print('Verificando dados:\n')
print(df.head())
print(df.columns.tolist())
# === Criando as colunas de percentuais por Estados.
df.columns = df.columns.str.strip().str.upper()
df_uf = df.groupby('SG_UF_MUN', as_index=False)[['VL_EXPORT', 'VL_IMPORT']].sum()

df_uf['SALDO'] = df_uf['VL_EXPORT'] - df_uf['VL_IMPORT']
print(f'Este e o Saldo Comercial:\n{df_uf["SALDO"]}\n')

# Quais as regioes que são mais consumidoras

df_uf['CONSUMO_NORMALIZADO'] = ((df_uf['VL_IMPORT'] - df_uf['VL_IMPORT'].min()) / (df_uf['VL_IMPORT'].max() - df_uf['VL_IMPORT'].min()))
print('Região Com Maior Consumo Normalizado:\n',df_uf.sort_values(by='CONSUMO_NORMALIZADO',ascending=False).head(10))

df_uf['VENDEDORA_NORMALIZADA'] = ((df_uf['VL_EXPORT'] - df_uf['VL_EXPORT'].min()) / (df_uf['VL_EXPORT'].max() - df_uf['VL_EXPORT'].min()))
print('Região Com Maior Vendas Normalizadas:\n',df_uf.sort_values(by='VENDEDORA_NORMALIZADA',ascending=False).head(10))

df_uf['PERC_EXPORT'] = df_uf['VL_EXPORT'] / df_uf['VL_EXPORT'].sum() * 100
df_uf['PERC_IMPORT'] = df_uf['VL_IMPORT'] / df_uf['VL_IMPORT'].sum() * 100


top10_percExport =df_uf.nlargest(10,'VL_EXPORT')
print(top10_percExport)
top10_percImport= df_uf.nlargest(10,'VL_IMPORT')
print(top10_percImport)

f =df.merge(df_uf[['SG_UF_MUN','PERC_EXPORT','PERC_IMPORT','CONSUMO_NORMALIZADO','VENDEDORA_NORMALIZADA']], on='SG_UF_MUN', how='left')
# === Exibir resumo
pd.options.display.float_format = '{:,.2f}'.format
print('\nResumo por UF:')
print(df_uf.columns)

print(df_uf[['SG_UF_MUN','CONSUMO_NORMALIZADO','VENDEDORA_NORMALIZADA']])




fig = px.choropleth(
    df_uf,
    geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
    locations="SG_UF_MUN",
    featureidkey="properties.sigla",
    color="VL_EXPORT",
    color_continuous_scale="Viridis",
    title="Exportações por Estado (2025)"
)
fig.update_geos(fitbounds="locations", visible=False)
fig.show()

# Correlação Pearson e Spearman
corr_pearson = df_uf['VL_EXPORT'].corr(df_uf['VL_IMPORT'], method='pearson')
corr_spearman = df_uf['VL_EXPORT'].corr(df_uf['VL_IMPORT'], method='spearman')

print(f"Correlação de Pearson: {corr_pearson:.4f}")
print(f"Correlação de Spearman: {corr_spearman:.4f}")

corr_matrix = df_uf[['VL_EXPORT','VL_IMPORT','SALDO','CONSUMO_NORMALIZADO','VENDEDORA_NORMALIZADA']].corr(method='pearson')

plt.figure(figsize=(8,6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Matriz de Correlação – Exportações, Importações e Indicadores Normalizados')
plt.tight_layout()
plt.show()
