import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_expenses():
  from app import main

  main.expenses.clear()
  main.next_id = 1


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
