# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Setup

This is a Django project using Pipenv for dependency management.

1. Install dependencies:
   ```bash
   pipenv install
   ```

2. Activate the virtual environment:
   ```bash
   pipenv shell
   ```

3. Ensure the database is configured. The project uses Microsoft SQL Server by default (see `Storeapp/settings.py`). For local development, you can switch to SQLite by commenting out the MSSQL database block and uncommenting the SQLite block in `settings.py`.

## Common Commands

- Run the development server:
  ```bash
  python manage.py runserver
  ```

- Run migrations:
  ```bash
  python manage.py migrate
  ```

- Create a new migration after model changes:
  ```bash
  python manage.py makemigrations
  ```

- Run tests:
  ```bash
  python manage.py test
  ```

- Run a specific test app:
  ```bash
  python manage.py test game
  ```

- Collect static files (for production):
  ```bash
  python manage.py collectstatic
  ```

## Code Architecture

- **Project Structure**:
  - `Storeapp/` - Django project settings and configuration (`settings.py`, `urls.py`, `wsgi.py`, `asgi.py`)
  - `game/` - A Django app containing models, views, templates, and tests for the game functionality
  - `db.sqlite3` - Default SQLite database (can be replaced with MSSQL as configured)
  - `manage.py` - Django's command-line utility

- **Key Components**:
  - **Settings**: Configured for MSSQL database (Azure SQL) with specific connection details in `Storeapp/settings.py`. For local development, SQLite can be used by adjusting the `DATABASES` setting.
  - **URLs**: Root URL configuration in `Storeapp/urls.py` includes the game app's URLs.
  - **Templates**: Located in `game/templates/` (Django app-directories template loader).
  - **Static Files**: Served from `static/` directory (configured via `STATIC_URL`).

- **Dependencies**:
  - Django 6.0.5
  - mssql-django and pyodbc for SQL Server connectivity
  - See `Pipfile` and `requirements.txt` for full list.

## Testing

- Tests are written using Django's `TestCase` class.
- Test files are located in each app (e.g., `game/tests.py`).
- Run all tests with `python manage.py test`.
- The test database is automatically created and destroyed.

## Database

- Primary database: Microsoft SQL Server (Azure SQL) as configured in `settings.py`.
- For local development without Azure SQL, switch to SQLite by:
  1. Commenting out the MSSQL database block in `settings.py`.
  2. Uncommenting the SQLite block.
  3. Running `python manage.py migrate` to create the SQLite database.

## Deployment

- The project is configured for Azure App Service (see `CSRF_TRUSTED_ORIGINS` and `web.config`).
- Deployment typically involves pushing to Azure and ensuring the database connection string is set in the app settings.
