import sqlite3

DATABASE_PATH = "expenses.db"

def create_tables(database_path=DATABASE_PATH):
    connection = sqlite3.connect(database_path)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def get_expenses(database_path=DATABASE_PATH):
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    expenses = connection.execute(
        """
        SELECT * FROM expenses ORDER BY id
        """
    ).fetchall()

    connection.close()

    return [dict(row) for row in expenses]


def insert_expense(description: str, amount: float, category: str, database_path=DATABASE_PATH) -> dict:
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    cursor = connection.execute(
        """
        INSERT INTO expenses(description, amount, category)
        VALUES (?, ?, ?)
        """,
        (description, amount, category),
    )

    connection.commit()

    expense = dict(
        connection.execute(
            "SELECT * FROM expenses WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()
    )

    connection.close()
    return expense


def get_expense_by_id(expense_id: int, database_path=DATABASE_PATH):
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    row = connection.execute(
        """
        SELECT * FROM expenses WHERE id = ?
        """,
        (expense_id,),
    ).fetchone()

    connection.close()
    if row is not None:
        return dict(row)
    
    return None


def delete_expense(expense_id: int, database_path=DATABASE_PATH) -> bool:
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    cursor = connection.execute(
        """
        DELETE FROM expenses WHERE id = ?
        """,
        (expense_id,),
    )
    connection.commit()
    row_count = cursor.rowcount
    connection.close()

    return row_count > 0


def update_expense(
    expense_id: int,
    description: str,
    amount: float,
    category: str,
    database_path=DATABASE_PATH
    ) -> dict | None:
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    cursor = connection.execute(
        """
        UPDATE expenses 
        SET description = ?, amount = ?, category = ?
        WHERE id = ?
        """,
        (description, amount, category, expense_id,),
    )

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()
        return None

    updated_expense = get_expense_by_id(expense_id, database_path)
    connection.close()

    return updated_expense