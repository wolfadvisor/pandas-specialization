import pandas as pd


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
    return resultado



