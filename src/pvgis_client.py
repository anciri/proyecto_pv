# src/pvgis_client.py

import requests
import pandas as pd
from typing import Tuple
from src.config import PVGISParams

PVGIS_BASE_URL = "https://re.jrc.ec.europa.eu/api/seriescalc?"

def fetch_pvgis_hourly(params: PVGISParams, timeout: int = 30) -> Tuple[pd.DataFrame, dict]:
    # Construimos un payload sin los valores None
    payload = {k: v for k, v in params.__dict__.items() if v is not None}

    try:
        resp = requests.get(PVGIS_BASE_URL, params=payload, timeout=timeout)
        resp.raise_for_status()
    except requests.HTTPError as err:
        # Intentamos extraer un mensaje de error más detallado
        try:
            err_json = resp.json()
            msg = err_json.get("error", err_json)
        except Exception:
            msg = resp.text[:200]
        raise RuntimeError(f"PVGIS API devolvió {resp.status_code}: {msg}")
    except requests.RequestException as exc:
        raise RuntimeError(f"Error en la petición PVGIS: {exc}")

    data = resp.json()
    if "outputs" not in data or "hourly" not in data["outputs"]:
        raise RuntimeError("Respuesta PVGIS no contiene 'outputs.hourly'.")

    # DataFrame horario
    df = pd.DataFrame(data["outputs"]["hourly"])
    df["time"] = pd.to_datetime(df["time"], format="%Y%m%d:%H%M", utc=True)
    df = df.set_index("time").sort_index()

    # Metadata simplificada
    meta = data.get("meta", {})
    return df, meta
