#### PIPELINE DE DATA MINING - ANÁLISE DE VENDAS DE MODA FITNESS NO BRASIL ####

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg') # Para salvar os gráficos sem abrir janelas
import matplotlib.pyplot as plt
import seaborn as sns
import os

#### Configuração de caminhos e pastas para dados e imagens ####
PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))
PASTA_DADOS = os.path.join(PASTA_PROJETO, "dados")
PASTA_IMAGENS = os.path.join(PASTA_PROJETO, "imagens")
os.makedirs(PASTA_IMAGENS, exist_ok=True)

print("=" * 70)
print("  PASSO 1: CARREGAMENTO E LIMPEZA (DATA PREPARATION)")
print("=" * 70)

#### Carregando os dados de vendas e clientes ####
df_vendas = pd.read_csv(os.path.join(PASTA_DADOS, "fVendas.csv"), sep=';')
df_clientes = pd.read_csv(os.path.join(PASTA_DADOS, "dClientes.csv"), sep=';')

#### REMOVENDO DUPLICATAS ####
total_antes = len(df_vendas)
df_vendas = df_vendas.drop_duplicates()
print(f"  ├─ Removidas {total_antes - len(df_vendas)} linhas duplicadas.")

#### TRATANDO NULOS (Imputação de Preços) ####
##### Se o preço está nulo, vamos preencher com a média da categoria ####
nulos_antes = df_vendas['preco_unitario'].isna().sum()
df_vendas['preco_unitario'] = df_vendas['preco_unitario'].fillna(df_vendas['preco_unitario'].median())
print(f"  └─ Tratados {nulos_antes} valores de preço ausentes.")

print("\n" + "=" * 70)
print("  PASSO 2: ANÁLISE EXPLORATÓRIA (DATA UNDERSTANDING)")
print("=" * 70)

#### Gráfico de Vendas por Categoria ####
plt.figure(figsize=(10, 6))
top_categorias = df_vendas.groupby('sku')['quantidade'].sum().sort_values(ascending=False).head(10)
sns.barplot(x=top_categorias.values, y=top_categorias.index, palette='viridis')
plt.title('Top 10 SKUs mais Vendidos - Moda Fitness BR')
plt.xlabel('Total de Unidades Vendidas')
plt.ylabel('SKU')
plt.tight_layout()

#### Salvando o gráfico ####
caminho_grafico1 = os.path.join(PASTA_IMAGENS, "01_top_vendas.png")
plt.savefig(caminho_grafico1)
plt.close()
print(f"  ├─ Gráfico de Top Vendas salvo em: {PASTA_IMAGENS}")

#### Faturamento por Canal de Venda ####
plt.figure(figsize=(8, 8))
faturamento_canal = df_vendas.groupby('canal_venda')['valor_total'].sum()
plt.pie(faturamento_canal, labels=faturamento_canal.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
plt.title('Distribuição de Faturamento por Canal')

#### Salvando o gráfico ####
caminho_grafico2 = os.path.join(PASTA_IMAGENS, "02_faturamento_canal.png")
plt.savefig(caminho_grafico2)
plt.close()
print(f"  └─ Gráfico de Canais salvo em: {PASTA_IMAGENS}")