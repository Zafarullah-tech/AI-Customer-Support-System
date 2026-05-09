
import pytest
from unittest.mock import patch, MagicMock

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "AI Customer Support API is running"}

@patch('chatbot.client.chat.completions.create')
def test_ask_endpoint(mock_create, client):
    # Mock Groq
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Standard shipping takes 3-5 days."
    mock_create.return_value = mock_response

    response = client.post("/ask", json={"query": "How long is shipping?"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["intent"] == "delivery_time"
    assert "id" in data

def test_escalate_endpoint(client):
    # First create an interaction
    with patch('chatbot.client.chat.completions.create') as mock_create:
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Mock response"
        mock_create.return_value = mock_response
        
        ask_res = client.post("/ask", json={"query": "Test query"})
        interaction_id = ask_res.json()["id"]

    # Now escalate it
    response = client.post("/escalate", json={"interaction_id": interaction_id})
    assert response.status_code == 200
    assert response.json()["message"] == "Query successfully escalated to a human agent."

def test_logs_endpoint(client):
    # Create an interaction
    with patch('chatbot.client.chat.completions.create') as mock_create:
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Log test"
        mock_create.return_value = mock_response
        client.post("/ask", json={"query": "Log me"})

    response = client.get("/logs")
    assert response.status_code == 200
    logs = response.json()
    assert len(logs) >= 1
    assert logs[0]["user_query"] == "Log me"

def test_concurrent_interactions(client):
    # Simulate concurrent interactions using multiple requests in a loop
    # In a real integration test, we might use threading, but for TestClient, 
    # we just want to ensure sequential integrity first, or use a tool like Locust later.
    for i in range(5):
        with patch('chatbot.client.chat.completions.create') as mock_create:
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = f"Response {i}"
            mock_create.return_value = mock_response
            
            res = client.post("/ask", json={"query": f"Query {i}"})
            assert res.status_code == 200
