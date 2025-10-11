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
from matplotlib.lines import lineStyles

from ClassesApoio import DataManager
from ClassesApoio.Format import dashboar_style
from scripts.Semana03.semana03_dia08 import ordem_meses

# ---- Carregando dataset -----
manager = DataManager.DataManager()

file = r'C:\Users\User\PycharmProjects\PythonProject\data\limpos\producao_mes_sem_outliers_20251008.csv'

df = pd.read_csv(file)
print(f'DataSet Carregado com sucesso: \n{df.shape}\n')

# ====== Ordenação Mensal ======
ordem_meses
df['Mes'] = pd.Categorical(df['Mes'],categories=ordem_meses,ordered=True,copy=True)

#==== Agrupamentos =====
df_mes = df.groupby(['Mes', 'Commodity'], as_index=False)[['Producao','Exportacoes']].sum()

#==== Calculo de Médias Moveis ====
df_mes['MM_Producao'] = df_mes.groupby('Commodity')['Producao'].transform(lambda x:x.rolling(3, min_periods=1).mean())
df_mes['MM_Exportacoes'] = df_mes.groupby('Commodity')['Exportacoes'].transform(lambda x:x.rolling(3, min_periods=1).mean())

#==== Gráfico de Tendencias====

dashboar_style(tema='whitegrid',context='talk',paleta='viridis')

plt.figure(figsize=(10,6))
sns.lineplot(
    data=df_mes,
    x='Mes',
    y='MM_Producao',
    hue='Commodity',
    linewidth = 2.5,

)

sns.lineplot(
    data=df_mes,
    x='Mes',
    y='MM_Exportacoes',
    hue='Commodity',
    linestyle=':',
    linewidth = 2.0,
    legend=False
)
#==== Titulos e Eixos ====
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

manager.save_files_clean('Tendencias_temporais_toop5', show=True)

#------ Calculo de Correlação Temporal ------
