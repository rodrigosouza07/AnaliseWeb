import pandas as pd
from typing import List, Dict, Optional

class FinancialDataTransformer:
    """Classe responsável pelo tratamento e limpeza dos dados com Pandas."""

    @staticmethod
    def transform_bcb_data(raw_data: Optional[List[Dict]], metric_name: str) -> pd.DataFrame:
        """
        Limpa e padroniza o JSON bruto em um DataFrame Pandas pronto para gravação.
        """
        if not raw_data:
            print("⚠️ Dados brutos vazios ou inválidos para transformação.")
            return pd.DataFrame()

        # 1. Carrega dados brutos
        df = pd.DataFrame(raw_data)

        # 2. Renomeia e limpa colunas
        df.rename(columns={"data": "data_registro", "valor": metric_name}, inplace=True)

        # 3. Conversão de tipos de dados (Data e Numéricos)
        df["data_registro"] = pd.to_datetime(df["data_registro"], format="%d/%m/%Y")
        df[metric_name] = pd.to_numeric(df[metric_name], errors="coerce")

        # 4. Tratamento de valores ausentes/nulos
        df.dropna(subset=["data_registro", metric_name], inplace=True)

        # 5. Engenharia de Recursos / Métricas derivadas
        df["ano"] = df["data_registro"].dt.year
        df["mes"] = df["data_registro"].dt.month
        df["dia_da_semana"] = df["data_registro"].dt.day_name()
        
        # Média móvel de 7 períodos para análise de tendência
        df[f"{metric_name}_media_movel_7d"] = df[metric_name].rolling(window=7, min_periods=1).mean()

        # Ordenação cronológica
        df.sort_values(by="data_registro", ascending=True, inplace=True)
        df.reset_index(drop=True, inplace=True)

        return df