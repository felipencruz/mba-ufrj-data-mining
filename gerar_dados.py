#### GERAR DADOS HISTÓRICOS ####
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

#### CONFIGURAÇÃO DE PASTAS ####
PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))
PASTA_DADOS = os.path.join(PASTA_PROJETO, "dados")
os.makedirs(PASTA_DADOS, exist_ok=True)

print("=" * 70)
print("  MODA FITNESS BR - AMBIENTE CONFIGURADO")
print("=" * 70)
print(f"Pasta dos dados: {PASTA_DADOS}")

#### Seed para que os resultados sejam iguais toda vez que rodar ####
np.random.seed(42)
random.seed(42)

print("\n[1/4] Gerando Dimensões (Produtos e Clientes)...")

#### PRODUTOS (Categorias e Preços Médios) ####
categorias = {
    'Legging': 89.90,
    'Top': 45.00,
    'Shorts': 59.90,
    'Camiseta Dry-Fit': 69.90,
    'Agasalho': 189.00,
    'Acessórios': 25.00
}

produtos_lista = []
for cat, preco in categorias.items():
    for i in range(1, 6):  # 5 variações por categoria
        produtos_lista.append({
            'sku': f"{cat[:3].upper()}-{100+i}",
            'produto': f"{cat} Modelo {i}",
            'categoria': cat,
            'preco_base': preco
        })
df_produtos = pd.DataFrame(produtos_lista)

#### CLIENTES (Gerando 5.000 clientes únicos) ####
n_clientes = 15000
clientes_data = {
    'cliente_id': range(1, n_clientes + 1),
    'idade': np.random.randint(18, 65, n_clientes),
    'genero': np.random.choice(['F', 'M', 'Outro', None], n_clientes, p=[0.65, 0.25, 0.05, 0.05]),
    'uf': np.random.choice(['RJ', 'SP', 'MG', 'ES', 'PR', 'SC', 'RS'], n_clientes),
    'data_cadastro': [datetime(2021, 1, 1) + timedelta(days=np.random.randint(0, 1800)) for _ in range(n_clientes)]
}
df_clientes = pd.DataFrame(clientes_data)

print(f"  ├─ {len(df_produtos)} SKUs de produtos criados.")
print(f"  └─ {len(df_clientes)} clientes únicos simulados.")

#### GERANDO TRANSACOES ####
print("\n[2/4] Gerando Transações (~250.000 registros)...")

n_vendas = 250000

# Datas aleatórias nos últimos 5 anos
data_inicial = datetime.now() - timedelta(days=5*365)
datas_vendas = [data_inicial + timedelta(days=np.random.randint(0, 5*365)) for _ in range(n_vendas)]

# Criando a estrutura principal de vendas
vendas_data = {
    'venda_id': range(1, n_vendas + 1),
    'data_venda': datas_vendas,
    'cliente_id': np.random.choice(df_clientes['cliente_id'], n_vendas),
    'sku': np.random.choice(df_produtos['sku'], n_vendas),
    'quantidade': np.random.randint(1, 5, n_vendas),
    'canal_venda': np.random.choice(['Loja Física', 'E-commerce', 'Instagram', 'WhatsApp', None], n_vendas, p=[0.3, 0.4, 0.15, 0.1, 0.05]),
    'forma_pagamento': np.random.choice(['Cartão de Crédito', 'Pix', 'Boleto', 'Dinheiro', None], n_vendas, p=[0.5, 0.3, 0.1, 0.05, 0.05])
}

df_vendas = pd.DataFrame(vendas_data)

# Trazendo o preço base dos produtos para calcular o total
df_vendas = df_vendas.merge(df_produtos[['sku', 'preco_base']], on='sku', how='left')

# Inserindo "sujeira" nos preços (simulando erro de sistema em 2% dos dados)
df_vendas['preco_unitario'] = df_vendas['preco_base']
mask_nulos = np.random.random(n_vendas) < 0.02
df_vendas.loc[mask_nulos, 'preco_unitario'] = np.nan

# Calculando valor total
df_vendas['valor_total'] = df_vendas['preco_unitario'] * df_vendas['quantidade']

print(f"  ├─ Geradas {len(df_vendas):,} linhas de vendas.")
print(f"  └─ Faturamento total simulado: R$ {df_vendas['valor_total'].sum():,.2f}")

#### INSERINDO ANOMALIAS PROPOSITAIS ####
print("\n[3/4] Inserindo Anomalias e Dados Sujos (CRISP-DM Prep)...")

# 1. Inserindo Duplicatas (Simulando erro de clique duplo no PDV)
df_duplicadas = df_vendas.sample(n=1000)
df_vendas = pd.concat([df_vendas, df_duplicadas], ignore_index=True)

# 2. Gerando Estoque com valores negativos propositais
estoque_data = {
    'sku': df_produtos['sku'],
    'qtd_estoque': [random.randint(-10, 500) for _ in range(len(df_produtos))]
}
df_estoque = pd.DataFrame(estoque_data)

print("\n[4/4] Salvando arquivos CSV...")

# Salvando os 4 arquivos fundamentais
df_vendas.to_csv(os.path.join(PASTA_DADOS, "fVendas.csv"), index=False, sep=';', encoding='utf-8')
df_produtos.to_csv(os.path.join(PASTA_DADOS, "dProdutos.csv"), index=False, sep=';', encoding='utf-8')
df_clientes.to_csv(os.path.join(PASTA_DADOS, "dClientes.csv"), index=False, sep=';', encoding='utf-8')
df_estoque.to_csv(os.path.join(PASTA_DADOS, "fEstoque.csv"), index=False, sep=';', encoding='utf-8')

print("=" * 70)
print("  SUCESSO: Arquivos gerados na pasta /dados")
print(f"  Total de vendas final (com duplicatas): {len(df_vendas):,}")
print("=" * 70)