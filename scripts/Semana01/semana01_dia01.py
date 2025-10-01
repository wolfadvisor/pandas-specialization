"""
    - Criar series de Pandas
    - Usar metodos basicos .head() e .tail()
    - Entender com indice funciona em pandas.

"""
import pandas as pd

from ClassesApoio.Format import alinhar_series

#Criando a primeira série.

ingredientes = pd.Series(
    ["4 xicaras", '1 xicara', '2 unidades', '1 lata'],
    index=['Farinha','leite', 'Ovos', 'Ervilha'],
    name= 'Jantar'
)
# Mostrando a série completa
print('----- Ingredientes -----')
print(alinhar_series(ingredientes))

#Mostrar as primeiras linhas
print('----- primeiros elementos usando head() -----')
print(alinhar_series(ingredientes.head(2))) #somente dois elementos

#Mostrar as primeiras linhas
print('----- Ultimos elementos usando tail() -----')
print(alinhar_series(ingredientes.tail(2))) #somente dois elementos

#acessando pelo indicie
print('----- Acessando pelo index -----')
print(ingredientes['leite']) #Usando o index ele retorna a quantidade

#Mostrar os tipos de dados
print('----- tipos de dados dtype -----')
print(ingredientes.dtype) #somente dois elementos


