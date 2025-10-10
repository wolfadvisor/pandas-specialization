"""
Mini-Desafio – Dia 08: Comparando Commodities ao Longo do Ano
Tema: Análise visual da Produção e Exportações das principais commodities.
Objetivo: Identificar padrões sazonais e comparativos entre commodities.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from ClassesApoio.DataManager import DataManager
from ClassesApoio.Format import dashboar_style

# --- Carregar dataset ---
file = r'C:\Users\User\PycharmProjects\PythonProject\data\commodities_mes.csv'
df = pd.read_csv(file)

# --- Ordenar meses corretamente ---
ordem_m = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
df['Mes'] = pd.Categorical(df['Mes'], categories=ordem_m, ordered=True)

# --- Agrupar dados ---
df_agrupado = df.groupby(['Mes', 'Commodity'], as_index=False)[['Producao', 'Exportacoes']].sum()
df_agrupado['Saldo'] = df_agrupado['Producao'] - df_agrupado['Exportacoes']
df_agrupado['Commodity'] = df_agrupado['Commodity'].str.lower()

# --- Top 5 Commodities por Produção e Exportação ---
top5_prod = df_agrupado.groupby('Commodity')['Producao'].sum().nlargest(5).index
top5_exp = df_agrupado.groupby('Commodity')['Exportacoes'].sum().nlargest(5).index

df_top5_prod = df_agrupado[df_agrupado['Commodity'].isin(top5_prod)]
df_top5_exp = df_agrupado[df_agrupado['Commodity'].isin(top5_exp)]

# --- Configuração de tema global ---
sns.set_theme(style='whitegrid', palette='tab10')

# ==========================================================
# 📊 Gráfico 1 – Evolução Mensal da Produção
# ==========================================================
plt.figure(figsize=(10, 6))
ax = sns.lineplot(
    data=df_top5_prod,
    x='Mes',
    y='Producao',
    hue='Commodity',
    marker='o',
    linewidth=2.5
)
for line in ax.lines:
    y_data = line.get_ydata()
    x_data = line.get_xdata()
    if len(x_data) == len(y_data):
        for x, y in zip(x_data, y_data):
            ax.text(x, y, f'{y:.2f}', color=line.get_color(),
                    fontsize=9, ha='center', va='bottom')

plt.title('Evolução Mensal da Produção - Top 5 Commodities', fontsize=14)
plt.xlabel('Mês')
plt.ylabel('Produção (toneladas)')
plt.legend(title='Commodity', title_fontsize=12, fontsize=10, loc='upper left', bbox_to_anchor=(1, 1))
plt.tight_layout()
DataManager.save_plot(filename='semana03_dia08_Producao', show=True)

# ==========================================================
# 📊 Gráfico 2 – Evolução Mensal das Exportações
# ==========================================================
dashboar_style(tema='whitegrid', context='talk', paleta='coolwarm')
plt.figure(figsize=(10, 6))
ax = sns.lineplot(
    data=df_top5_exp,
    x='Mes',
    y='Exportacoes',
    hue='Commodity',
    marker='s',
    linewidth=2.5
)

for line in ax.lines:
    y_data = line.get_ydata()
    x_data = line.get_xdata()
    if len(x_data) == len(y_data):
        for x, y in zip(x_data, y_data):
            ax.text(x, y, f'{y:.2f}', color=line.get_color(),
                    fontsize=9, ha='center', va='bottom')


plt.title('Evolução Mensal das Exportações - Top 5 Commodities', fontsize=14)
plt.xlabel('Mês')
plt.ylabel('Exportações (toneladas)')
plt.legend(title='Commodity', title_fontsize=12, fontsize=10, loc='upper left', bbox_to_anchor=(1, 1))
plt.tight_layout()
DataManager.save_plot(filename='semana03_dia08_Exportacoes', show=True)

# ==========================================================
# 📊 Gráfico 3 – Barras Empilhadas Produção vs Exportações
# ==========================================================
df_total = df_agrupado.groupby('Commodity')[['Producao', 'Exportacoes']].sum().reset_index()

df_total.plot(
    x='Commodity',
    kind='bar',
    stacked=True,
    figsize=(10, 6),
    color=['#4e79a7', '#f28e2b']
)
plt.title('Produção e Exportações Totais por Commodity (Ano Completo)', fontsize=14)
plt.ylabel('Toneladas')
plt.xlabel('Commodity')
plt.legend(title='Commodity', title_fontsize=12, fontsize=10, loc='upper left', bbox_to_anchor=(1, 1))
plt.tight_layout()
DataManager.save_plot(filename='semana03_dia08_BarrasEmpilhadas', show=True)

print("✅ Desafio do Dia 08 finalizado com sucesso!")


