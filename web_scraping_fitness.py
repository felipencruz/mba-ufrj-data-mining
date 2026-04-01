import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from urllib.robotparser import RobotFileParser

#### Configuração de Caminhos ####
PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))
PASTA_DADOS = os.path.join(PASTA_PROJETO, "dados")
os.makedirs(PASTA_DADOS, exist_ok=True)
ARQUIVO_CSV = os.path.join(PASTA_DADOS, "tendencias_mercado.csv")

#### Configuração do Site ####
URL_ALVO = "https://claudia.abril.com.br/moda/moda-fitness-verao-2026-tendencias/"
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

print("=" * 70)
print(">>> INICIANDO WEB SCRAPING ÉTICO (CONFORMIDADE ROBOTS.TXT)")
print("=" * 70)

#### VALIDAÇÃO DE ÉTICA ####
rp = RobotFileParser()
rp.set_url("https://claudia.abril.com.br/robots.txt")

try:
    print(f"[*] Consultando regras em: https://claudia.abril.com.br/robots.txt")
    rp.read()
    pode_acessar = rp.can_fetch(USER_AGENT, URL_ALVO)
except Exception as e:
    print(f"⚠️ Aviso: Não foi possível ler o robots.txt ({e}). Assumindo permissão padrão.")
    pode_acessar = True

#### EXECUÇÃO DO SCRAPING ####
if pode_acessar:
    try:
        headers = {'User-Agent': USER_AGENT}
        res = requests.get(URL_ALVO, headers=headers, timeout=15)
        res.raise_for_status()
        
        soup = BeautifulSoup(res.text, 'html.parser')
        
        #### Buscamos os títulos e destaques ####
        elementos = soup.find_all(['h2', 'h3', 'strong'])
        
        termos = []
        for e in elementos:
            texto = e.get_text().strip().lower()
            if texto and len(texto) > 3:  # Filtrar termos curtos ou vazios
                termos.append(texto)
        
        if termos:
            df = pd.DataFrame(termos, columns=['termo_tendencia']).drop_duplicates()
            df.to_csv(ARQUIVO_CSV, index=False, sep=';', encoding='utf-8-sig')
            print(f"✅ SUCESSO: {len(df)} termos reais extraídos.")
            print(f"└─ Arquivo salvo: {ARQUIVO_CSV}")
        else:
            print("⚠️ Conexão realizada, mas nenhum termo foi encontrado na estrutura.")

    except Exception as e:
        print(f"❌ Erro técnico na coleta: {e}")
else:
    print("❌ ACESSO NEGADO: As regras do robots.txt proíbem o scraping nesta URL.")

print("=" * 70)