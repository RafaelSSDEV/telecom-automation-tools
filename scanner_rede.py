import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor

def verificar_ip(ip_alvo):
    
   #Verifica SO para utilizar a flag correta
    flag_contagem = '-n' if platform.system().lower() == 'windows' else '-c'
    comando = ['ping', flag_contagem, '1', ip_alvo]

    try:
        
        # ping sem saida STDOUT/STDER e com timeout para não ficar preso em ip's que não respondem
        resposta = subprocess.run(comando, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=0.5)
        if resposta.returncode == 0:
            return f" {ip_alvo} está ONLINE"
    except subprocess.TimeoutExpired:
        return None 
    except Exception as e:
        return None

def main():
    print('--- INICIANDO VARREDURA ---')
    # .strip() remove espaços 
    rede_base = input('Digite a rede (ex: 192.168.0): ').strip()
    
    try:
        r1 = int(input('Inicio do range (ex: 1): '))
        r2 = int(input('Final do range (ex: 50): '))
    except ValueError:
        print("O range precisa ser um numero inteiro!")
        return

    print(f" Varrendo de {rede_base}.{r1} até {rede_base}.{r2}...")
    
    # Montando a lista de IPs completos
    lista_ips = []
    # O range no python para antes do ultimo numero por isso o r2 + 1 pra incluir ele
    for i in range(r1, r2 + 1):
        ip_completo = f"{rede_base}.{i}" 
        lista_ips.append(ip_completo)

    # ThreadPoolExecutor para executar em paralelo (concorrente).
    # Sequencial levaria ~120s; Com threads cai para ~5s.  
    with ThreadPoolExecutor(max_workers=50) as executor:
        resultados = executor.map(verificar_ip, lista_ips)

        for res in resultados:
            if res:
                print(res)

if __name__ == '__main__':
    main()