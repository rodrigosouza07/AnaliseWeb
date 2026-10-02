from extract import FinancialAPIExtractor
from transform import FinancialDataTransformer
import requests

def run_pipeline():
    print("🚀 Iniciando Pipeline ETL de Dados do PIX (Banco Central)...")

    # Mês base para consulta no formato 'AAAAMM'
    MES_BANCO_CENTRAL = "'202401'"  # Mantenha as aspas simples internas exigidas pelo OData
    
    # URL OData do Pix no Portal Olinda do Banco Central
    url = (
        "https://olinda.bcb.gov.br/olinda/servico/"
        "Pix_DadosAbertos/versao/v1/odata/"
        "EstatisticasTransacoesPix(Database=@Database)"
        "?@Database='202401'"
        "&$top=1"
        "&$format=json"
    )

    try:
        print("🌐 Testando conexão com Banco Central...")

        response = requests.get(
            url,
            timeout=(10, 60)
        )

        print("Status:", response.status_code)
        print("Resposta:", response.text[:1000])

    except requests.exceptions.Timeout:
        print("❌ O servidor do Banco Central demorou mais de 60 segundos.")

    except requests.exceptions.ConnectionError as e:
        print("❌ Erro de conexão:", e)

    except requests.exceptions.RequestException as e:
        print("❌ Erro HTTP:", e)
        # 1. Extração
        extractor = FinancialAPIExtractor()
        print(f"📥 Buscando estatísticas do PIX para o mês {MES_BANCO_CENTRAL}...")
        
        # Chamada passando a nova URL direta
        json_response = extractor.fetch_from_url(url)

        # A resposta do protocolo OData embrulha os dados dentro de uma chave chamada 'value'
        raw_data = json_response.get("value", []) if json_response else []

        # 2. Transformação
        transformer = FinancialDataTransformer()
        print("🔄 Transformando e tratando dados do PIX com Pandas...")
        
        df_pix = transformer.transform_pix_data(raw_data)

if __name__ == "__main__":
    run_pipeline()