import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import (
  create_tables
)

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_database(tmp_path):
  database_path = tmp_path / "test_expenses.db"

  create_tables(database_path)
  app.state.database_path = database_path

  yield

  app.state.database_path = "expenses.db"


def test_home():
  response = client.get("/")

  assert response.status_code == 200
  assert response.json() == {
    "message": "Welcome to Expense Tracker"
  }


def test_create_expense():
  response = client.post(
    "/expenses",
    json={
        "description": "Pizza",
        "amount": 32.5,
        "category": "Food",
    },
  )

  assert response.status_code == 201
  assert response.json() == {
    "id": 1,
    "description": "Pizza",
    "amount": 32.5,
    "category": "Food",
  }


def test_create_expense_invalid_amount():
  response = client.post(
    "/expenses",
    json={
        "description": "Pizza",
        "amount": "not a number",
        "category": "Food",
    },
  )

  assert response.status_code == 422
  assert len(client.get("/expenses").json()) == 0


def test_create_multiple_expenses():
  response_1 = client.post(
    "/expenses",
    json={
      "description": "Pizza",
      "amount": 32.50,
      "category": "Food",
    }
  )

  assert response_1.status_code == 201
  assert response_1.json()["id"] == 1

  response_2 = client.post(
    "/expenses",
    json={
      "description": "Bus ticket",
      "amount": 4.80,
      "category": "Transport",
    }
  )

  assert response_2.status_code == 201
  assert response_2.json()["id"] == 2

  get_response = client.get("/expenses").json()
  assert len(get_response) == 2
  assert get_response[0]["category"] == "Food"
  assert get_response[1]["category"] == "Transport"


def test_read_expense():
  post_response = client.post(
    "/expenses",
    json={
      "description": "Coffee",
      "amount": 9.99,
      "category": "Food"
    }
  )

  expense_id = post_response.json()["id"]
  assert expense_id is not None

  result = client.get(
    f"/expenses/{expense_id}"
  )

  assert result.status_code == 200
  assert result.json()["description"] == "Coffee"
  assert result.json()["amount"] == 9.99
  assert result.json()["category"] == "Food"
  assert result.json()["id"] == expense_id


def test_read_missing_expense():
  response = client.get("/expenses/999")

  assert response.status_code == 404


def test_delete_existing_expense():
  expense = client.post(
    "/expenses",
    json={
      "description": "Coffee",
      "amount": 9.99,
      "category": "Food"
    })

  expense_id = expense.json()["id"]

  delete_res = client.delete(f"/expenses/{expense_id}")
  assert delete_res.status_code == 204

  get_res = client.get(f"/expenses/{expense_id}")
  assert get_res.status_code == 404


def test_delete_non_existing_expense():
  res = client.delete("/expenses/999")
  assert res.status_code == 404