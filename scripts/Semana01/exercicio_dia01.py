"""
Exercício 1 - Exportação de Dados em PDF
Descrição:
    Script educacional que demonstra o uso da classe ReportBuilder
    para exportar uma série de exportações brasileiras em formato PDF.
"""

import pandas as pd
from ClassesApoio import Format, ReportBuilder

# Série base simulando exportações de commodities
exportBR = pd.Series(
    [20000, 25000, 12500, 50000],
    index=['Milho', 'Açúcar', 'Café', 'Soja'],
    name='Exportações_Brasileiras'
)

if __name__ == "__main__":
    print('📊 Resumo de exportações brasileiras deste mês:')
    print(Format.alinhar_series(exportBR))

    print('\nOs dois primeiros eventos exportados:')
    print(exportBR.head(2))

    print('\nÚltimo evento exportado:')
    print(exportBR.tail(1))

    # Inserindo uma nova exportação (exemplo de atualização)
    nova_export = pd.Series([25000], index=['Açúcar']) #adiciona mais uma serie/coluna
    exportBR.loc['Açúcar'] = 2500 #adiciona na série ou coluna existente
    exportBR = pd.concat([exportBR, nova_export])

    print('\n📈 Série atualizada:')
    print(Format.alinhar_series(exportBR))

    # Estatísticas básicas (reforço prático de pandas)
    print("\n=== Estatísticas gerais ===")
    print(f"Total exportado: {exportBR.sum():.2f} toneladas")
    print(f"Média por registro: {exportBR.mean():.2f} toneladas")
    print(f"Máximo exportado: {exportBR.max():.2f} toneladas")
    print(f"Mínimo exportado: {exportBR.min():.2f} toneladas")

    # 🔽 Exportando a tabela como PDF
    print("\nGerando relatório em PDF...")
    rb = ReportBuilder()
    file_path = rb.export_to_pdf(exportBR,filename='exportacoes-brasileiras')

    print(f"\n✅ Relatório salvo em:{file_path}")
