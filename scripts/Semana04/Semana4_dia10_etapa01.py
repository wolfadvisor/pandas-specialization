"""
Engenharia de Dados – Semana 04, Dia 10
Análise de Exportações e Importações (ComexStat)
Autor: Carlos Ribbeiro
Objetivo: Consolidar dados de comércio exterior e gerar insights.
"""

# ---- Importações
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

from fontTools.subset import subset
from hypothesis.extra.pandas import columns

from ClassesApoio import Format
from ClassesApoio.Format import dashboar_style, remover_acentos

# === Configuração inicial e visual ===
dashboar_style(tema='whitegrid', context='talk', paleta='viridis')
sns.set_style('whitegrid')

# === Carregando Dataset ===

path_expo = r'C:\Users\User\PycharmProjects\PythonProject\data\brutos\EXP_2025_MUN.csv'
path_imp = r'C:\Users\User\PycharmProjects\PythonProject\data\brutos\IMP_2025_MUN.csv'
out_dir = r'C:\Users\User\PycharmProjects\PythonProject\reports\semana04_dia10'
os.makedirs(out_dir, exist_ok=True)

exp = pd.read_csv(path_expo, sep=';', quotechar='"')
imp = pd.read_csv(path_imp, sep=';', quotechar='"')

print(f'Exportações: \n{exp.shape}\n')
print(f'Importações: \n{imp.shape}\n')
# === Visualizando dados Exportações e Importações
# print(f'Exportações: \n{exp.info()}\n')

# print(f'Importações: \n{imp.info()}\n')

# ===== Padronização dos nomes ====
exp.columns = [remover_acentos(c.strip().upper().replace(' ', '_')) for c in exp.columns]
imp.columns = [remover_acentos(c.strip().upper().replace(' ', '_')) for c in imp.columns]
print(f'Colunas Exportação:\n', list(exp.columns)[:20])
print(f'Colunas Importação:\n', list(imp.columns)[:20])
# ==== Verificando duplicidade ====
print('\nVerificando duplicidade:', exp[['CO_ANO', 'SG_UF_MUN', 'CO_MUN']].duplicated().sum())
print('\nVerificando duplicidade:', exp[['CO_ANO', 'SG_UF_MUN', 'CO_MUN']].duplicated().sum())

exp = exp.drop_duplicates(subset=['CO_ANO', 'SG_UF_MUN', 'CO_MUN'])
imp = imp.drop_duplicates(subset=['CO_ANO', 'SG_UF_MUN', 'CO_MUN'])

print('\nVerificando duplicidade:', exp[['CO_ANO', 'SG_UF_MUN', 'CO_MUN']].duplicated().sum())
print('\nVerificando duplicidade:', exp[['CO_ANO', 'SG_UF_MUN', 'CO_MUN']].duplicated().sum())

# === Seleção de colunas relevantes ===

cols = ['CO_ANO', 'SG_UF_MUN', 'CO_MUN', 'VL_FOB']
for df_name, df in [('exp', exp), ('imp', imp)]:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f'Arquivo {df_name} esta com colunas esperadas:{missing}')

exp = exp[cols].copy().rename(columns={'VL_FOB': 'VL_EXPORT'})
imp = imp[cols].copy().rename(columns={'VL_FOB': 'VL_IMPORT'})

# === Conversor de valores numericos '.' -> ',' ===

exp['VL_EXPORT'] = (
    exp['VL_EXPORT'].astype(str)
    .str.replace('.', '', regex=False)
    .str.replace(',', '.', regex=False)
)
imp['VL_IMPORT'] = (
    imp['VL_IMPORT'].astype(str)
    .str.replace('.', '', regex=False)
    .str.replace(',', '.', regex=False)
)

exp['VL_EXPORT'] = pd.to_numeric(exp['VL_EXPORT'], errors='coerce').fillna(0)
imp['VL_IMPORT'] = pd.to_numeric(imp['VL_IMPORT'], errors='coerce').fillna(0)

# ==== Agrupamentos por municipios ===

exp_agg = exp.groupby(['CO_ANO', 'SG_UF_MUN', 'CO_MUN'], as_index=False, observed=True)['VL_EXPORT'].sum()
imp_agg = imp.groupby(['CO_ANO', 'SG_UF_MUN', 'CO_MUN'], as_index=False, observed=True)['VL_IMPORT'].sum()

# ==== Consolidação ====
df = pd.merge(exp_agg, imp_agg, on=['CO_ANO', 'SG_UF_MUN', 'CO_MUN'], how='outer')
df.fillna(0, inplace=True)
print(df.head())

# === Criação do Saldo Comercial ===
df['SALDO_COMERCIAL'] = df['VL_EXPORT'] - df['VL_IMPORT']

# === Estatisticas Iniciais ===
print(df.describe())

# === TOP 10 por ano 2025 ===
ANO = 2025  # ajustando o ano
df_ano = df[df['CO_ANO'] == ANO]

# === TOP 10 Municipios Exportadores ===
top_exp = (
    df.groupby(['SG_UF_MUN', 'CO_MUN'], as_index=False)['VL_EXPORT']
    .sum()
    .sort_values(by='VL_EXPORT', ascending=False)
    .head(7)
)
print(top_exp)
# --- Plot de Barras horizontais com nome dos estados e valores anotados
plt.figure(figsize=(12, 8))
sns.barplot(x='VL_EXPORT', y='SG_UF_MUN', hue='SG_UF_MUN', data=top_exp, palette='viridis', legend=False)
plt.title('Top 7 Municípios Exportadores – 2025')
plt.xlabel('Valor FOB (US$)')
plt.ylabel('UF')

# Anotar valores no final de cada barra
for i, (valor, mun) in enumerate(zip(top_exp['VL_EXPORT'], top_exp['SG_UF_MUN'])):
    plt.text(valor, i, f'  {valor:,.0f}', va='center', fontsize=10)

plt.tight_layout()
out_file = os.path.join(out_dir, f'Top7_municipios_exportadores_{ANO}.png')
plt.savefig(out_file, dpi=300)
plt.show()
print(f'Arquivo salvo: {out_file}')

# --- Também salvar tabela top10 em CSV ---
csv_out = os.path.join(out_dir, f'top7_municipios_exportadores_{ANO}.csv')
top_exp.to_csv(csv_out, index=False)
print(f'Tabela salva: {csv_out}')
