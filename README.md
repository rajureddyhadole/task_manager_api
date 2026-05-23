# Task Manager Backend

A Django REST Framework backend for a task management application. This project provides user authentication, JWT-based security, and RESTful task management endpoints backed by PostgreSQL.

## Key Features

- User registration and login
- JWT authentication with access and refresh tokens
- Task creation, listing, editing, and deletion
- Custom user model via `users.CustomUser`
- Django REST Framework API endpoints

## Built With

- Django 5.2.14
- Django REST Framework 3.17.1
- djangorestframework-simplejwt 5.5.1
- python-decouple 3.8
- PostgreSQL via `psycopg` / `psycopg-binary`

## Project Structure

- `task_manager/` — Django project settings and URL routing
- `users/` — custom user model, registration, login, and JWT endpoints
- `tasks/` — task CRUD functionality and task-related API routes

## Prerequisites

- Python 3.10+
- PostgreSQL database server
- Virtual environment for Python dependencies

## Installation

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure database credentials using environment variables or a `.env` file:

```env
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
```

4. Apply database migrations:

```bash
python manage.py migrate
```

5. (Optional) Create a superuser:

```bash
python manage.py createsuperuser
```

6. Start the development server:

```bash
python manage.py runserver
```

## Configuration

The database configuration is defined in `task_manager/settings.py` and uses `python-decouple` to load `DB_NAME`, `DB_USER`, and `DB_PASSWORD`. The project is configured to use PostgreSQL on `localhost:5432`.

## API Endpoints

### Authentication

- `POST /register/` — register a new user
- `POST /login/` — login using the custom user authentication view
- `POST /api/token/` — obtain JWT access and refresh tokens
- `POST /api/token/refresh/` — refresh JWT access token

### Task Management

- `GET /tasks/` — list all tasks
- `POST /tasks/create/` — create a new task
- `PUT /tasks/edit/<task_id>/` — update an existing task
- `DELETE /tasks/delete/<task_id>/` — delete a task

## Testing

Run the Django test suite:

```bash
python manage.py test
```

## Notes

- `AUTH_USER_MODEL` is set to `users.CustomUser` in `task_manager/settings.py`
- JWT authentication is enabled through DRF with `rest_framework_simplejwt`
- `DEBUG` is currently enabled; switch to `False` for production deployments

## License

No license is included with this repository. Add a license file if you plan to publish or share the project.
