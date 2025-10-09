"""Dia 06: Padronização e Operações com Strings

Aprender a padronizar textos, corrigir inconsistências e normalizar nomes,
algo essencial em bases de dados reais.

1️⃣ Motivação:
Muitos datasets têm diferenças sutis como:
"Soja " (com espaço no fim)
"algodão" vs "Algodao"
"Milho" vs "milho"

Esses detalhes quebram agrupamentos e análises.

2️⃣ Técnicas que você vai aplicar
Ação	Método Pandas	Exemplo
Remover espaços extras	.str.strip()	df['Commodity'] = df['Commodity'].str.strip()
Colocar tudo em maiúsculas ou minúsculas	.str.upper() / .str.lower()	df['Commodity'] = df['Commodity'].str.upper()
Substituir acentuação	unidecode (lib externa)	Algodão → Algodao
Substituir palavras específicas	.replace()	df['Commodity'].replace({'Algodão': 'Algodao'})
3️⃣ Etapas sugeridas
Carregar o arquivo que você salvou no Dia 05.
Detectar inconsistências na coluna COMMODITY.
Normalizar (letras maiúsculas, sem acentos, sem espaços).
Garantir que não há duplicatas (drop_duplicates()).
Salvar o dataset padronizado em data/limpos/semana02_dia06.csv."""

import pandas as pd
import os

file = r'C:\Users\User\PycharmProjects\PythonProject\data\producao_mes_expandido_20251006.csv'
df = pd.read_csv(file)
df.sort_values(by=['Commodity'], ascending=True)
df['Commodity'] = df['Commodity'].str.strip()

# [nan 'Trigo' 'milho' 'Algodao' 'Açucar' 'Minerio de Ferro' 'Cacau' 'trigo' 'soja' 'Algodão' 'Café' 'minério de ferro' 'Açúcar' 'Soja' 'Milho']
df['Commodity'] = df['Commodity'].str.upper()
df['Commodity'] = df['Commodity'].replace(
    {'ALGODÃO': 'ALGODAO', 'AÇÚCAR': 'AÇUCAR', 'CAFÉ': 'CAFE', 'MINÉRIO DE FERRO': 'MINERIO DE FERRO'})
df.drop_duplicates()
df_standard = df.copy()
df_standard.sort_values(by=['Mes'], ascending=True)

df_standard.to_csv('C:\\Users\\User\\PycharmProjects\\PythonProject\\data\\limpos\\producao_mes_arrumado.csv')
print('Arquivo atualizado e salvo')


"""df_ordenado = df.copy()
df_ordenado = df.sort_values(by=['Mes','Commodity'], ascending=True)
print(df_ordenado)
print(df_ordenado['Commodity'].unique())
agrupar = df_ordenado.groupby('Commodity')
print(agrupar.max())

print(df_ordenado.iloc[1])
print(df_ordenado.query('Producao > 300000'))"""
