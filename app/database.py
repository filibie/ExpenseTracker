import sqlite3

DATABASE_PATH = "expenses.db"

def create_tables(database_path=DATABASE_PATH):
    connection = sqlite3.connect(database_path)
    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL DEFAULT '2026-01-01'
            )
        """)

        columns = connection.execute(
            "PRAGMA table_info(expenses)"
        ).fetchall()

        column_names = [column[1] for column in columns]

        if "date" not in column_names:
            connection.execute("""
                ALTER TABLE expenses
                ADD COLUMN date TEXT NOT NULL DEFAULT '2026-01-01'
            """)
        
        connection.commit()

    finally:
        connection.close()


def get_expenses(database_path=DATABASE_PATH):
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    try:
        expenses = connection.execute(
            """
            SELECT * FROM expenses ORDER BY id
            """
        ).fetchall()
    finally:
        connection.close()

    return [dict(row) for row in expenses]


def insert_expense(
        description: str, 
        amount: float, 
        category: str, 
        database_path=DATABASE_PATH,
        date: str = "2026-01-01",
    ) -> dict:
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.execute(
            """
            INSERT INTO expenses(description, amount, category, date)
            VALUES (?, ?, ?, ?)
            """,
            (description, amount, category, date),
        )

        connection.commit()

        expense = dict(
            connection.execute(
                "SELECT * FROM expenses WHERE id = ?",
                (cursor.lastrowid,),
            ).fetchone()
        )
        return expense
    
    finally:
        connection.close()


def get_expense_by_id(expense_id: int, database_path=DATABASE_PATH):
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    try:
        row = connection.execute(
            """
            SELECT * FROM expenses WHERE id = ?
            """,
            (expense_id,),
        ).fetchone()
    finally:
        connection.close()
    
    return dict(row) if row is not None else None


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


def get_expense_summary(database_path=DATABASE_PATH):
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    try:   
        row = connection.execute(
            """
            SELECT 
                SUM(amount) AS total_spent,
                COUNT(*) AS expense_count,
                AVG(amount) AS average_expense
            FROM expenses
            """
        ).fetchone()

    finally:
        connection.close()

    return {
        "total_spent": row["total_spent"] or 0,
        "expense_count" : row["expense_count"],
        "average_expense": row["average_expense"] or 0,
    }


def get_expenses_by_category(database_path=DATABASE_PATH):
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    try:   
        rows = connection.execute(
            """
            SELECT 
                category, 
                sum(amount) AS total_spent
            FROM expenses 
            GROUP BY category
            """
        ).fetchall()

    finally:
        connection.close()

    return {
        row["category"]: row["total_spent"]
        for row in rows
    }