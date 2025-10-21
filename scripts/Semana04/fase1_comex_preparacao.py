"""
fase1_comex_preparacao.py
Engenharia de Dados – Semana 04, Dia 10
Autor: Carlos Ribbeiro (adaptado)
Objetivo: preparar dados COMEX (EXP_2025_MUN + IMP_2025_MUN),
gerar Top lists, gráficos (com nomes e valores anotados) e sumarização por UF.
"""

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from ClassesApoio import Format as fr,PlotManager,DataManager as dm,Dashboard as ds

# --------------------------
# Configurações visuais e paths
# --------------------------

ds.Dashboard.dashboar_style(tema='whitegrid', context='talk', paleta='viridis')
sns.set_style('whitegrid')

PATH_EXP = r'C:\Users\User\PycharmProjects\PythonProject\data\brutos\EXP_2025_MUN.csv'
PATH_IMP = r'C:\Users\User\PycharmProjects\PythonProject\data\brutos\IMP_2025_MUN.csv'
OUT_DIR = r'C:\Users\User\PycharmProjects\PythonProject\reports\semana04_dia10'
os.makedirs(OUT_DIR, exist_ok=True)

# --------------------------
# Leitura (ajuste encoding/sep se necessário)
# --------------------------
exp = pd.read_csv(PATH_EXP, sep=';', quotechar='"', encoding='latin1', low_memory=False)
imp = pd.read_csv(PATH_IMP, sep=';', quotechar='"', encoding='latin1', low_memory=False)

print(f'Exportações: {exp.shape}')
print(f'Importações: {imp.shape}')

# --------------------------
# Padronização de colunas
# --------------------------
exp.columns = [fr.remover_acentos(c.strip().upper().replace(' ', '_')) for c in exp.columns]
imp.columns = [fr.remover_acentos(c.strip().upper().replace(' ', '_')) for c in imp.columns]

print('Colunas export:', exp.columns.tolist()[:20])
print('Colunas import:', imp.columns.tolist()[:20])

# --------------------------
# Verifica existência de colunas de nome do município
# --------------------------
# Preferimos exibir NM_MUN (nome). Se ausente, usaremos CO_MUN.
nome_mun_col = 'NM_MUN' if 'NM_MUN' in exp.columns else None
if nome_mun_col is None:
    print("Atenção: coluna 'NM_MUN' NÃO encontrada — usarei CO_MUN como rótulo legível (código).")

# --------------------------
# Seleção de colunas mínimas esperadas
# --------------------------
REQUIRED = ['CO_ANO', 'SG_UF_MUN', 'CO_MUN', 'VL_FOB']
for df_name, df in [('exp', exp), ('imp', imp)]:
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Arquivo {df_name} está sem colunas esperadas: {missing}")

# Prepare seleções: se NM_MUN existe, we'll add it later when grouping for display
exp_sel = exp[REQUIRED + (['NM_MUN'] if 'NM_MUN' in exp.columns else [])].copy()
imp_sel = imp[REQUIRED + (['NM_MUN'] if 'NM_MUN' in imp.columns else [])].copy()

exp_sel = exp_sel.rename(columns={'VL_FOB': 'VL_EXPORT'})
imp_sel = imp_sel.rename(columns={'VL_FOB': 'VL_IMPORT'})

# --------------------------
# Conversão robusta de valores VL_FOB -> float
# --------------------------
def to_numeric_fob(series):
    s = series.astype(str).str.strip()
    # Remover pontos milhares e transformar vírgula decimal em ponto
    s = s.str.replace(r'\.', '', regex=True)
    s = s.str.replace(',', '.', regex=False)
    return pd.to_numeric(s, errors='coerce')

exp_sel['VL_EXPORT'] = to_numeric_fob(exp_sel['VL_EXPORT']).fillna(0)
imp_sel['VL_IMPORT'] = to_numeric_fob(imp_sel['VL_IMPORT']).fillna(0)

# --------------------------
# Drop de duplicatas por chave (ano, uf, municipio)
# --------------------------
exp_sel = exp_sel.drop_duplicates(subset=['CO_ANO', 'SG_UF_MUN', 'CO_MUN'])
imp_sel = imp_sel.drop_duplicates(subset=['CO_ANO', 'SG_UF_MUN', 'CO_MUN'])

# --------------------------
# Agregação por município (mantendo NM_MUN se existir)
# --------------------------
group_cols = ['CO_ANO', 'SG_UF_MUN', 'CO_MUN']
if 'NM_MUN' in exp_sel.columns:
    group_cols_with_name = group_cols + ['NM_MUN']
    exp_agg = exp_sel.groupby(group_cols_with_name, as_index=False)['VL_EXPORT'].sum()
    imp_agg = imp_sel.groupby(group_cols_with_name, as_index=False)['VL_IMPORT'].sum()
else:
    exp_agg = exp_sel.groupby(group_cols, as_index=False)['VL_EXPORT'].sum()
    imp_agg = imp_sel.groupby(group_cols, as_index=False)['VL_IMPORT'].sum()

# --------------------------
# Merge outer e preenchimento
# --------------------------
merge_cols = group_cols + (['NM_MUN'] if 'NM_MUN' in exp_sel.columns else [])
df = pd.merge(exp_agg, imp_agg, on=merge_cols, how='outer')
df[['VL_EXPORT','VL_IMPORT']] = df[['VL_EXPORT','VL_IMPORT']].fillna(0)
df['SALDO_COMERCIAL'] = df['VL_EXPORT'] - df['VL_IMPORT']

# Salvar arquivo fase 1 (opcional, pode ser importado na fase 2)
csv_fase1 = os.path.join(OUT_DIR, 'fase1_comex_preparado_2025.csv')
df.to_csv(csv_fase1, index=False)
print('Arquivo fase1 salvo:', csv_fase1)

# --------------------------
# Filtros por ano e preparação top lists
# --------------------------
ANO = 2025
df_ano = df[df['CO_ANO'] == ANO].copy()
if df_ano.empty:
    print(f"Aviso: não foram encontradas linhas para o ano {ANO}")

# Decidir label para exibir: NM_MUN se existir, caso contrário CO_MUN
label_col = 'NM_MUN' if 'NM_MUN' in df_ano.columns else 'CO_MUN'

# Top 10 municípios exportadores e importadores
top_exp = df_ano.groupby([label_col, 'SG_UF_MUN'], as_index=False)['VL_EXPORT'].sum().sort_values(by='VL_EXPORT', ascending=False).head(10)
top_imp = df_ano.groupby([label_col, 'SG_UF_MUN'], as_index=False)['VL_IMPORT'].sum().sort_values(by='VL_IMPORT', ascending=False).head(10)

# Salva CSVs top lists
top_exp.to_csv(os.path.join(OUT_DIR, f'top10_municipios_exportadores_{ANO}.csv'), index=False)
top_imp.to_csv(os.path.join(OUT_DIR, f'top10_municipios_importadores_{ANO}.csv'), index=False)

# --------------------------
# Função utilitária para plot horizontal com anotações
# --------------------------
def plot_horizontal_top(df_top, value_col, label_col, title, outname, palette='viridis'):
    plt.figure(figsize=(12, 8))
    sns.barplot(x=value_col, y=label_col, data=df_top, palette=palette, orient='h')
    plt.title(title)
    plt.xlabel('Valor FOB (US$)')
    plt.ylabel('Município / UF')
    # anotar valores ao final da barra
    for i, (v, lbl) in enumerate(zip(df_top[value_col], df_top[label_col])):
        plt.text(v, i, f'  {v:,.0f}', va='center', fontsize=9)
    plt.tight_layout()
    fp = os.path.join(OUT_DIR, outname)
    plt.savefig(fp, dpi=300)
    plt.show()
    print('Gráfico salvo:', fp)

# Plot Top Exportadores
plot_horizontal_top(
    df_top=top_exp,
    value_col='VL_EXPORT',
    label_col=label_col + ' ( ' + 'SG_UF_MUN' + ' )' if label_col=='NM_MUN' else label_col,
    title=f'Top 10 Municípios Exportadores – {ANO}',
    outname=f'top10_municipios_exportadores_{ANO}.png'
)

# Plot Top Importadores
plot_horizontal_top(
    df_top=top_imp,
    value_col='VL_IMPORT',
    label_col=label_col + ' ( ' + 'SG_UF_MUN' + ' )' if label_col=='NM_MUN' else label_col,
    title=f'Top 10 Municípios Importadores – {ANO}',
    outname=f'top10_municipios_importadores_{ANO}.png'
)

# --------------------------
# Gráfico comparativo side-by-side por UF (estado)
# --------------------------
# Agregar por UF (estado)
df_uf = df_ano.groupby('SG_UF_MUN', as_index=False)[['VL_EXPORT','VL_IMPORT']].sum()
df_uf['SALDO'] = df_uf['VL_EXPORT'] - df_uf['VL_IMPORT']
csv_uf = os.path.join(OUT_DIR, f'comex_uf_sum_{ANO}.csv')
df_uf.to_csv(csv_uf, index=False)
print('Tabela por UF salva:', csv_uf)

# Para comparar export vs import: transformar para long
df_uf_long = df_uf.melt(id_vars='SG_UF_MUN', value_vars=['VL_EXPORT','VL_IMPORT'], var_name='Tipo', value_name='Valor')
df_uf_long['Tipo'] = df_uf_long['Tipo'].map({'VL_EXPORT':'Exportações','VL_IMPORT':'Importações'})

plt.figure(figsize=(14,10))
sns.barplot(data=df_uf_long, x='Valor', y='SG_UF_MUN', hue='Tipo', palette=['seagreen','darkorange'])
plt.title(f'Exportações vs Importações por UF – {ANO}')
plt.xlabel('Valor FOB (US$)')
plt.ylabel('UF')

# anotar valores em cada barra (usa containers)
ax = plt.gca()
for container in ax.containers:
    plt.bar_label(container, fmt='%.0f', label_type='edge', fontsize=9)

fp = os.path.join(OUT_DIR, f'Comparativo_Exportadores_vs_Importadores_{ANO}.png')
plt.tight_layout()
plt.savefig(fp, dpi=300)
plt.show()
print('Comparativo salvo:', fp)

# --------------------------
# Gráfico espelhado (exportações à direita; importações à esquerda)
# --------------------------
# ordena UF por export para layout
df_uf_sorted = df_uf.sort_values('VL_EXPORT', ascending=True)
y = df_uf_sorted['SG_UF_MUN']

exp_vals = df_uf_sorted['VL_EXPORT'].values
imp_vals = -df_uf_sorted['VL_IMPORT'].values  # negativo para espelhar à esquerda

plt.figure(figsize=(14,10))
plt.barh(y, exp_vals, color='seagreen', label='Exportações')
plt.barh(y, imp_vals, color='darkorange', label='Importações (negativo)')
plt.title(f'Exportações (direita) vs Importações (esquerda) por UF – {ANO}')
plt.xlabel('Valor FOB (US$)')
plt.legend()

# Anotações: export à direita, import à esquerda (valores positivos na string)
for i, (e, m) in enumerate(zip(exp_vals, -imp_vals)):
    plt.text(e + max(exp_vals)*0.01, i, f'{e:,.0f}', va='center', color='black', fontsize=9)
    plt.text(-m - max(exp_vals)*0.01, i, f'{m:,.0f}', va='center', color='black', fontsize=9, ha='right')

fp = os.path.join(OUT_DIR, f'Comparativo_espelhado_UF_{ANO}.png')
plt.tight_layout()
plt.savefig(fp, dpi=300)
plt.show()
print('Espelhado salvo:', fp)

print('\n== Fase 1 concluída: arquivos salvos em', OUT_DIR)


