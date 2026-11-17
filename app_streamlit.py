import streamlit as st
import requests

st.set_page_config(
    page_title="Club Intelligence — Predictor de Churn",
    page_icon="🛡️",
    layout="centered"
)
st.title("🛡️ Predictor de Fuga de Clientes (Churn)")
st.markdown("Simulador interactivo conectado en tiempo real a la API de Machine Learning desplegada en Render.")


API_URL = "https://churn-mlops-club.onrender.com/predecir"

st.subheader("📋 Datos del Cliente")

col1, col2 = st.columns(2)

with col1:
    antiguedad_meses = st.slider("Antigüedad (meses)", min_value=1, max_value=72, value=12)
    total_gastado = st.number_input("Total gastado ($)", min_value=0.0, max_value=10000.0, value=450.0, step=50.0)
    total_compras = st.number_input("Total de compras", min_value=1, max_value=200, value=10)

with col2:
    tickets_pendientes = st.slider("Tickets de soporte pendientes", min_value=0, max_value=15, value=1)
    recencia_dias = st.slider("Días desde la última compra (Recencia)", min_value=0, max_value=365, value=30)
    categoria_plan = st.selectbox("Categoría del plan", ["Básico", "Estándar", "Premium"])

if st.button("🔍 Evaluar Riesgo de Fuga", type="primary", use_container_width=True):
    payload = {
        "antiguedad_meses": antiguedad_meses,
        "total_gastado": total_gastado,
        "total_compras": total_compras,
        "tickets_pendientes": tickets_pendientes,
        "recencia_dias": recencia_dias,
        "categoria_plan": categoria_plan
    }
    
    with st.spinner("Consultando modelo en la nube (puede tardar ~30s si el servidor estaba en reposo)..."):
        try:
            response = requests.post(API_URL, json=payload, timeout=60)
            if response.status_code == 200:
                resultado = response.json()
                prob = resultado["probabilidad_fuga_porcentaje"]
                riesgo = resultado["nivel_riesgo"]
                
                st.divider()
                st.subheader("📊 Resultado del Modelo")
                
                # Métrica principal y barra visual
                st.metric(label="Probabilidad de Cancelación", value=f"{prob}%")
                st.progress(min(prob / 100, 1.0))
                
                if prob >= 70:
                    st.error(f"🚨 **Nivel de Riesgo:** {riesgo}")
                elif prob >= 35:
                    st.warning(f"⚠️ **Nivel de Riesgo:** {riesgo}")
                else:
                    st.success(f"✅ **Nivel de Riesgo:** {riesgo}")
            else:
                st.error(f"Error en la API (Código {response.status_code}): {response.text}")
        except Exception as e:
            st.error(f"No se pudo conectar con la API: {e}")