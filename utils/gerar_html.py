
def gerar_html_obra(obra):
    return f"""
    <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: 'DejaVu Sans', sans-serif; padding: 30px; }}
                h1 {{ color: navy; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                td, th {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
            </style>
        </head>
        <body>
            <h1>Relatório da Obra</h1>
            <table>
                <tr><th>ID</th><td>{obra.id}</td></tr>
                <tr><th>Interessado</th><td>{obra.Interessado or ''}</td></tr>
                <tr><th>Empreendimento</th><td>{obra.Empreendimento or ''}</td></tr>
                <tr><th>Objeto do Contrato</th><td>{obra.ObjetoContrato or ''}</td></tr>
                <tr><th>Valor da Obra</th><td>R$ {obra.ValorObra:,.2f}</td></tr>
                <tr><th>Data Início Prevista</th><td>{obra.DataInicioPrevista}</td></tr>
                <tr><th>Data Fim Prevista</th><td>{obra.DataFimPrevista}</td></tr>
                <tr><th>Endereço</th><td>{obra.Logradouro}, {obra.Numero} - {obra.Bairro}, {obra.Cidade} - {obra.Estado}</td></tr>
                <tr><th>Latitude / Longitude</th><td>{obra.Latitude} / {obra.Longitude}</td></tr>
                <tr><th>Status</th><td>{obra.Status}</td></tr>
            </table>
        </body>
    </html>
    """
