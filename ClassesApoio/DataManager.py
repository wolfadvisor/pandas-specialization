import os
import pandas as pd
import datetime


class DataManager:
    @staticmethod
    def save_files_clean(df, filename, path):

        if path is None:
            path =r'C:\\Users\\User\\PycharmProjects\\PythonProject\\data\\limpos'

        os.makedirs(path,exist_ok=True)

        hoje = datetime.date.today().strftime('%Y%m%d')
        if filename is None:
            filename = input(f'Digite o nome do arquivo sem extensão: {hoje}_')

        file_path = os.path.join(path,f'{filename}_{hoje}.csv')

        df.to_csv(file_path,index=False,encoding='utf-8-sig')
        print(f'Arquivo salvo com sucesso: \n{file_path}\n{path}')
        return file_path
