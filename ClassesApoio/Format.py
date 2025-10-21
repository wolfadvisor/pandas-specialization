import pandas as pd

import unicodedata


class Format:

    def remover_acentos(text):
        return ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )

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

    def alinhar_dataframe(df: pd.DataFrame) -> str:
        return df.to_string()
