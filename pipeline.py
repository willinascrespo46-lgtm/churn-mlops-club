import os
import pandas as pd
import joblib
from dotenv import load_dotenv
from sqlalchemy import create_engine
from datetime import datetime

load_dotenv()

def ejecutar_pipeline():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Iniciando pipeline de predicción de Churn...")

    usuario = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST", "localhost")
    puerto = os.getenv("DB_PORT", "3306")
    base_datos = os.getenv("DB_NAME", "club_intelligence")

    engine = create_engine(f"mysql+pymysql://{usuario}:{password}@{host}:{puerto}/{base_datos}")

    df_clientes = pd.read_sql("SELECT * FROM clientes", engine)
    df_transacciones = pd.read_sql("SELECT * FROM transacciones", engine)
    df_tickets = pd.read_sql("SELECT * FROM tickets_soporte", engine)

    fecha_referencia = pd.to_datetime(df_transacciones['fecha_transaccion']).max()

    df_transacciones['fecha_transaccion'] = pd.to_datetime(df_transacciones['fecha_transaccion'])
    rfm = df_transacciones.groupby('id_clientes').agg(
        total_gastado=('monto', 'sum'),
        total_compras=('id_transacciones', 'count'),
        ultima_compra=('fecha_transaccion', 'max')
    ).reset_index()

    rfm['recencia_dias'] = (fecha_referencia - rfm ['ultima_compra']).dt.days

    tickets_pend = (
    df_tickets[df_tickets["resuelto"] == 0]
    .groupby("id_clientes")
    .size()
    .reset_index(name="tickets_pendientes")
)
    df_proc = df_clientes.merge(rfm[['id_clientes', 'total_gastado', 'total_compras', 'recencia_dias']], on='id_clientes', how='left')
    df_proc = df_proc.merge(tickets_pend, on='id_clientes', how='left')

    df_proc['total_gastado'] = df_proc['total_gastado'].fillna(0)
    df_proc['total_compras'] = df_proc['total_compras'].fillna(0)
    df_proc['tickets_pendientes'] = df_proc['tickets_pendientes'].fillna(0)
    df_proc['recencia_dias'] = df_proc['recencia_dias'].fillna(999)

    df_proc['ratio_tickets_pendientes'] = df_proc.apply(
        lambda row: row['tickets_pendientes'] / row['total_compras'] if row['total_compras'] > 0 else row['ticktes_pendientes'],
        axis=1
    )

    df_proc['categoria_plan_Básico'] = (df_proc['categoria_plan'] == 'Básico').astype(int)
    df_proc['categoria_plan_Premium'] = (df_proc['categoria_plan'] == 'Premium').astype(int)
    df_proc['categoria_plan_VIP'] = (df_proc['categoria_plan'] == 'VIP').astype(int)


    artefacto = joblib.load('modelo_churn.joblib')
    modelo = artefacto['modelo']
    columnas_modelo = artefacto['columnas']

    X_pred = df_proc[columnas_modelo]
    df_proc['prediccion_churn'] = modelo.predict(X_pred)
    df_proc['probabilidad_churn_pct'] = (modelo.predict_proba(X_pred)[:, 1] * 100).round(2)

    def clasificar_riesgo(prob):
        if prob >= 70:
            return 'ALTO - Contactar Soporte / Descuento'
        elif prob >= 30:
            return 'MEDIO - Campaña de Re-engagement'
        return 'BAJO - Cliente Sano'

    df_proc['nivel_riesgo'] = df_proc['probabilidad_churn_pct'].apply(clasificar_riesgo)
    df_proc['fecha_ejecucion'] = datetime.now()


    columnas_salida = [
        'id_clientes', 'nombre', 'categoria_plan', 'recencia_dias',
        'total_gastado', 'tickets_pendientes', 'prediccion_churn',
        'probabilidad_churn_pct', 'nivel_riesgo', 'fecha_ejecucion'
    ]

    df_proc[columnas_salida].to_sql('predicciones_churn', con=engine, if_exists='replace', index=False)
    print(f"¡Éxito! {len(df_proc)} registros procesados y guardados en la tabla 'predicciones_churn' de MySQL.")

if __name__ == "__main__":
    ejecutar_pipeline()
