import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield

def test_root_endpoint():
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["engine"] == "Swiss Ephemeris"
    assert data["status"] == "Operational"

def test_create_and_get_birth_profile():
    profile_data = {
        "name": "Aryabhata Research Profile",
        "gender": "Male",
        "date_of_birth": "1995-10-24",
        "time_of_birth": "06:30:00",
        "birthplace": "Patna, Bihar, India",
        "country": "India",
        "state": "Bihar",
        "city": "Patna",
        "latitude": 25.5941,
        "longitude": 85.1376,
        "timezone_str": "Asia/Kolkata",
        "timezone_offset": 5.5,
    }
    resp = client.post("/api/profiles/", json=profile_data)
    assert resp.status_code == 200
    created = resp.json()
    assert created["id"] is not None
    assert created["name"] == profile_data["name"]

    # Calculate chart for this profile
    chart_resp = client.get(f"/api/chart/calculate/{created['id']}")
    assert chart_resp.status_code == 200
    chart_data = chart_resp.json()
    assert "chart_summary" in chart_data
    assert "planets" in chart_data
    assert len(chart_data["planets"]) == 12
    assert "houses" in chart_data
    assert len(chart_data["houses"]) == 12

    # Query divisional chart D9
    d9_resp = client.get(f"/api/calculations/divisional/{created['id']}/D9")
    assert d9_resp.status_code == 200
    assert d9_resp.json()["varga_key"] == "D9"

    # Query Vimshottari dasha
    dasha_resp = client.get(f"/api/calculations/dasha/{created['id']}")
    assert dasha_resp.status_code == 200
    assert "starting_mahadasha_lord" in dasha_resp.json()

    # Query Yogas
    yogas_resp = client.get(f"/api/calculations/yogas/{created['id']}")
    assert yogas_resp.status_code == 200
    assert isinstance(yogas_resp.json(), list)

    # Query Doshas
    doshas_resp = client.get(f"/api/calculations/doshas/{created['id']}")
    assert doshas_resp.status_code == 200
    assert isinstance(doshas_resp.json(), list)

    # Query Grounded AI Chat
    chat_req = {
        "profile_id": created["id"],
        "message": "Explain my Lagna and active yogas."
    }
    chat_resp = client.post("/api/ai/chat", json=chat_req)
    assert chat_resp.status_code == 200
    chat_json = chat_resp.json()
    assert "response" in chat_json
    assert "source" in chat_json
    assert len(chat_json["response"]) > 0

def test_engine_settings_and_dashboard():
    status_resp = client.get("/api/settings/status")
    assert status_resp.status_code == 200
    status_json = status_resp.json()
    assert status_json["engine_name"] == "Swiss Ephemeris"
    assert "LAHIRI" in status_json["supported_ayanamsas"]

    summary_resp = client.get("/api/settings/dashboard-summary")
    assert summary_resp.status_code == 200
    summary_json = summary_resp.json()
    assert "total_birth_charts" in summary_json
    assert "total_test_cases" in summary_json
