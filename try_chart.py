from app.database import (
    get_monthly_expenses,
    get_expenses_by_category,
)
from app.visualizations import (
    plot_monthly_expenses,
    plot_expenses_by_category,
)

plot_monthly_expenses(
    get_monthly_expenses(),
    "monthly_expenses.png",
)

plot_expenses_by_category(
    get_expenses_by_category(),
    "category_expenses.png",
)

print("Both charts saved!")