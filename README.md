@'

\# 🛡️ Sistema Predictivo de Fuga de Clientes (Churn MLOps) — Club Intelligence



Arquitectura híbrida de Ciencia de Datos y MLOps de extremo a extremo diseñada para identificar clientes con riesgo de cancelación (`churn`), tanto mediante procesamiento masivo automatizado (\*batch\*) conectado a base de datos como a través de inferencia en tiempo real mediante API REST.



\---



\## 🏗️ Arquitectura del Proyecto



```text

+-------------------+       +------------------------+       +-----------------------+

|   MySQL Database  | ----> |  Feature Engineering   | ----> |  RandomForest Model   |

| (club\_intelligence)|       | (RFM + Soporte Técnico) |       | (modelo\_churn.joblib) |

+-------------------+       +------------------------+       +-----------+-----------+

&#x20;        ^                                                               |

&#x20;        |                   +------------------------+                  |

&#x20;        +-------------------|   Batch Pipeline       | <----------------+

&#x20;        |  (Tabla salida:   |    (pipeline.py)       |                  |

&#x20;        |predicciones\_churn)+------------------------+                  |

&#x20;                                                                        |

&#x20;                            +------------------------+                  |

&#x20;                            |   API REST Tiempo Real | <----------------+

&#x20;                            |  FastAPI (api\_churn.py)|

&#x20;                            +------------------------+

