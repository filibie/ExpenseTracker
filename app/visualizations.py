import matplotlib.pyplot as plt


def plot_monthly_expenses(
    monthly_expenses: dict[str, float],
    output_path: str,
):
    months = list(monthly_expenses.keys())
    totals = list(monthly_expenses.values())

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.bar(months, totals)
    ax.set_title("Monthly Expenses", fontsize=16)
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount (PLN)")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def plot_expenses_by_category(
    category_expenses: dict[str, float],
    output_path: str,
):
    categories = list(category_expenses.keys())
    totals = list(category_expenses.values())

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.bar(categories, totals)
    ax.set_title("Expenses by Category", fontsize=16)
    ax.set_xlabel("Category")
    ax.set_ylabel("Amount (PLN)")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
