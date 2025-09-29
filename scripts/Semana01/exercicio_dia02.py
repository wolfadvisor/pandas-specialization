import os
import pandas as pd

from scripts.Semana01.exercicio_dia01 import exportBR
from scripts.Semana01.semana_01_dia02 import producaoBR

"""
Tarefas práticas

Adicionar mais uma commodity (ex: Algodão).
Testar operações como exportBR.mean() e producaoBR.max().
Salvar o DataFrame em um CSV dentro da pasta data/.
"""

# Adicionando um novo item à Series já existente
novaexport = pd.Series([30000], ['Algodao'], name='Exportações Brasileiras')
exportBR = pd.concat([exportBR, novaexport])

#Verificando diretorio
print("📂 Verificando diretório atual:", os.getcwd())
print("📄 Verificando se a pasta 'data' existe:", os.path.exists("data"))

# Criando o diretório (se não existir) e salvando em CSV
caminho_csv = "C:\\Users\\User\\PycharmProjects\\PythonProject\\data\\exportacoes.csv"
os.makedirs("C:\\Users\\User\\PycharmProjects\\PythonProject\\data", exist_ok=True)
exportBR.to_csv(caminho_csv, index=True)

#Depois de salvar

print(f"✅ Arquivo salvo em: {caminho_csv}")
print("Existe mesmo?", os.path.exists(caminho_csv))


# Estatísticas
print('-- Média Geral dos Commodities Exportados --')
print(f'A média {exportBR.mean():.2f} toneladas é referente ao mês passado.')

print('-- Commodity com maior quantidade produzida --')
print(f'A maior produção {producaoBR.max():.2f} toneladas, pertence ao commodity {producaoBR.idxmax()}')
