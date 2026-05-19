# ✓ FocusFlow

A clean, full-featured To-Do application built with Python and Flask.
Live demo: [focusflow.onrender.com](https://focusflow.onrender.com)

## Features

- Create, edit, and delete tasks
- Priority levels — High, Medium, Low with color coding
- Categories — Work, Personal, Dev, Health, and more
- Due date tracking with overdue detection
- Smart grouping — overdue tasks surface automatically
- Search across task titles and descriptions
- Filter by status, category, and due date
- Progress bar showing completion percentage
- Task detail pages
- Fully responsive — works on mobile and desktop

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Web Framework | Flask |
| Database | SQLite via Flask-SQLAlchemy |
| Templates | Jinja2 |
| Styles | Custom CSS |
| Deployment | Render |

## Run Locally

1. Clone the repository
   git clone https://github.com/YOUR_USERNAME/focusflow.git
   cd focusflow

2. Install dependencies
   pip install -r requirements.txt

3. Create a .env file
   SECRET_KEY=any-secret-key
   DATABASE_URL=sqlite:///focusflow.db

4. Run the app
   python run.py

5. Open http://127.0.0.1:5000 in your browser

## Project Structure

focusflow/
├── app/
│   ├── __init__.py      # App factory & context processor
│   ├── models.py        # Task database model
│   ├── routes.py        # URL routes & request handling
│   ├── db_utils.py      # Database query functions
│   ├── forms.py         # Form validation
│   ├── errors.py        # Custom error pages
│   ├── templates/       # HTML templates (Jinja2)
│   └── static/          # CSS
├── config.py            # App configuration
├── run.py               # Entry point
└── Procfile             # Deployment config

## What I Learned

- Flask application factory pattern
- SQLAlchemy ORM — models, queries, relationships
- POST → Validate → Redirect form pattern
- Jinja2 templating and template inheritance
- Context processors for global template data
- Partial templates for reusable components
- Production deployment with Gunicorn and WhiteNoise
- Environment variables for secret management
- Git and GitHub workflow