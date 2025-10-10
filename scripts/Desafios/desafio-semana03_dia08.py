"""
Mini-Desafio – Dia 08
Tema: Comparando Commodities ao Longo do Ano

Criar gráficos comparativos de Produção e Exportações das
principais commodities ao longo dos meses, identificando padrões e sazonalidades.

Raciocínio do desafio

Antes de sair codando, pense assim:

O que quero comparar?
→ As commodities com maior volume de Produção e Exportação.
→ Quero ver se há meses em que aumentam ou caem.

Como estruturar os dados?
→ Agrupar por Mes e Commodity, somando os totais.
→ Converter os meses em ordem cronológica.

Como representar isso visualmente?

Linha → evolução no tempo.

Barras empilhadas → proporção entre commodities.

Boxplot → dispersão (opcional).

🧑‍🏫 Desafio prático
✳️ Tarefas

1️⃣ Agrupar o dataset por Mes e Commodity, somando Produção e Exportações.
2️⃣ Criar dois gráficos de linha:

Evolução da Produção mensal.

Evolução das Exportações mensais.

3️⃣ Criar um gráfico de barras empilhadas mostrando o total anual por commodity.
4️⃣ Adicionar título, legendas e rótulos formatados.
5️⃣ Salvar cada gráfico como imagem PNG em data/graficos/semana03_dia08/."""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from ClassesApoio.DataManager import DataManager

file = r'C:\Users\User\PycharmProjects\PythonProject\data\commodities_mes.csv'

df = pd.read_csv(file)

# 'Index', 'Mes', 'sum', 'mean', 'Commodity', 'Producao', 'Exportacoes','Outlier_IQR_Prod', 'Outlier_IQR_Expo', 'Z_Score'

ordem_m = ['Jan', 'Fev', 'Mar', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
df['Mes'] = pd.Categorical(df['Mes'], categories=ordem_m, ordered=True)

sumProd = df.groupby(['Mes', 'Commodity'], as_index=True, observed=True)['Producao'].sum()

sumExport = df.groupby(['Mes', 'Commodity'], as_index=True, observed=True)['Exportacoes'].sum()

df_agrupado = (
    df.groupby(['Mes', 'Commodity'], as_index=False, observed=True)[['Producao', 'Exportacoes']].sum()
)
# print(df_agrupado)
df_agrupado['Saldo'] = df_agrupado['Producao'] - df_agrupado['Exportacoes']
# print(df_agrupado['Saldo'])
df_agrupado['Commodity'] = df_agrupado['Commodity'].str.lower()

# Selecionar as 5Top Commodities
top5Ex = df_agrupado.groupby('Commodity')['Exportacoes'].sum().nlargest(5).index  # ele diz o top 5 por indice
df_top5Ex = df_agrupado[df_agrupado['Commodity'].isin(top5Ex)]  # ele diz as linhas para gerar o grafico
top5Prod = df_agrupado.groupby('Commodity')['Producao'].sum().nlargest(5).index
df_top5Prod = df_agrupado[df_agrupado['Commodity'].isin(top5Prod)]  # ele diz as linhas para gerar o grafico
# Graficos de linha Produção
sns.set_theme(style='whitegrid')

plt.figure(figsize=(10, 6))

ax = sns.lineplot(
    data=df_top5Prod,
    x='Mes',
    y='Producao',
    hue='Commodity',
    markers='o',
    linewidth=2.5,
)

# adicionando valores nas linhas
for line in ax.lines:
    y_data = line.get_ydata()
    x_data = line.get_xdata()
    if len(x_data) == len(y_data):
        for x, y in zip(x_data, y_data):
            ax.text(x, y, f'{y:.2f}', color=line.get_color(), fontsize=9, ha='center', va='bottom')

#---- Titulos e Eixos ---
plt.title('Evolução Mensal da Produção de Commodities - TOP 5 -', fontsize=16)
plt.xlabel('Mes')
plt.ylabel('Producao')
#--- Legenda ---
plt.legend(title='Commodity', title_fontsize=12, fontsize=10, loc='upper left', bbox_to_anchor=(1, 1))

plt.tight_layout()

DataManager.save_plot(filename='Evolução Mensal da Produção de Commodities - TOP 5 -', show=True)

soja = df_agrupado[df_agrupado['Commodity'] == 'soja']
milho = df_agrupado[df_agrupado['Commodity'] == 'milho']
print(soja[['Mes', 'Commodity', 'Producao', 'Exportacoes', 'Saldo']])
print()
print(milho[['Mes', 'Commodity', 'Producao', 'Exportacoes', 'Saldo']])
