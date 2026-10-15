from app.database import (
    create_tables,
    insert_expense,
    get_expenses,
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