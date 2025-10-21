"""
Módulo: ReportBuilder
Função: Exportar DataFrames ou Séries em formato PDF.
Autor: Carlos Ribeiro
Data: 2025-10-19
"""

import os
import datetime
import pandas as pd
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


class ReportBuilder:
    """
    Classe responsável por exportar dados em formato PDF.
    """

    def __init__(self):
        print('✅ ReportBuilder inicializado com sucesso.')

    def export_to_pdf(self, df, path=None, filename=None):
        """
        Exporta um DataFrame ou uma Série para um arquivo PDF.

        Parâmetros
        ----------
        df: pandas.DataFrame | pandas.Series
            Dados a serem exportados.
        path: str
            Caminho onde o PDF será salvo (padrão: diretório de relatórios).
        filename: str
            Nome do arquivo (sem extensão). Se não informado, será solicitado ao usuário.
        : return str
            Caminho completo do arquivo PDF gerado.
        """

        # Converte Series para DataFrame, se necessário
        if isinstance(df, pd.Series):
            series_name = df.name or 'Valor'
            df = df.reset_index()
            df.columns = [df.columns[0], series_name]

        # Define caminho padrão se não informado
        if path is None:
            path = r'C:\Users\User\PycharmProjects\PythonProject\reports\PdfFiles'

        os.makedirs(path, exist_ok=True)

        # Define nome de arquivo com data
        hoje = datetime.date.today().strftime('%Y%m%d')
        if not filename:
            filename = input(f'Digite o nome do arquivo sem extensão ({hoje}_): ')

        file_path = os.path.join(path, f'{filename}_{hoje}.pdf')

        # Converte o DataFrame para lista (necessário para o ReportLab)
        data = [df.columns.tolist()] + df.values.tolist()

        # Criação do PDF com tabela
        pdf = SimpleDocTemplate(file_path)
        table = Table(data)

        # Aplicando estilos de tabela
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
        ]))

        # Gera o arquivo final
        pdf.build([table])
        print(f'📄 Arquivo PDF salvo com sucesso em: {file_path}')

        return file_path
