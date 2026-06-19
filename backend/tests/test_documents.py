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




def test_upload_document():
    with open(SAMPLE_PDF, "rb") as f:
        response = client.post("/documents/upload/", files={"file": ("sample.pdf", f, "application/pdf")})
    assert response.status_code == 200
    data = response.json()
    assert "document_id" in data
    assert data["filename"] == "sample.pdf"
    assert data["size"] > 0
    assert data["chunks_count"] > 0

def test_list_documents():
    response = client.get("/documents/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for doc in data:
        assert "id" in doc
        assert "filename" in doc
        assert "size" in doc
        assert "created_at" in doc

def test_get_document(uploaded_document):
    response = client.get(f"/documents/{uploaded_document}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == uploaded_document
    assert data["filename"] == "sample.pdf"
    assert data["size"] > 0
    assert "created_at" in data
    

def test_delete_document(uploaded_document):
    response = client.delete(f"/documents/{uploaded_document}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Document deleted successfully"
    get_response = client.get(f"/documents/{uploaded_document}")
    assert get_response.status_code == 404