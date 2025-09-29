"""
Operações com Series e introdução a DataFrames
Objetivos do dia:

Criar duas Series de commodities (produção e exportação).

Fazer operações matemáticas entre elas.

Criar o primeiro DataFrame com pandas.

Explorar métodos como .shape, .info() e .describe().

"""

import pandas as pd
from ClassesApoio.Format import alinhar_series
from scripts.Semana01.exercicio_dia01 import exportBR


# Criando operações matemáticas para obtenção de saldo
def saldoNacional(producaoBr, exportBR):
    saldoBr = producaoBr - exportBR
    return saldoBr


# criando series de produção por materia prima

producaoBR = pd.Series([60000, 45000, 30000, 70000],
                       index=['Milho', 'Açucar', 'Café', 'Soja'],
                       name='Producao_Brasileira')
exportBR

# 🔹 1. Operações matemáticas entre Series
saldo = producaoBR - exportBR
print("\nSaldo disponível para mercado interno (Produção - Exportações):")
print(alinhar_series(saldo))

#Criando um DATAFRAME

df = pd.DataFrame({"Produção": producaoBR,
                   "Exportações": exportBR,
                   'Saldo Interno': saldo})

if __name__ == "__main__":
    print("--- Produção Brasileira em Toneladas ---\n")
    print(alinhar_series(producaoBR))
    print()

    print("--- Exportações Brasileira em Toneladas ---\n")
    print(alinhar_series(exportBR))
    print()

    #Saldo Produção Brasileira usando uma função
    print(f'Saldo da produção Brasileira em Toneladas:'
          f'\n{saldoNacional(producaoBR, exportBR)}')

    # Usando DATAFRAME
    print('\nDataFrame de Commodities.')
    print(df)

    #explorando o DATAFRAME com .info() e .describe()
    print("\nInformação do Dataframe - df")
    print(df.info())

    print("\nResumo estatístico do Dataframe - df")
    print(df.describe())