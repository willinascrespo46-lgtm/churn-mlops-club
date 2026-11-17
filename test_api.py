from fastapi.testclient import TestClient
from api_churn import app

client = TestClient(app)

def test_docs_endpoint():
    """Verifica que la documentación interactiva (/docs) carga correctamente."""
    response = client.get("/docs")
    assert response.status_code == 200

def test_predecir_churn():
    """Verifica que el endpoint /predecir procesa un cliente válido y responde 200."""
    payload = {
        "antiguedad_meses": 12,
        "total_gastado": 450.50,
        "total_compras": 5,
        "tickets_pendientes": 1,
        "recencia_dias": 20,
        "categoria_plan": "Premium"
    }
    response = client.post("/predecir", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0