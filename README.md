# 🛡️ Sistema Predictivo de Fuga de Clientes (Churn MLOps) — Club Intelligence

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-009688?logo=fastapi&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-RandomForest-F7931E?logo=scikitlearn&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED?logo=docker&logoColor=white)

Arquitectura híbrida de Ciencia de Datos y MLOps de extremo a extremo diseñada para identificar clientes con riesgo de cancelación (`churn`), tanto mediante procesamiento masivo automatizado (*batch*) conectado a base de datos como a través de inferencia en tiempo real mediante API REST.

---

## 🏗️ Arquitectura del Proyecto

```mermaid
flowchart LR
    A[(MySQL: club_intelligence)] -->|Extracción SQL| B[Feature Engineering\nRFM + Soporte Técnico]
    B --> C{RandomForest Model\nmodelo_churn.joblib}
    C -->|Inferencia Batch\npipeline.py| D[(MySQL: predicciones_churn)]
    C -->|Inferencia Tiempo Real\napi_churn.py| E[FastAPI REST Endpoint\nPOST /predecir]



# 🚀 Churn Prediction MLOps Pipeline — Club Intelligence

![MLOps CI Pipeline](https://github.com/willinascrespo46-lgtm/churn-mlops-club/actions/workflows/ci.yml/badge.svg)

🌐 **API en Producción (Swagger UI):** [https://churn-mlops-club.onrender.com/docs](https://churn-mlops-club.onrender.com/docs)# 🚀 Churn Prediction MLOps Pipeline — Club Intelligence

![MLOps CI Pipeline](https://github.com/willinascrespo46-lgtm/churn-mlops-club/actions/workflows/ci.yml/badge.svg)

🌐 **API en Producción (Swagger UI):** [https://churn-mlops-club.onrender.com/docs](https://churn-mlops-club.onrender.com/docs)
