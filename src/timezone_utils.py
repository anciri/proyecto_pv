# src/timezone_utils.py

from datetime import datetime
from timezonefinder import TimezoneFinder
import pytz

def get_utc_offset_hours(lat: float, lon: float) -> float:
    """
    Devuelve el offset UTC (en horas) de la ubicación dada.
    
    Parámetros:
        lat (float): Latitud en grados decimales.
        lon (float): Longitud en grados decimales.
    
    Retorna:
        float: Desplazamiento con respecto a UTC en horas (puede ser negativo).
    """
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lat=lat, lng=lon)
    if tz_name is None:
        raise ValueError(f"No se pudo determinar la zona horaria para ({lat}, {lon})")
    
    tz = pytz.timezone(tz_name)
    # Tomamos la fecha y hora actual UTC para calcular el offset real (incluye horario de verano)
    now_utc = datetime.utcnow()
    offset = tz.utcoffset(now_utc)
    if offset is None:
        raise RuntimeError(f"No se pudo obtener el offset para la zona {tz_name}")
    return offset.total_seconds() / 3600
