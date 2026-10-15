# ExpenseTracker

A simple REST API for tracking personal expenses, built with Python, FastAPI, and SQLite.

This project is a hands-on exercise in backend development, database operations, API design, and automated testing.

## Features

- Create new expenses
- Retrieve all expenses
- Retrieve a single expense by ID
- Update existing expenses
- Delete expenses
- Calculate expense statistics:
  - Total amount spent
  - Number of expenses
  - Average expense amount
- Return appropriate HTTP errors for expenses that don't exist
- Automated tests for database operations and API endpoints

## Tech Stack

- **Python 3.14+**
- **FastAPI** — REST API framework
- **SQLite** — database
- **Pydantic** — request data validation
- **pytest** — automated testing
- **HTTPX** — testing API endpoints

## Project Structure

```text
ExpenseTracker/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── database.py
├── tests/
│   ├── test_main.py
│   └── test_database.py
├── .gitignore
├── README.md
└── expenses.db
```

The database file is created locally when the application initializes or creates its tables.

## Getting Started

### 1. Clone the repository

```bash
git clone git@github.com:filibie/ExpenseTracker.git
cd ExpenseTracker
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Make sure your virtual environment uses Python 3.14 or newer.

### 3. Install dependencies

```bash
python -m pip install fastapi "uvicorn[standard]" pytest httpx
```

### 4. Run the application

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/expenses` | Retrieve all expenses |
| POST | `/expenses` | Create an expense |
| GET | `/expenses/{expense_id}` | Retrieve an expense by ID |
| PUT | `/expenses/{expense_id}` | Update an expense |
| DELETE | `/expenses/{expense_id}` | Delete an expense |
| GET | `/expenses/summary` | Retrieve expense statistics |

### Example: Create an expense

**Request**

```http
POST /expenses
Content-Type: application/json
```

```json
{
  "description": "Lunch",
  "amount": 12.00,
  "category": "Food"
}
```

A successful request returns HTTP `201 Created` and the created expense, including its database ID.

### Example: Retrieve expense statistics

**Request**

```http
GET /expenses/summary
```

Example response:

```json
{
  "total_spent": 19.9,
  "expense_count": 3,
  "average_expense": 6.633333333333333
}
```

The values above are illustrative. The actual response depends on the expenses stored in the database.

### Error handling

Requests for nonexistent expenses return HTTP `404 Not Found`.

Invalid request data is validated by FastAPI and Pydantic.

## Running Tests

Run the complete test suite:

```bash
python -m pytest -v
```

Run only database tests:

```bash
python -m pytest tests/test_database.py -v
```

Run only API tests:

```bash
python -m pytest tests/test_main.py -v
```

The tests cover database operations, API endpoints, and error handling.

## Database

ExpenseTracker uses SQLite to store expenses.

Each expense contains:

- `id` — unique identifier
- `description` — description of the expense
- `amount` — expense amount
- `category` — expense category

The database layer is separated from the API routes in `app/database.py`.

## Future Improvements

- Add expense dates and date-range filtering
- Add spending summaries grouped by category
- Improve validation for expense amounts and descriptions
- Add configuration for database paths
- Build a frontend for visualizing expenses

## License

MIT License