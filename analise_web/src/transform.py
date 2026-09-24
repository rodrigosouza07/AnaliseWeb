import pandas as pd
from typing import List, Dict

class FinancialDataTransformer:
    @staticmethod
    def transform_pix_data(raw_data: List[Dict]) -> pd.DataFrame:
        if not raw_data:
            return pd.DataFrame()

        # Converte lista de dicionários para DataFrame
        df = pd.DataFrame(raw_data)

        # Padroniza nomes de colunas para snake_case
        df.columns = [col.lower() for col in df.columns]

        # Garantir conversões de tipos
        if "ano_mes" in df.columns:
            df["ano_mes"] = df["ano_mes"].astype(str)
            
        if "valor" in df.columns:
            df["valor"] = pd.to_numeric(df["valor"], errors="coerce")

        if "quantidade" in df.columns:
            df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce")

        return df