from datetime import date as Date
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from pathlib import Path
from fastapi.responses import FileResponse

from app.database import (
  DATABASE_PATH,
  create_tables,
  insert_expense,
  get_expenses,
  get_expense_by_id,
  delete_expense,
  update_expense,
  get_expense_summary,
  get_expenses_by_category,
  get_monthly_expenses,
  get_monthly_spending_comparison,
  get_biggest_spending_category,
)

app = FastAPI()

app.state.database_path = str(DATABASE_PATH)

create_tables(DATABASE_PATH)

class Expense(BaseModel):
  description: str
  amount: float
  category: str
  date: Date = Field(default_factory=Date.today)

STATIC_DIR = Path(__file__).resolve().parent / "static"

@app.get("/")
def home():
  return FileResponse(STATIC_DIR / "index.html")


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
    expense.date.isoformat(),
  )


@app.get("/expenses/summary")
def expense_summary():
  return get_expense_summary(app.state.database_path)


@app.get("/expenses/by-category")
def expenses_by_category():
  return get_expenses_by_category(app.state.database_path)


@app.get("/expenses/by-month")
def expenses_by_month():
    return get_monthly_expenses(app.state.database_path)


@app.get("/expenses/insights")
def monthly_insights():
    comparison = get_monthly_spending_comparison(
        app.state.database_path
    )
    biggest_category = get_biggest_spending_category(
        app.state.database_path
    )

    return {
        **comparison,
        "biggest_category": biggest_category,
    }


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
