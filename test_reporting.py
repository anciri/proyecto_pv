import pandas as pd
import numpy as np
from src.reporting import monthly_report, plot_monthly

# Simula un DataFrame con un trimestre de datos
dates = pd.date_range("2020-01-01", "2020-03-31 23:00", freq="h", tz="UTC")
n = len(dates)
rng = np.random.RandomState(0)
df = pd.DataFrame({
    "energy_kWh": rng.uniform(50, 150, size=n),
    "pv_generated_kWh": rng.uniform(0, 100, size=n),
}, index=dates)

# A partir de generated, asumimos consumed = min(demand, generated)
df["pv_consumed_kWh"] = np.minimum(df["energy_kWh"], df["pv_generated_kWh"])
df["pv_surplus_kWh"]  = df["pv_generated_kWh"] - df["pv_consumed_kWh"]

report = monthly_report(df)
print("Informe mensual:")
print(report)

# Prueba el plot (se abrirá una ventana o se mostrará inline en Jupyter)
ax = plot_monthly(report)
