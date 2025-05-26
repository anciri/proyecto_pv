# src/processing.py

import pandas as pd
import numpy as np
from typing import Tuple

def remove_leap_day(df: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina los registros correspondientes al 29 de febrero de cualquier año.
    """
    mask = ~((df.index.month == 2) & (df.index.day == 29))
    return df.loc[mask].copy()

def compute_annual_median(df: pd.DataFrame, value_col: str) -> pd.Series:
    """
    Calcula la mediana de `value_col` para cada hora del año (excluyendo 29Feb).
    Devuelve una Serie indexada por cadena 'MM-DD HH:MM'.
    """
    df2 = remove_leap_day(df)
    df2['mdh'] = df2.index.strftime('%m-%d %H:%M')
    med = df2.groupby('mdh')[value_col].median()
    return med

def align_consumption(consumption: pd.Series, profile: pd.Series) -> pd.DataFrame:
    """
    Crea un DataFrame con la serie de consumo (kWh) y el perfil horario (W).
    `consumption` debe tener índice datetime, `profile` debe mapear 'MM-DD HH:MM' -> valor.
    """
    df = consumption.to_frame('energy_kWh').copy()
    df['profile_W'] = df.index.strftime('%m-%d %H:%M').map(profile.to_dict()).fillna(0)
    return df

def compute_pv_metrics(df: pd.DataFrame) -> Tuple[pd.DataFrame, float]:
    """
    A partir de un DataFrame con columnas 'energy_kWh' y 'profile_W', calcula:
      - 'required_kW': potencia PV necesaria por hora.
      - Cuantil 75% -> potencia instalada óptima.
      - 'pv_generated_kWh', 'pv_consumed_kWh', 'pv_surplus_kWh'.
    Devuelve el DataFrame con estas columnas y la potencia instalada (kW).
    """
    df = df.copy()
    # Potencia necesaria:
    df['required_kW'] = np.where(
        df['profile_W'] > 0,
        df['energy_kWh'] / (df['profile_W'] / 1e3),
        0
    )
    # Cuantil 75%:
    installed = df['required_kW'].quantile(0.75)
    # Generación PV con la potencia instalada:
    df['pv_generated_kWh'] = installed * df['profile_W'] / 1e3
    # Autoconsumo directo:
    df['pv_consumed_kWh'] = np.minimum(df['energy_kWh'], df['pv_generated_kWh'])
    # Excedente:
    df['pv_surplus_kWh'] = df['pv_generated_kWh'] - df['pv_consumed_kWh']
    return df, installed
