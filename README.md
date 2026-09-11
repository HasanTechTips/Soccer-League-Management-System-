# Soccer League Management System

A Flask and SQLite web application for managing a La Liga-style soccer league.

It provides player search and CRUD operations, database setup scripts, league standings, goalkeeper statistics, stadium match totals, assist comparisons, and coach reports.

## Run locally

```bash
pip install flask
python app.py
```

Open `http://127.0.0.1:5000`, then use the database actions to create and populate the sample data.

## Project files

- `app.py` - Flask application and database queries
- `01_drop_tables.sql`, `02_create_tables.sql`, `03_populate_tables.sql` - SQLite database scripts
- `templates/` and `static/` - web interface
