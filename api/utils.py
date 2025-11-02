import pandas as pd

def normalize_input(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoyage / harmonisation des valeurs en entrée.
    À enrichir selon ton préprocesseur.
    """
    for col in df.select_dtypes(include="object"):
        df[col] = df[col].str.strip().str.capitalize()
    return df
