"""
Engenharia de Dados – Semana 03, Dia 10
Mini-Desafio: Tendência e Correlação Temporal
Autor: Carlos Ribbeiro
Objetivo: Identificar tendências e correlações
entre Produção e Exportações ao longo do tempo.
"""

# --- Importações ---

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from ClassesApoio.DataManager import DataManager as dm, DataManager
from ClassesApoio.Format import dashboar_style

from scripts.Desafios.desafio_semana02_dia07 import manager
from scripts.Semana03.semana03_dia08 import ordem_meses

# ---- Carregando dataset -----


file = r'C:\Users\User\PycharmProjects\PythonProject\data\limpos\producao_mes_sem_outliers_20251008.csv'

df = pd.read_csv(file)
print(f'DataSet Carregado com sucesso: \n{df.shape}\n')

# ====== Ordenação Mensal ======
ordem_meses
df['Mes'] = pd.Categorical(df['Mes'], categories=ordem_meses, ordered=True, copy=True)

# ==== Agrupamentos =====
df_mes = df.groupby(['Mes', 'Commodity'], as_index=False, observed=True)[['Producao', 'Exportacoes']].sum()

# ==== Calculo de Médias Moveis ====
df_mes['MM_Producao'] = df_mes.groupby('Commodity')['Producao'].transform(lambda x: x.rolling(3, min_periods=1).mean())
df_mes['MM_Exportacoes'] = df_mes.groupby('Commodity')['Exportacoes'].transform(
    lambda x: x.rolling(3, min_periods=1).mean())

# ==== Gráfico de Tendencias====

dashboar_style(tema='whitegrid', context='talk', paleta='viridis')

plt.figure(figsize=(10, 6))
sns.lineplot(
    data=df_mes,
    x='Mes',
    y='MM_Producao',
    hue='Commodity',
    linewidth=2.5,

)

sns.lineplot(
    data=df_mes,
    x='Mes',
    y='MM_Exportacoes',
    hue='Commodity',
    linestyle=':',
    linewidth=2.0,
    legend=False
)
# ==== Titulos e Eixos ====
plt.title('Tendência Temporal – Produção vs Exportações (Média Móvel 3M)')
plt.xlabel('Mês')
plt.ylabel('Toneladas (Média Móvel)')
plt.legend(
    title='Commodity',
    title_fontsize=12,
    fontsize=10,
    loc='upper left',
    bbox_to_anchor=(1, 1)
)
plt.tight_layout()

dm.save_files_clean(df_mes, 'Tendencias_temporais_toop5')

# ------ Calculo de Correlação Temporal ------

corr_temporal = (
    df.groupby('Commodity')[['Producao', 'Exportacoes']].corr().iloc[0::2, -1]
    .reset_index(level=1, drop=True)
    .rename('Corr_temporal')
)
print('Correlação Temporal de Produção vs Exportações por Commodity.')
print(corr_temporal)

# ====== Grafico de Dispersão (Correlação Visual) ========
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_mes, x='Producao', y='Exportacoes', hue='Commodity', s=100, alpha=0.8)
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df_mes, x='Producao', y='Exportacoes', hue='Commodity', s=100, alpha=0.8)
plt.title('Dispersão Temporal – Produção vs Exportações')
plt.xlabel('Produção (Toneladas)')
plt.ylabel('Exportações (Toneladas)')
plt.tight_layout()

DataManager.save_plot('dispersão_temporal_corr', show=True)

#======Relatório Final =========
corr_top = corr_temporal.nlargest(5)
print("\n🏆 Commodities com maior correlação temporal:")
print(corr_top)

manager.save_files_clean(df_mes,'semana03_dia10')
