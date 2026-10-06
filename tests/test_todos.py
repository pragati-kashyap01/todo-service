from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_todo():
    response = client.post(
        "/todos",
        json={
            "title": "Pytest todo",
            "description":"Created during testing",
            "priority": "high",
            "due_date": "2026-10-22",
            "user_id": 2
        }
    )
    
    assert response.status_code == 201
    assert response.json()["title"]== "Pytest todo"
    
def test_get_non_existing_tod0():
    response = client.get("/todos/99999?user_id=2")
    
    assert response.status_code == 404
    assert response.json() == {"error": "Todo not found"}
    
def test_get_todos():
    response = client.get("/todos?user_id=2")
    
    assert response.status_code == 200
    assert isinstance(response.json(),list)

def test_filter_todos_by_priority():
    response = client.get("/todos?priority=high&user_id=2")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
def test_user_cannot_access_another_users_todo():
    create_response = client.post(
        "/todos",
        json={
            "title": "Private Todo",
            "description": "User 2 private todo",
            "priority": "high",
            "due_date": "2026-10-22",
            "user_id": 2
        }
    )

    assert create_response.status_code == 201

    todo_id = create_response.json()["id"]

    response = client.get(
        f"/todos/{todo_id}?user_id=999"
    )

    assert response.status_code == 404
    assert response.json() == {"error": "Todo not found"}