import matplotlib.pyplot as plt


def plot_monthly_expenses(monthly_expenses: dict[str, float], output_path: str):
    months = list(monthly_expenses.keys())
    totals = list(monthly_expenses.values())

    fig, ax = plt.subplots()

    ax.bar(months, totals)
    ax.set_title("Monthly Expenses")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount Spent")
    ax.tick_params(axis="x", rotation=45)

    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def plot_expenses_by_category(
    category_expenses: dict[str, float],
    output_path: str,
):
    categories = list(category_expenses.keys())
    totals = list(category_expenses.values())

    fig, ax = plt.subplots()

    ax.bar(categories, totals)
    ax.set_title("Expenses by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Amount Spent")
    ax.tick_params(axis="x", rotation=45)

    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
