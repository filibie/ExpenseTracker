from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

from app.database import (
    create_tables,
    insert_expense,
    get_expenses,
    get_expense_by_id,
    delete_expense,
    update_expense,
)

app = FastAPI()

DATABASE_PATH = "expenses.db"
app.state.database_path = DATABASE_PATH

create_tables(DATABASE_PATH)

class Expense(BaseModel):
  description: str
  amount: float
  category: str


@app.get("/")
def home():
  return { "message": "Welcome to Expense Tracker" }


@app.get("/expenses")
def read_expenses():
  return get_expenses(app.state.database_path)


@app.post("/expenses", status_code=status.HTTP_201_CREATED)
def create_expense(expense: Expense):
  return insert_expense(
    expense.description,
    expense.amount,
    expense.category,
    app.state.database_path,
  )


@app.get("/expenses/{expense_id}")
def read_expense(expense_id: int):
  result = get_expense_by_id(expense_id, app.state.database_path)
  if result is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Expense not found")

  return result


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_expense(expense_id: int):
  res = delete_expense(expense_id, app.state.database_path)
  if not res:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")


@app.put("/expenses/{expense_id}")
def edit_expense(expense_id: int, expense: Expense):
  updated_expense = update_expense(
    expense_id,
    expense.description,
    expense.amount,
    expense.category,
    app.state.database_path,
  )

  if updated_expense is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Expense not found"
    )

  return updated_expense