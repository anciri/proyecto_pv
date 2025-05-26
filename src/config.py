# src/config.py

from dataclasses import dataclass
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el .env en el proyecto raíz
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), os.pardir, ".env"))

# Lee la clave de API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("❌ No se encontró la variable GOOGLE_API_KEY en el archivo .env")

@dataclass
class PVGISParams:
    """
    Parámetros para la llamada a PVGIS.
    """
    lat: float
    lon: float
    usehorizon: int = 1
    raddatabase: str | None = None
    startyear: int = 2013
    endyear: int = 2023
    pvcalculation: int = 1
    peakpower: float = 1.0
    pvtechchoice: str = "crystSi"
    mountingplace: str = "free"
    loss: float = 15.0
    trackingtype: int = 0
    angle: float = 0.0
    aspect: float = 0.0
    outputformat: str = "json"
