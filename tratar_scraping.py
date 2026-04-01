import pandas as pd
import os

#### Configuração de Caminhos ####
PASTA_DADOS = os.path.join(os.path.dirname(__file__), "dados")
arquivo_sujo = os.path.join(PASTA_DADOS, "tendencias_mercado.csv")
arquivo_limpo = os.path.join(PASTA_DADOS, "tendencias_limpas.csv")

print("=" * 70)
print("  PASSO 6.1: REFINAMENTO FINAL DE TEXT MINING")
print("=" * 70)

if not os.path.exists(arquivo_sujo):
    print("❌ Erro: O arquivo 'tendencias_mercado.csv' não foi encontrado!")
else:
    #### Carregar os dados do Scraping ####
    df = pd.read_csv(arquivo_sujo, sep=';', encoding='utf-8-sig')
    total_inicial = len(df)

    #### Lista de Termos de Ruído Final ####
    ruido_final = [
        'adrieny', 'magalhães', 'digital completo', 'revista em casa', 
        'claudia', 'newsletter', 'whatsapp', 'inscreva-se', 'cadastro',
        'superinteressante', 'guia do estudante', 'viagem e turismo',
        'veja', 'negócios', 'zero hora', 'acesse as notícias', 'através de nosso app'
    ]

    #### Remover linhas com termos de ruído ####
    df_limpo = df[~df['termo_tendencia'].str.contains('|'.join(ruido_final), case=False, na=False)].copy()

    #### Remover títulos de seção ####
    df_limpo = df_limpo[~df_limpo['termo_tendencia'].str.endswith(':')]

    #### Limpeza de Caracteres: Remover numeração de listas ####
    df_limpo['termo_tendencia'] = df_limpo['termo_tendencia'].str.replace(r'^\d+\.\s+', '', regex=True)

    #### Filtro de Relevância por Tamanho e Duplicatas ####
    df_limpo = df_limpo[df_limpo['termo_tendencia'].str.len() > 15]
    df_limpo = df_limpo.drop_duplicates()

    #### Salvar a Base Pronta para o Modelo ####
    df_limpo.to_csv(arquivo_limpo, index=False, sep=';', encoding='utf-8-sig')

    print(f"✅ Tratamento finalizado!")
    print(f"  ├─ Termos originais: {total_inicial}")
    print(f"  ├─ Termos limpos e prontos: {len(df_limpo)}")
    print(f"  └─ Insights preservados: {list(df_limpo['termo_tendencia'].head(2))}")

print("=" * 70)