import requests
from typing import Optional, Dict, Any

class FinancialAPIExtractor:
    def __init__(self, timeout: int = 15):
        self.timeout = timeout

    def fetch_from_url(self, url: str) -> Optional[Dict[str, Any]]:
        """Busca dados JSON diretamente de qualquer URL HTTP."""
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na requisição HTTP: {e}")
            return None