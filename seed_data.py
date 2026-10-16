from datetime import date
import random

from app.database import create_tables, insert_expense

DATABASE_PATH = "expenses.db"

create_tables(DATABASE_PATH)

random.seed(42)

categories = {
    "Food": (8, 80),
    "Transport": (3, 30),
    "Entertainment": (15, 120),
    "Bills": (40, 250),
    "Shopping": (10, 150),
}

for month_offset in range(6):
    year = 2026
    month = 5 + month_offset

    if month > 12:
        year += 1
        month -= 12

    for _ in range(random.randint(8, 15)):
        category = random.choice(list(categories))
        min_amount, max_amount = categories[category]
        amount = round(random.uniform(min_amount, max_amount), 2)
        day = random.randint(1, 25)

        insert_expense(
            f"{category} expense",
            amount,
            category,
            DATABASE_PATH,
            date(year, month, day).isoformat(),
        )

print("Sample expenses added!")
