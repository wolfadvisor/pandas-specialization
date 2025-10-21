import os
import matplotlib.pyplot as plt

import datetime

import pandas as pd


class DataManager:
    @staticmethod
    def save_files_clean(df, filename=None, path=None):
        if path is None:
            path = r'C:\Users\User\PycharmProjects\PythonProject\data\limpos'

        os.makedirs(path, exist_ok=True)

        hoje = datetime.date.today().strftime('%Y%m%d')
        if not filename:
            filename = input(f'Digite o nome do arquivo sem extensão ({hoje}_): ')

        file_path = os.path.join(path, f'{filename}_{hoje}.csv')

        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f'✅ Arquivo salvo com sucesso:\n{file_path}')
        return file_path

    @staticmethod
    def save_plot(fig=None, filename=None, path=None, show=False, format='png'):
        if path is None:
            path = r'C:\Users\User\PycharmProjects\PythonProject\reports'

        os.makedirs(path, exist_ok=True)
        hoje = datetime.date.today().strftime('%Y%m%d')

        if not filename:
            filename = input(f'Digite o nome do gráfico sem extensão ({hoje}_): ')

        file_path = os.path.join(path, f'{filename}_{hoje}.{format}')

        try:
            # Se nenhuma figura for passada, usa a atual
            if fig is None:
                fig = plt.gcf()

            # Salva a figura (sem limpar o buffer)
            fig.savefig(file_path, bbox_inches='tight', dpi=300)

            if show:
                plt.show()

            print(f'✅ Gráfico salvo com sucesso:\n{file_path}')
            return file_path

        except Exception as e:
            print(f'❌ Erro ao salvar o gráfico: {e}')
            return None


    def carregar_fase1(self):
        path = r'C:\Users\User\PycharmProjects\PythonProject\reports\semana04_dia10\fase1_comex_preparado_2025.csv'
        return  pd.read_csv(path)
