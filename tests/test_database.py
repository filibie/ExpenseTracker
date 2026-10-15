import pytest

from app.database import (
    create_tables,
    insert_expense,
    get_expenses,
    get_expense_by_id,
    delete_expense,
    update_expense,
    get_expense_summary,
)

def test_insert_expense(tmp_path):
    database_path = tmp_path / "test_expenses.db"

    create_tables(database_path)

    new_expense = insert_expense("Pizza", 35.50, "Food", database_path)

    assert new_expense["id"] == 1
    assert new_expense["description"] == "Pizza"
    assert new_expense["amount"] == 35.50
    assert new_expense["category"] == "Food"


def test_get_expenses(tmp_path):
    database_path = tmp_path / "test_expenses.db"

    create_tables(database_path)

    insert_expense("Pizza", 35.50, "Food", database_path)
    insert_expense("Bus ticket", 8.80, "Transport", database_path)
    expenses = get_expenses(database_path)

    assert len(expenses) == 2
    assert expenses[0]["id"] == 1
    assert expenses[0]["description"] == "Pizza"
    assert expenses[0]["amount"] == 35.50
    assert expenses[0]["category"] == "Food"

    assert expenses[1]["id"] == 2
    assert expenses[1]["description"] == "Bus ticket"
    assert expenses[1]["amount"] == 8.80
    assert expenses[1]["category"] == "Transport"


def test_get_existing_expense_by_id(tmp_path):
    database_path = tmp_path / "test_expenses.db"
    create_tables(database_path)

    new_expense = insert_expense(
        "Pizza",
        35.50,
        "Food",
        database_path
    )

    expense_id = new_expense["id"]

    expense_by_id = get_expense_by_id(expense_id, database_path)
    assert expense_by_id is not None
    assert expense_by_id["description"] == "Pizza"


def test_get_expense_by_non_existing_id(tmp_path):
    database_path = tmp_path / "test_expenses.db"
    create_tables(database_path)

    non_existing_expense = get_expense_by_id(999, database_path)
    assert non_existing_expense is None


def test_delete_existing_expense(tmp_path):
    database_path = tmp_path / "test_expenses.db"
    create_tables(database_path)

    created_expense = insert_expense("Coffee", 9.99, "Food", database_path)
    expense_id = created_expense["id"]

    result = delete_expense(expense_id, database_path)
    assert result is True

    none_expense = get_expense_by_id(expense_id, database_path)
    assert none_expense is None


def test_delete_non_existing_expense(tmp_path):
    database_path = tmp_path / "test_expenses.db"
    create_tables(database_path)

    result = delete_expense(999, database_path)
    assert result is False


def test_update_existing_expense(tmp_path):
    database_path = tmp_path / "test_expenses.db"
    create_tables(database_path)
    
    created_expense = insert_expense("Coffee", 9.99, "Food", database_path)
    expense_id = created_expense["id"]

    updated_expense = update_expense(expense_id, "UpdatedCoffee", 5.99, "UpdatedFood", database_path)

    assert updated_expense["id"] == expense_id
    assert updated_expense["description"] == "UpdatedCoffee"
    assert updated_expense["amount"] == 5.99
    assert updated_expense["category"] == "UpdatedFood"


def test_update_non_existing_expense(tmp_path):
    database_path = tmp_path / "test_expenses.db"
    create_tables(database_path)

    updated_expense = update_expense(999, "UpdatedCoffee", 5.99, "UpdatedFood", database_path)

    assert updated_expense is None


def test_get_expense_summary(tmp_path):
    database_path = str(tmp_path / "test.db")
    create_tables(database_path)

    insert_expense("Coffee", 4.50, "Food", database_path)
    insert_expense("Lunch", 12.00, "Food", database_path)
    insert_expense("Bus ticket", 3.40, "Transport", database_path)

    summary = get_expense_summary(database_path)

    assert summary["total_spent"] == 19.90
    assert summary["expense_count"] == 3
    assert summary["average_expense"] == pytest.approx(19.90 / 3)