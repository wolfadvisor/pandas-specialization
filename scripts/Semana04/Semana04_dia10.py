"""
Engenharia de Dados – Semana 04, Dia 10
Tema: Modelagem Preditiva Simples
Autor: Carlos Ribbeiro
Objetivo: Prever Exportações com base na Produção
utilizando Regressão Linear.
"""
# === Importações ===
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

from ClassesApoio.DataManager import DataManager

# Carregando DataSet
file = r'C:\Users\User\PycharmProjects\PythonProject\data\limpos\producao_mes_sem_outliers_20251008.csv'
df = pd.read_csv(file)

print(f'Dataset carregado: \n{df.shape}\n')
print(df.head())

# === Selecionar variáveis
x = df[['Producao']]
y = df['Exportacoes']

# === Divisão entre treino e teste ====
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

# === Verificando colunas  que possuem valores ausentes

x_train = x_train.dropna()
y_train = y_train.loc[x_train.index]

x_test = x_test.dropna()
y_test =y_test.loc[x_test.index]


# ==== Treinando modelo ====
modelo = LinearRegression()
modelo.fit(x_train, y_train)

# ====Previsões====
y_pred = modelo.predict(x_test)

#==== Avaliação ====
r2 = r2_score(y_test,y_pred)
rmse = np.sqrt(mean_squared_error(y_test,y_pred))

print(f"\nCoeficiente angular (b): {modelo.coef_[0]:.4f}")
print(f"Intercepto (a): {modelo.intercept_:.4f}")
print(f"R²: {r2:.4f}")
print(f"RMSE: {rmse:.2f}")

# === Visualização ===
sns.scatterplot(x=y_test, y=y_pred)
plt.title("Previsão vs Valores Reais – Exportações")
plt.xlabel("Valores Reais")
plt.ylabel("Previsões")
plt.tight_layout()

DataManager.save_plot(fig=None, filename="regressao_linear_exportacoes", show=True)

#Salvando Resultados
df_resultados = pd.DataFrame({
    'Real': y_test,
    'Previsto':y_pred
})

DataManager.save_files_clean(df,'resultados_regressão_semana04_dia10',path=None)