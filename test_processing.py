import numpy as np
import pandas as pd
from src.processing import (
    remove_leap_day,
    compute_annual_median,
    align_consumption,
    compute_pv_metrics
)

# 1) Simula un DataFrame con fecha y consumo:
date_range = pd.date_range("2020-01-01", "2020-01-03 23:00", freq="H", tz="UTC")
df_demo = pd.DataFrame({
    "value": np.sin(np.linspace(0, 10, len(date_range))) * 100,
}, index=date_range)

# 2) Prueba remove_leap_day (no debería eliminar nada en este rango):
df_noleap = remove_leap_day(df_demo)
assert df_noleap.shape == df_demo.shape

# 3) Calcula mediana anual de 'value':
profile = compute_annual_median(df_demo, "value")
print("Perfil mediano:", profile.head())

# 4) Alinea una serie de consumo ficticia (usa 'value' como energía kWh):
aligned = align_consumption(df_demo['value'], profile)
print(aligned.head())

# 5) Calcula métricas PV:
metrics_df, installed_kw = compute_pv_metrics(aligned)
print("Potencia instalada (kW):", installed_kw)
print(metrics_df.head())

# 6) Verifica columnas calculadas:
assert 'required_kW' in metrics_df.columns