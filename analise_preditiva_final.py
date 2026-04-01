import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import os

#### Configuração de Caminhos ####
PASTA_DADOS = os.path.join(os.path.dirname(__file__), "dados")
PASTA_IMAGENS = os.path.join(os.path.dirname(__file__), "imagens")

#### Carregamento e Integração de Dados ####
df_vendas = pd.read_csv(os.path.join(PASTA_DADOS, "fVendas.csv"), sep=';')
df_trends = pd.read_csv(os.path.join(PASTA_DADOS, "tendencias_limpas.csv"), sep=';')

print("=" * 70)
print("  PASSO 7: MODELO PREDITIVO - REGRESSÃO LINEAR MÚLTIPLA")
print("=" * 70)

#### Cálculo do Fator de Impacto ####
#### Identificamos a força das tendências reais extraídas no scraping ####
termos_chave = ['short', 'legging', 'top', 'macacão', 'flare', 'capri', 'tecnológico']
hits = df_trends['termo_tendencia'].str.contains('|'.join(termos_chave)).sum()

#### Cada termo relevante do scraping adiciona um boost de 4% na projeção ####
fator_mercado = min(1 + (hits * 0.04), 1.25)
print(f"  ├─ Insights de Moda detectados: {hits}")
print(f"  ├─ Fator de Impulso para 2026: {fator_mercado:.2f}x")

#### Preparação da Série Temporal ####
df_vendas['data_venda'] = pd.to_datetime(df_vendas['data_venda'])
df_mensal = df_vendas.set_index('data_venda').resample('ME')['valor_total'].sum().reset_index()
df_mensal['mes_num'] = range(len(df_mensal))

#### Treinamento do Modelo de Regressão ####
X = df_mensal[['mes_num']]
y = df_mensal['valor_total']
modelo = LinearRegression().fit(X, y)

#### Predição Ajustada para 2026 ####
meses_futuros = np.array(range(len(df_mensal), len(df_mensal) + 6)).reshape(-1, 1)
pred_simples = modelo.predict(meses_futuros)
pred_com_tendencia = pred_simples * fator_mercado

#### Geração do Gráfico ####
plt.figure(figsize=(12, 6))
plt.plot(df_mensal['data_venda'], df_mensal['valor_total'], label='Faturamento Real (Histórico)', color='#1f77b4', lw=2)

#### Datas para a projeção ####
datas_futuras = pd.date_range(df_mensal['data_venda'].max(), periods=7, freq='ME')[1:]

plt.plot(datas_futuras, pred_com_tendencia, 'r--', label='Projeção 2026 (Ajustada p/ Scraping)', lw=2)
plt.fill_between(datas_futuras, pred_simples, pred_com_tendencia, color='red', alpha=0.1, label='Margem de Otimismo (Tendências Externas)')

plt.title('Data Mining: Predição de Vendas Moda Fitness 2026')
plt.ylabel('Faturamento (R$)')
plt.xlabel('Linha do Tempo')
plt.legend()
plt.grid(True, alpha=0.2)

caminho_final = os.path.join(PASTA_IMAGENS, "05_predicao_final_tendencias.png")
plt.savefig(caminho_final)
plt.close()

print(f"  └─ Sucesso! Gráfico final gerado em: {caminho_final}")
print("=" * 70)