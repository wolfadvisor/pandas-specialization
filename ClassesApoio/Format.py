import pandas as pd
import matplotlib as plt
import seaborn as sns


def alinhar_series(series: pd.Series) -> pd.Series:
    # Tamanhos máximos
    max_index = max(len(str(idx)) for idx in series.index)
    max_val = max(len(str(val)) for val in series.values)

    # Nova Series formatada
    resultado = pd.Series(
        [f"{str(idx).ljust(max_index)}   {str(val).ljust(max_val)}"
         for idx, val in series.items()],
        name=series.name
    )


def alinhar_dataframe(df: pd.DataFrame):
    return df.to_string()


def dashboar_style(
        tema='whitegrid',
        context='talk',
        paleta='viridis',
        fonte='sans-serif',
        fonte_tamanho=12,
        fonte_titulo=16,
        grid=True
):
    """
        Aplica um estilo consistente para todos os gráficos Seaborn e Matplotlib.

        Parâmetros:
        - tema: 'darkgrid', 'whitegrid', 'dark', 'white', 'ticks'
        - contexto: 'paper', 'notebook', 'talk', 'poster'
        - paleta: qualquer paleta Seaborn ('deep', 'muted', 'viridis', 'coolwarm', etc.)
        - fonte: tipo de fonte global ('sans-serif', 'serif', 'monospace')
        - fonte_tamanho: tamanho base dos textos
        - fonte_titulo: tamanho dos títulos dos gráficos
        - grid: mostrar linhas de grade (True/False)
        """

    # aplicar estilo e contexto
    sns.set_theme(style=tema, context=context, palette=paleta)

    # Configurações globais do matplot
    plt.rcParams.update({
        "font.family": fonte,
        "font.size": fonte_tamanho,
        "axes.titlesize": fonte_titulo,
        "axes.labelsize": fonte_tamanho,
        "axes.edgecolor": "#333333",
        "axes.linewidth": 1,
        "axes.labelcolor": "#222222",
        "xtick.color": "#444444",
        "ytick.color": "#444444",
        "grid.alpha": 0.3,
        "grid.linestyle": "--",
        "grid.color": "#CCCCCC",
        "figure.facecolor": "#FAFAFA",
        "axes.facecolor": "#FFFFFF" if tema in ["whitegrid", "white"] else "#1E1E1E",
        "legend.frameon": False,
        "legend.fontsize": fonte_tamanho - 1,
        "legend.title_fontsize": fonte_tamanho,
    })
    #mostrar ou ocultar grid
    if not grid:
        sns.set_style('white')
        plt.grid(False)

