# CheckIT — Django To‑Do Application

A lightweight, server-rendered task manager built with Django and Bootstrap.

This repository provides a small personal task tracking app with per-user tasks, steps (subtasks), a dashboard, and sensible validations.

## Features
- User signup, login and logout (session authentication)
- Per-user Task CRUD (create, list, view detail, edit, delete)
- Task steps with per-step completion and automatic progress calculation
- Dashboard with quick-create widget and recent tasks
- Server-side validation to prevent due dates in the past
- Mobile-friendly server-rendered UI using Bootstrap 5

## Tech stack
- Django with python 3.10.11 
- SQLite (data)
- Bootstrap 5 (CDN)

## Quick start (Windows / PowerShell)
1. Create and activate a virtual environment (recommended):
python -m venv .venv
source venv\Scripts\Activate


2. Install dependencies:
pip install -r requirements.txt


3. Prepare the database and run migrations:
python manage.py makemigrations
python manage.py migrate


4. Create a superuser to access Django admin:
python manage.py createsuperuser

5. Run the development server:
python manage.py runserver


6. Open http://127.0.0.1:8000/ in your browser.


