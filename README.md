 🛡️ Sistema Predictivo de Fuga de Clientes (Churn MLOps) — Club Intelligence



Arquitectura híbrida de Ciencia de Datos y MLOps de extremo a extremo diseñada para identificar clientes con riesgo de cancelación (`churn`), tanto mediante procesamiento masivo automatizado (\*batch\*) conectado a base de datos como a través de inferencia en tiempo real mediante API REST.


 🏗️ Arquitectura del Proyecto



+-------------------+       +------------------------+       +-----------------------+
|   MySQL Database  | ----> |  Feature Engineering   | ----> |  RandomForest Model   |
| (club_intelligence)|       | (RFM + Soporte Técnico) |       | (modelo_churn.joblib) |
+-------------------+       +------------------------+       +-----------+-----------+
         ^                                                               |
         |                   +------------------------+                  |
         +-------------------|   Batch Pipeline       | <----------------+
         |  (Tabla salida:   |    (pipeline.py)       |                  |
         |predicciones_churn)+------------------------+                  |
                                                                         |
                             +------------------------+                  |
                             |   API REST Tiempo Real | <----------------+
                             |  FastAPI (api_churn.py)|
                             +------------------------+

