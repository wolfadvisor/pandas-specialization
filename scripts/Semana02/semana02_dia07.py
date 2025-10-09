"""

Detecção de Outliers e Normalização
Aprender a identificar valores fora do padrão (outliers) e normalizar
os dados numéricos para padronizar a escala entre variáveis.
Essas técnicas são fundamentais para análises comparativas,
correlações e modelos estatísticos.

"""

# Tecnicas para detectar Outliers
# Desvio padrão um valor que esta acima da média, caso |z| >3

import pandas as pd
import numpy as np

# vou carregar o arquivo padronizado
file = r'C:\\Users\\User\\PycharmProjects\\PythonProject\\data\\limpos\\producao_mes_arrumado.csv'

df = pd.read_csv(file)

# Calcular a média da coluna produção e depois o Desvio Padrão
media = df['Producao'].mean()
desvio = df['Producao'].std()
print(f'A média de Produção é {media:.2f} e o Desvio Padrão é {desvio:.2f}.')

# Criando a coluna Z-Score
df['Z_PRODUCAO'] = (df['Producao'] - media) / desvio
# Zscore é calculo que usaremos para definir os outliers
df['Outlier_Z'] = abs(df['Z_PRODUCAO']) > 3

# agora usaremos uma outra tecnica de detecção
# Metodo IQR

Q1 = df['Producao'].quantile(0.25)

Q3 = df['Producao'].quantile(0.75)

IQR = Q3 - Q1

lim_inf = Q1 - 1.5 * IQR
lim_sup = Q3 + 1.5 * IQR

# Criando a coluna Outliers
df['Outliers_IQR'] = (df['Producao'] < lim_inf) | (df['Producao'] > lim_sup)
z_Score = df[df['Outlier_Z']]
print(f'Outlier pelo Z Score {z_Score}\n')
outliers_IQR = df[df['Outliers_IQR']]
print(f'\nOutlier pelo IQR {outliers_IQR}')



