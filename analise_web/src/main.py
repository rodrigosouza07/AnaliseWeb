from extract import FinancialAPIExtractor
from transform import FinancialDataTransformer

def run_pipeline():
    print("🚀 Iniciando Pipeline ETL de Dados do PIX (Banco Central)...")

    # Mês base para consulta no formato 'AAAAMM'
    MES_BANCO_CENTRAL = "'202401'"  # Mantenha as aspas simples internas exigidas pelo OData
    
    # URL OData do Pix no Portal Olinda do Banco Central
    URL_PIX_OLINDA = (
        "https://olinda.bcb.gov.br/olinda/servico/Pix_DadosAbertos/versao/v1/odata/"
        f"EstatisticasTransacoesPix(Database=@Database)?@Database={MES_BANCO_CENTRAL}&$top=100&$format=json"
    )

    # 1. Extração
    extractor = FinancialAPIExtractor()
    print(f"📥 Buscando estatísticas do PIX para o mês {MES_BANCO_CENTRAL}...")
    
    # Chamada passando a nova URL direta
    json_response = extractor.fetch_from_url(URL_PIX_OLINDA)

    # A resposta do protocolo OData embrulha os dados dentro de uma chave chamada 'value'
    raw_data = json_response.get("value", []) if json_response else []

    # 2. Transformação
    transformer = FinancialDataTransformer()
    print("🔄 Transformando e tratando dados do PIX com Pandas...")
    
    df_pix = transformer.transform_pix_data(raw_data)

    # 3. Exibição e Validação
    if not df_pix.empty:
        print("\n✅ Transformação dos dados do PIX concluída com sucesso!")
        print("\n📊 Amostra dos Dados do PIX (Primeiras linhas):")
        print(df_pix.head(10))
        print(f"\n📋 Registros processados: {len(df_pix)}")
        print(f"\n🔎 Tipos de dados (Schema):\n{df_pix.dtypes}")
    else:
        print("❌ Falha no pipeline. Nenhum dado do PIX foi processado.")

if __name__ == "__main__":
    run_pipeline()