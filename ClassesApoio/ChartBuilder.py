from fileinput import filename

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from seaborn import axes_style
from DataManager import DataManager as dm


class PlotManager:
    """
    Classe genérica para criação e personalização de gráficos com Matplotlib e Seaborn.

    A classe PlotManager foi desenvolvida para centralizar a geração de gráficos
    comuns em análises exploratórias de dados (EDA). Suporta gráficos de caixa, barras,
    dispersão, calor e permite inserção opcional de rótulos de valores nos nós.

    Métodos principais:
    -------------------
    - boxplot(df, x, y, title=""):
        Cria um boxplot mostrando a distribuição de uma variável numérica por categoria.

    - heatmap(df, title=""):
        Cria um mapa de calor com a matriz de correlação entre variáveis numéricas.

    - scatterplot(df, x, y, hue=None, title=""):
        Cria um gráfico de dispersão com coloração por categoria.

    - barplot(df, x, y, hue=None, title="", annotate=False):
        Cria um gráfico de barras com opção de exibir valores nos nós.

    :param
    df: pandas.DataFrame
        Dataframe contendo os dados a serem visualizados
    x,y: str
        Colunas correspondentes aos eixos x e y
    hue: str, optional
        Coluna usada para diferenciar os gráficos
    title: str, optional
        Titulo exibido no topo do gráfico
    annotate: bool, optional
        If True adiciona os valores sobre as barras ou pontos

    Exemplo de uso:
    ______________
    >>> from matplotlib.pyplot import annotate    >>> pm = PlotManager()
    >>> pm.barplot(df, x="Mês",y='Produção', hue='Commodity',title= 'Produção Mensal', annotate=True)
"""

    def __init__(self, style='whitegrid'):
        sns.set_style(style)
        plt.rcParams.update({
            'figure.autolayout': True,
            'axes.titlesize': 14,
            'axes.labelsize': 12,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10
        })

    def boxplot(self, x, y, title=None, filename=None, salvar=None, show=None):
        plt.figure(figsize=(10, 6))
        ax = sns.boxplot(data=None, x=x, y=y)
        plt.title(title)
        plt.xticks(rotation=45)

        if salvar:
            dm.save_plot(fig=plt.gcf(), filename=filename, show=show)

        if show:
            plt.show()

        return ax
