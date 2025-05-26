# src/reporting.py

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from matplotlib.axes import Axes
from typing import Tuple, Optional


def monthly_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera un informe mensual con sumas y tasas de autoconsumo/autosuficiencia.
    
    Parámetros:
        df: DataFrame con index datetime y columnas:
            - energy_kWh
            - pv_generated_kWh
            - pv_consumed_kWh
            - pv_surplus_kWh
    
    Retorna:
        DataFrame indexado por mes (final de mes) con columnas:
            - energy_kWh
            - pv_generated_kWh
            - pv_consumed_kWh
            - pv_surplus_kWh
            - self_consumption_rate    (pv_consumed_kWh / energy_kWh)
            - self_sufficiency_rate    (pv_consumed_kWh / pv_generated_kWh)
            - surplus_generation_rate  (pv_surplus_kWh / pv_generated_kWh)
    """
    # Sumar por mes
    monthly = df.resample("ME").sum()
    
    # Evitar división por cero
    sc_rate = (monthly["pv_consumed_kWh"] / monthly["energy_kWh"]).fillna(0)
    ss_rate = (monthly["pv_consumed_kWh"] / monthly["pv_generated_kWh"]).fillna(0)
    sg_rate = (monthly["pv_surplus_kWh"]   / monthly["pv_generated_kWh"]).fillna(0)
    
    report = monthly.assign(
        self_consumption_rate   = sc_rate,
        self_sufficiency_rate   = ss_rate,
        surplus_generation_rate = sg_rate
    )

    report = report.rename(columns={
        'energy_kWh': 'energía_total_demandada_kWh',
        'pv_generated_kWh': 'energía_pv_generada_kWh',
        'pv_consumed_kWh': 'energía_pv_consumida_directamente_kWh',
        'pv_surplus_kWh': 'energía_pv_disponible_excedente_kWh'
    })
    return report

def plot_monthly(report: pd.DataFrame) -> Axes:
    """
    Dibuja un gráfico de barras comparando demanda, generación, consumo y excedente mes a mes.
    
    Parámetros:
        report: DataFrame devuelto por monthly_report (debe contener las 4 columnas energéticas).
    
    Retorna:
        El objeto Axes de matplotlib para mayor personalización si se desea.
    """
    # Seleccionar solo las columnas de energía
    cols = ["energía_total_demandada_kWh", "energía_pv_generada_kWh", "energía_pv_consumida_directamente_kWh", "energía_pv_disponible_excedente_kWh"]
    df_plot = report[cols]
    
    ax = df_plot.plot(kind="bar", figsize=(12, 6), width=0.8)
    ax.set_xlabel("Mes")
    ax.set_ylabel("Energía (kWh)")
    ax.set_title("Energía Mensual: Demanda vs. Generación PV vs. Autoconsumo/Excedente")
    ax.legend(title="Tipo de energía")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    return ax

def plot_hourly_comparison(
    df_metrics: pd.DataFrame,
    index_name: Optional[str] = None
) -> 'plotly.graph_objs._figure.Figure':
    """
    Genera un gráfico interactivo horario usando Plotly de generación PV frente a carga.

    Parámetros:
        df_metrics: DataFrame con índice datetime y columnas 'pv_generated_kWh', 'energy_kWh'.
        index_name: nombre de la columna de tiempo si df_metrics ha renombrado índice; si no se pasa, se usa el índice original.

    Retorna:
        fig: Objeto Figure de Plotly.
    """
    # Prepara DataFrame para Plotly
    df = df_metrics.reset_index()
    # Determinar columna de tiempo
    if index_name and index_name in df.columns:
        time_col = index_name
    else:
        time_col = df.columns[0]  # primera columna tras reset_index()
    df = df.rename(columns={time_col: 'time'})

    fig = px.line(
        df,
        x='time',
        y=['pv_generated_kWh', 'energy_kWh'],
        labels={'value': 'Energía (kWh)', 'variable': 'Serie'},
        title='Generación PV vs. Demanda Horaria'
    )
    fig.update_layout(xaxis_title='Fecha y Hora', yaxis_title='kWh')
    return fig