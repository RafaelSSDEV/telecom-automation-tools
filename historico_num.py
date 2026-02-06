import clickhouse_connect
import pandas as pd
import configparser
import os
from rich.console import Console
from rich.table import Table

# Configurações Visuais do Pandas e Rich
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
console = Console()

def get_client():
    """Gerencia conexao com clickhouse."""
    if not os.path.exists('config.ini'):
        console.print("[bold yellow]Aviso:[/bold yellow] config.ini não encontrado.")
        return None
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    try:
        return clickhouse_connect.get_client(
            host=config['database']['host'],
            port=int(config['database']['port']),
            username=config['database']['user'],
            password=config['database']['password'],
            secure=config.getboolean('database', 'secure')
        )
    except Exception as e:
        console.print(f"[bold red]Erro de conexão:[/bold red] {e}")
        return None

def analisar_performance(numero, dias):
    client = get_client()
    if not client: return

    console.print(f"\n[bold cyan] Iniciando análise para: {numero} ({dias} dias)[/bold cyan]")

    query = """
    SELECT 
        start_stamp,
        dest_nap AS NAP,
        hangup_cause AS SIP,
        billsec,
        duration
    FROM bilhetes.khomp_cdr
    WHERE 
        dest_addr LIKE %(num)s
        AND start_stamp >= now() - INTERVAL %(dias)s DAY
    ORDER BY start_stamp DESC
    LIMIT 1000
    """
    
    try:
        df = client.query_df(query, parameters={'num': f"%{numero}%", 'dias': dias})
        
        if df.empty:
            console.print("[red] Nenhum registro encontrado.[/red]")
            return
        
        #  Resumo de codigos SIP
        resumo_sip = df['SIP'].value_counts().reset_index()
        resumo_sip.columns = ['SIP CODE', 'QTD']
        
        # Cria tabela visual com Rich
        table = Table(title=" Top Ocorrências (SIP)", style="magenta")
        table.add_column("SIP Code", justify="center")
        table.add_column("Quantidade", justify="center")
        
        for index, row in resumo_sip.head().iterrows():
            cor = "red" if row['SIP CODE'] in [480, 503, 408] else "green"
            table.add_row(f"[{cor}]{row['SIP CODE']}[/{cor}]", str(row['QTD']))
            
        console.print(table)

        # Alerta codigos 
        erros_480 = df[df['SIP'] == 480]
        if not erros_480.empty:
            console.print(f"\n[bold red blink]  ALERTA: {len(erros_480)} falhas de NAP (SIP 480) detectadas![/bold red blink]")
            console.print("NAPs impactadas:")
            console.print(erros_480['NAP'].value_counts().head().to_string())

    except Exception as e:
        console.print(f"[bold red]Erro durante a query:[/bold red] {e}")

if __name__ == "__main__":
    console.print("[bold green]--- CDR Analyzer Tool v1.2 ---[/bold green]")
    # Exemplo de chamada (comentado para evitar execução sem input)
    # numero = console.input("Digite o número: ")
    # len(numero) > 8 (Proteção para consulta com LIKE no banco )
    # analisar_performance(numero, 7)