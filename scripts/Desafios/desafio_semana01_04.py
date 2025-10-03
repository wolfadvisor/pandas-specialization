import os.path


import pandas as pd
""" file= r'C:\\Users\\User\\PycharmProjects\\PythonProject\\data\\commodities_mes.csv'
df =pd.read_csv(file)
nova_linha = pd.DataFrame(
    [{'Mes': 'Mai', 'Commodity': 'Milho', 'Producao': 65000, 'Exportacoes': 25000},
    {'Mes': 'Mai', 'Commodity': 'Soja', 'Producao': 40000, 'Exportacoes': 30000},
    {'Mes': 'Mai', 'Commodity': 'Algodão', 'Producao': 95000, 'Exportacoes': 52000},
    {'Mes': 'Jun', 'Commodity': 'Milho', 'Producao': 67000, 'Exportacoes': 28000},
    {'Mes': 'Jun', 'Commodity': 'Soja', 'Producao': 42000, 'Exportacoes': 31000},
    {'Mes': 'Jun', 'Commodity': 'Algodão', 'Producao': 97000, 'Exportacoes': 55000}])

df = pd.concat([df,nova_linha],ignore_index=True)
print('Arquivo Atualizado com sucesso.')
print(df.tail(9))
mapa_trimestre = {'Jan':'T1', 'Fev':'T1','Mar': 'T1',
                  'Abr': 'T2', 'Mai': 'T2','Jun': 'T2'}
df['Trimestre'] = df['Mes'].map(mapa_trimestre)
#Limpar as colunas unnamed
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
print(df.head())
df.to_csv(file)
print(f"Arquivo atualizado {file}")
print(df)"""

#Calcular a soma trimestral de expo por commodity
df = pd.read_csv(r'C:\Users\User\PycharmProjects\PythonProject\data\commodities_mes.csv')

calcTrimestre = df.groupby(['Trimestre', 'Commodity'])['Exportacoes'].sum().reset_index()
calcT1 = df.query("Trimestre == 'T1'").groupby('Commodity')['Exportacoes'].sum().reset_index()
calcT2 = df.query("Trimestre == 'T2'").groupby('Commodity')['Exportacoes'].sum().reset_index()
print(calcTrimestre)
print("\nExportações primeiro trimestre\n",calcT1)
print("\nExportções segundo trimestre\n",calcT2)
calcT1 = df.query("Trimestre == 'T1'").groupby('Commodity')['Exportacoes'].idxmax().reset_index()
calcT2 = df.query("Trimestre == 'T2'").groupby('Commodity')['Exportacoes'].idxmax().reset_index()
print("\nExportações primeiro trimestre com maior valor\n",calcT1)
print("\nExportções segundo trimestre com o maior valor\n",calcT2)

# Soma trimestral de exportações por commodity
soma_trimestre = df.groupby(['Trimestre', 'Commodity'])['Exportacoes'].sum().reset_index()
print("Soma trimestral:\n", soma_trimestre)

mais_T1 = soma_trimestre[soma_trimestre['Trimestre'] == 'T1'].sort_values(by='Exportacoes', ascending=False).head(1)
print("\nMais exportada no T1:\n", mais_T1)

# Commodity mais exportada no T2
mais_T2 = soma_trimestre[soma_trimestre['Trimestre'] == 'T2'].sort_values(by='Exportacoes', ascending=False).head(1)
print("\nMais exportada no T2:\n", mais_T2)

# Crescimento entre T1 e T2
crescimento = soma_trimestre.pivot(index='Commodity', columns='Trimestre', values='Exportacoes').fillna(0)
crescimento['Crescimento'] = crescimento['T2'] - crescimento['T1']
maior_crescimento = crescimento.sort_values(by='Crescimento', ascending=False).head(1)
print("\nMaior crescimento de T1 para T2:\n", maior_crescimento)

#salvar resultados
caminho = r'C:\\Users\\User\\PycharmProjects\\PythonProject\\data'

soma_trimestre.to_csv(os.path.join(caminho, 'soma_trimestre.csv'), index=False)
soma_trimestre.to_json(os.path.join(caminho, 'soma_trimestre.json'), orient='records', indent=4)
soma_trimestre.to_excel(os.path.join(caminho, 'soma_trimestre.xlsx'), index=False)

