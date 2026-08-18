# Task Manager API

A production-ready Django REST Framework backend API for managing tasks with user authentication, JWT-based security, and comprehensive task management features. Built with PostgreSQL and designed for containerized deployment.

## ✨ Features

### Authentication & User Management

- **User Registration** — Create new user accounts with username, email, phone number, and age
- **JWT Authentication** — Secure token-based authentication using djangorestframework-simplejwt
- **Token Refresh** — Refresh expired access tokens without re-authentication
- **Custom User Model** — Extended user model with optional phone and age fields

### Task Management

- **Full CRUD Operations** — Create, read, update, and delete tasks with RESTful endpoints
- **Task Ownership** — Tasks are automatically associated with the authenticated user
- **Status Tracking** — Track task progress with pending and completed statuses
- **Priority Levels** — Support for high, medium, and low priority tasks
- **Due Date Management** — Set optional due dates with validation (prevents past dates)
- **Overdue Detection** — Automatic detection of overdue pending tasks
- **Soft Delete** — Tasks are archived rather than permanently removed

### Advanced Capabilities

- **Pagination** — Results are paginated with 3 items per page for optimal performance
- **Filtering** — Filter tasks by status and priority
- **Full-Text Search** — Search task titles and descriptions
- **Ordering** — Sort tasks by creation date or title
- **Admin Interface** — Django admin panel for system management
- **Docker Support** — Containerized deployment with Gunicorn and PostgreSQL

## 🛠️ Tech Stack

| Component      | Technology                    | Version             |
| -------------- | ----------------------------- | ------------------- |
| Framework      | Django                        | 5.2.14              |
| API            | Django REST Framework         | 3.17.1              |
| Authentication | djangorestframework-simplejwt | 5.5.1               |
| Database       | PostgreSQL                    | (via psycopg 3.3.4) |
| Server         | Gunicorn                      | Latest              |
| Language       | Python                        | 3.12+               |

**Key Dependencies:**

- **django-filter** — Advanced filtering and querying capabilities
- **whitenoise** — Efficient static file serving
- **python-decouple** — Environment variable management
- **PyJWT** — JWT token handling

## 📁 Project Structure

```
task_manager_api/
├── task_manager/              # Django project configuration
│   ├── settings.py           # Project settings and app configuration
│   ├── urls.py               # Main URL routing
│   ├── wsgi.py               # WSGI application entry point
│   └── asgi.py               # ASGI application entry point
│
├── users/                     # User authentication & management
│   ├── models.py             # CustomUser model with phone and age
│   ├── views.py              # Registration and login endpoints
│   ├── serializers.py        # User data serialization
│   ├── urls.py               # User app routes
│   ├── migrations/           # Database migrations
│   └── admin.py              # Django admin configuration
│
├── tasks/                     # Task management module
│   ├── models.py             # Task model with status and priority
│   ├── views.py              # Task CRUD endpoints (ViewSet)
│   ├── serializers.py        # Task data serialization
│   ├── pagination.py         # Pagination configuration
│   ├── urls.py               # Task app routes
│   ├── migrations/           # Database migrations
│   └── admin.py              # Django admin configuration
│
├── Dockerfile                 # Docker image configuration
├── docker-compose.yaml        # Docker Compose multi-container setup
├── requirements.txt           # Python dependencies
├── manage.py                  # Django management CLI
└── README.md                  # This file
```

## 🚀 Getting Started

### Prerequisites

- **Python** 3.12 or higher
- **PostgreSQL** database server
- **pip** and **venv** for dependency management
- **Docker** and **Docker Compose** (optional, for containerized deployment)

### Installation

1. **Navigate to the project directory:**

   ```bash
   cd task_manager_api
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables** (create a `.env` file in the project root):

   ```env
   DB_NAME=task_manager_db
   DB_USER=postgres
   DB_PASSWORD=your_secure_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. **Run database migrations:**

   ```bash
   python manage.py migrate
   ```

6. **(Optional) Create a superuser for admin access:**

   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server:**

   ```bash
   python manage.py runserver
   ```

   The API will be available at `http://localhost:8000/`

### Docker Deployment

Deploy the application using Docker Compose:

```bash
docker-compose up --build
```

This will:

- Start a PostgreSQL database container
- Build and run the Django application container
- Automatically run migrations
- Expose the API on port 8000

## ⚙️ Configuration

Database configuration is managed via environment variables in `task_manager/settings.py`:

- `DB_NAME` — PostgreSQL database name
- `DB_USER` — PostgreSQL user
- `DB_PASSWORD` — PostgreSQL password
- `DB_HOST` — Database host (default: localhost)
- `DB_PORT` — Database port (default: 5432)

The `AUTH_USER_MODEL` is set to `users.CustomUser` for extended user functionality.

## 📡 API Endpoints

### Authentication Endpoints

| Method | Endpoint              | Description                          |
| ------ | --------------------- | ------------------------------------ |
| `POST` | `/register/`          | Register a new user account          |
| `POST` | `/login/`             | Login and receive JWT tokens         |
| `POST` | `/api/token/`         | Obtain JWT access and refresh tokens |
| `POST` | `/api/token/refresh/` | Refresh an expired access token      |

**Register Request Example:**

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password",
  "phone": "+1234567890",
  "age": 28
}
```

**Login Response Example:**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

### Task Management Endpoints

| Method   | Endpoint       | Description                           |
| -------- | -------------- | ------------------------------------- |
| `GET`    | `/tasks/`      | List all tasks for authenticated user |
| `POST`   | `/tasks/`      | Create a new task                     |
| `GET`    | `/tasks/{id}/` | Retrieve a specific task              |
| `PUT`    | `/tasks/{id}/` | Update an entire task                 |
| `PATCH`  | `/tasks/{id}/` | Partially update a task               |
| `DELETE` | `/tasks/{id}/` | Soft delete a task                    |

**Create Task Request Example:**

```json
{
  "title": "Complete project documentation",
  "description": "Write comprehensive API documentation",
  "status": "pending",
  "priority": "high_priority",
  "due_date": "2026-12-31"
}
```

**Task Response Example:**

```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive API documentation",
  "status": "pending",
  "priority": "high_priority",
  "due_date": "2026-12-31"
}
```

### Query Parameters for Task Listing

| Parameter  | Values                                                     | Example                   |
| ---------- | ---------------------------------------------------------- | ------------------------- |
| `status`   | `pending`, `completed`                                     | `?status=pending`         |
| `priority` | `high_priority`, `medium_priority`, `low_priority`         | `?priority=high_priority` |
| `search`   | Any text                                                   | `?search=documentation`   |
| `ordering` | `created_at`, `title` or `-created_at`, `-title` (reverse) | `?ordering=-created_at`   |

**Example Query:**

```
GET /tasks/?status=pending&priority=high_priority&search=documentation&ordering=-created_at
```

## 🔐 Authentication

All task management endpoints require JWT authentication. Include the access token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

## 📝 Task Model Details

### Status Choices

- `pending` — Task is not yet completed
- `completed` — Task has been completed

### Priority Levels

- `high_priority` — High priority task
- `medium_priority` — Medium priority task (default)
- `low_priority` — Low priority task

### Properties

- **id** — Unique task identifier
- **title** — Task title (max 200 characters)
- **description** — Task description (max 400 characters)
- **status** — Current status (pending or completed)
- **priority** — Task priority level
- **due_date** — Optional due date (cannot be in the past)
- **is_overdue** — Auto-detected property indicating if task is past due and not completed
- **is_deleted** — Soft delete flag (false by default)
- **created_at** — Timestamp when task was created
- **updated_at** — Timestamp of last update

## 🧪 Testing

Run the test suite:

```bash
python manage.py test
```

Test specific apps:

```bash
python manage.py test users          # Test user authentication
python manage.py test tasks          # Test task management
```

## 📚 Development Notes

- **Custom User Model**: The `CustomUser` model extends Django's `AbstractUser` with phone number and age fields
- **JWT Tokens**: Access tokens expire after a set period; use refresh tokens to obtain new access tokens
- **Soft Deletes**: Deleted tasks are marked with `is_deleted=True` rather than removed from the database
- **Pagination**: All task listings return paginated results with 3 items per page
- **Overdue Calculation**: A task is overdue if its `due_date` is before today and its status is not completed
- **Due Date Validation**: The API prevents setting due dates in the past

## 🚨 Production Considerations

Before deploying to production:

1. **Set `DEBUG = False`** in `task_manager/settings.py`
2. **Configure `ALLOWED_HOSTS`** with your domain names
3. **Use environment-specific settings** for database credentials and secrets
4. **Enable HTTPS/SSL** for all API communications
5. **Implement rate limiting** to prevent abuse
6. **Set up proper logging** and error monitoring
7. **Use a production-grade database** with backups enabled
8. **Configure CORS settings** based on your frontend domain

## 📄 License

No license is currently included. Please add an appropriate license file (e.g., MIT, Apache 2.0) if you plan to publish or share this project.

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Create a feature branch from `main`
2. Implement your changes with clear commit messages
3. Add tests for new functionality
4. Ensure all tests pass before submitting a pull request
5. Update this README with any new features or changes

## 📞 Support

For issues, questions, or contributions, please open an issue in the repository.
