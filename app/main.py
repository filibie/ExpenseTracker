from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

class Expense(BaseModel):
  description: str
  amount: float
  category: str

expenses = []
next_id = 1

@app.get("/")
def home():
  return { "message": "Welcome to Expense Tracker" }


@app.get("/expenses")
def get_expenses():
  return expenses


@app.post("/expenses", status_code=status.HTTP_201_CREATED)
def create_expense(expense: Expense):
  global next_id
  new_expense = expense.model_dump()
  new_expense["id"] = next_id
  expenses.append(new_expense)
  next_id += 1

  return new_expense
