import requests
from typing import Dict, List, Optional

class FinancialAPIExtractor:
    """Classe responsável por extrair dados da API do Banco Central do Brasil."""
    
    BASE_URL = "https://olinda.bcb.gov.br/olinda/servico/Pix_DadosAbertos/versao/v1/odata/EstatisticasTransacoesPix(Database=@Database)?@Database=''&$top=100&$format=json"

    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def fetch_series(self, series_code: int, start_date: str, end_date: str) -> Optional[List[Dict]]:
        """
        Busca uma série temporal por código.
        
        Args:
            series_code: Código da série no SGS (ex: 11 para SELIC, 10813 para Dólar PTAX).
            start_date: Data inicial no formato 'DD/MM/AAAA'.
            end_date: Data final no formato 'DD/MM/AAAA'.
        """
        url = self.BASE_URL.format(code=series_code)
        params = {
            "formato": "json",
            "dataInicial": start_date,
            "dataFinal": end_date
        }

        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()  # Levanta exceção para status HTTP 4xx/5xx
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na requisição para a série {series_code}: {e}")
            return None