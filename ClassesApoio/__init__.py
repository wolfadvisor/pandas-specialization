"""
Pacote: ClassesApoio
Descrição: Este pacote contém classes de apoio utilizadas nos módulos de análise
de dados do projeto de commodities. O arquivo __init__.py facilita o acesso
aos principais componentes do pacote.
"""

#Importações relativas para os modulos
from .DataManager import DataManager
from .PlotBuilder import PlotManager
from .Format import Format
from .ReportBuilder import ReportBuilder

#Define o que será expoto ao importar o pacote

__all__ = ['DataManager','PlotManager','Format','ReportBuilder','Dashboard']
