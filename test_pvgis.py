from src.config import PVGISParams
from src.pvgis_client import fetch_pvgis_hourly

# Parámetros de ejemplo
params = PVGISParams(
    lat=40.4165,
    lon=-3.7026,
    startyear=2020,
    endyear=2020,
    peakpower=1.0
)

df, meta = fetch_pvgis_hourly(params)

print("Metadata PVGIS:", meta)
print("Primeras filas del DataFrame:")
print(df.head())
