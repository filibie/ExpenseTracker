from app.visualizations import (
    plot_monthly_expenses,
    plot_expenses_by_category,
)


def test_plot_monthly_expenses_creates_file(tmp_path):
    output_path = tmp_path / "monthly.png"

    plot_monthly_expenses(
        {
            "2026-08": 120.50,
            "2026-09": 245.75,
            "2026-10": 182.25,
        },
        str(output_path),
    )

    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_plot_expenses_by_category_creates_file(tmp_path):
    output_path = tmp_path / "categories.png"

    plot_expenses_by_category(
        {
            "Food": 120.00,
            "Transport": 45.00,
            "Entertainment": 80.00,
        },
        str(output_path),
    )

    assert output_path.exists()
    assert output_path.stat().st_size > 0
