from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(
    title="API de Predicción de Churn - Club Intelligence",
    description="Servicio en tiempo real para evaluar el riesgo de cancelación de clientes",
    version="1.0"
)

artefacto = joblib.load('modelo_churn.joblib')
modelo = artefacto['modelo']
columnas_modelo = artefacto['columnas']

class DatosCliente(BaseModel):
    antiguedad_meses: int
    total_gastado: float
    total_compras: int
    tickets_pendientes: int
    recencia_dias: int
    categoria_plan: str

@app.post("/predecir")
def predecir_churn(cliente: DatosCliente):
    ratio_tickets = (
        cliente.tickets_pendientes / cliente.total_compras
        if cliente.total_compras > 0
        else cliente.tickets_pendientes
    )

    datos = {
        'antiguedad_meses': cliente.antiguedad_meses,
        'total_gastado': cliente.total_gastado,
        'total_compras': cliente.total_compras,
        'tickets_pendientes': cliente.tickets_pendientes,
        'recencia_dias': cliente.recencia_dias,
        'ratio_tickets_pendientes': ratio_tickets,
        'categoria_plan_Básico': 1 if cliente.categoria_plan == 'Básico' else 0,
        'categoria_plan_Premium': 1 if cliente.categoria_plan == 'Premium' else 0,
        'categoria_plan_VIP': 1 if cliente.categoria_plan == 'VIP' else 0,
    }

    df_entrada = pd.DataFrame([datos])[columnas_modelo]

    prediccion = int(modelo.predict(df_entrada)[0])
    probabilidad = round(float(modelo.predict_proba(df_entrada)[0][1]) * 100, 2)

    if probabilidad >= 70:
        riesgo = "ALTO - Contactar Soporte / Descuento"
    elif probabilidad >= 30:
        riesgo = "MEDIO - Campaña de Re-engagement"
    else:
        riesgo = "BAJO - Cliente Sano"

    return {
        "prediccion_churn": prediccion,
        "probabilidad_fuga_porcentaje": probabilidad,
        "nivel_riesgo": riesgo
    }
