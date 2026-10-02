import time
import requests
from typing import Optional, Dict, Any


class FinancialAPIExtractor:

    def __init__(
        self,
        timeout: int = 60,
        retries: int = 3,
        retry_delay: int = 5
    ):
        self.timeout = timeout
        self.retries = retries
        self.retry_delay = retry_delay

    def fetch_from_url(
        self,
        url: str
    ) -> Optional[Dict[str, Any]]:
        """
        Busca dados JSON diretamente de uma URL HTTP/HTTPS.

        Possui:
        - timeout configurável
        - tentativas automáticas
        - tratamento de erros HTTP
        - validação da resposta JSON
        """

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }

        for tentativa in range(1, self.retries + 1):

            try:

                print(
                    f"🌐 Tentativa {tentativa}/{self.retries}"
                )

                print(
                    f"📡 Consultando: {url}"
                )

                response = requests.get(
                    url,
                    headers=headers,
                    timeout=(10, self.timeout)
                )

                print(
                    f"📥 Status HTTP: {response.status_code}"
                )

                response.raise_for_status()

                data = response.json()

                print(
                    "✅ Dados recebidos com sucesso!"
                )

                return data

            except requests.exceptions.Timeout:

                print(
                    f"⏱️ Timeout na tentativa "
                    f"{tentativa}/{self.retries}"
                )

            except requests.exceptions.HTTPError as e:

                print(
                    f"❌ Erro HTTP: {e}"
                )

                return None

            except requests.exceptions.ConnectionError as e:

                print(
                    f"🔌 Erro de conexão: {e}"
                )

            except ValueError:

                print(
                    "❌ A resposta recebida não é um JSON válido."
                )

                return None

            except requests.exceptions.RequestException as e:

                print(
                    f"❌ Erro na requisição HTTP: {e}"
                )

            if tentativa < self.retries:

                print(
                    f"⏳ Aguardando {self.retry_delay} segundos "
                    "antes de tentar novamente..."
                )

                time.sleep(self.retry_delay)

        print(
            "❌ Não foi possível obter os dados "
            "após todas as tentativas."
        )

        return None