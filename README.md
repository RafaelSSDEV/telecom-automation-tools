# Telecom Automation Tools 

Ferramentas de automação para operações de Telecomunicações e SRE, desenvolvidas para agilizar diagnósticos e monitoramento.

##  Ferramentas Incluídas

### 1. Network Scanner (`scanner_rede.py`)
Script de varredura de rede local utilizando **Threads** para alta performance.
- Identifica hosts ativos na sub-rede.
- Ajusta automaticamente os parâmetros de ping para Windows/Linux.
- Utiliza `ThreadPoolExecutor` para paralelismo.

### 2. CDR Analyzer (`historico_num.py`)
Ferramenta de análise de logs de chamadas (CDR) conectada ao **ClickHouse**.
- Gera relatórios visuais de falhas SIP (480, 503).
- Identifica rotas com problemas de completamento.
- Utiliza **Pandas** para manipulação de dados e **Rich** para visualização no terminal.

## 🛠️ Stack Tecnológica
- Python 3.12
- Pandas & ClickHouse Connect
- Rich (CLI Dashboards)
- Threading & Subprocess

---
*Projeto pessoal para estudos de automação.*