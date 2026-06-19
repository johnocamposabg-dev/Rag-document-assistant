from starlette.testclient import TestClient
from main import app
from pathlib import Path
import pytest

client = TestClient(app)
SAMPLE_PDF = Path(__file__).parent / "sample.pdf"

@pytest.fixture
def uploaded_document():
    with open(SAMPLE_PDF, "rb") as f:
        response = client.post("/documents/upload/", files={"file": ("sample.pdf", f, "application/pdf")})
    assert response.status_code == 200
    data = response.json()
    yield data["document_id"]
    client.delete(f"/documents/{data['document_id']}") 

def test_chat_with_uploaded_document(uploaded_document, monkeypatch):
    document_id = uploaded_document
    def mock_chat_response(*args, **kwargs):
        return "Respuesta de prueba"
    
    monkeypatch.setattr("routes.chat.get_answer", mock_chat_response)
    
    response = client.post("/chat/query/", json={"document_id": document_id, "question": "What is in the document?"})
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "Respuesta de prueba"
    assert "sources" in data