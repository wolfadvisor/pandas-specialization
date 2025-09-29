"""
Exercícios práticos para você fazer:

Troque os ingredientes por uma lista de commodities (Milho, Soja, Açúcar, Café) com quantidades em toneladas.

Teste o .head(3) e .tail(1).

Crie uma nova Series chamada "Exportações" com dados fictícios de exportações em toneladas.

"""


import pandas as pd
from ClassesApoio.Format import alinhar_series

exportBR = pd.Series(
    [20000, 25000, 12500, 50000],
    index=['Milho', 'Açucar', 'Café', 'Soja'],
    name='Exportacoes_Brasileiras'
)

if __name__ == "__main__":
    print('Resumos de exportações Brasileiras desse mês:')
    print(alinhar_series(exportBR))
    print(f'Os dois primeiros eventos que foram exportados pelo Brasil: \n{exportBR.head(2)}')
    print(f'O último evento que foi exportado pelo Brasil: \n{exportBR.tail(1)}')

    # inserindo uma nova exportação
    novaexport = pd.Series([25000], index=['Açucar'])
    # Usando concat para adicionar na série já feita
    exportBR = pd.concat([exportBR, novaexport])

    # Verificando a nova exportação
    print('Resumos de exportações Brasileiras desse mês atualizada:')
    print(alinhar_series(exportBR))
    alinhar_series(exportBR)

    # Estatísticas básicas (extra para reforçar pandas)
    print("\n=== Estatísticas gerais ===")
    print(f"Total exportado: {exportBR.sum():.2f} toneladas")
    print(f"Média por registro: {exportBR.mean():.2f} toneladas")
    print(f"Máximo exportado em um registro: {exportBR.max():.2f} toneladas")
    print(f"Mínimo exportado em um registro: {exportBR.min():.2f} toneladas")


