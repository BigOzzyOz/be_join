# Backend Join

A Django-based backend for managing tasks, contacts, and user authentication. This project provides a REST API for a task management application, designed to work with its corresponding [Join Frontend application](https://github.com/BigOzzyOz/join). It includes user registration, login, and contact management.

## Features
- User authentication (registration, login, guest login)
- Task management with priorities, categories, and subtasks
- Contact management with profile pictures and initials
- REST API with token authentication
- Admin interface for managing all data
- Comprehensive test suite

## Repositories
- **Backend (this project):** [https://github.com/BigOzzyOz/be_join](https://github.com/BigOzzyOz/be_join)
- **Frontend:** [https://github.com/BigOzzyOz/join](https://github.com/BigOzzyOz/join)

## Requirements
- Python 3.10+
- Django 5.x
- djangorestframework
- django-cors-headers
- MySQL (for production) or SQLite (for development/testing)

## Installation
1. **Clone the repository:**
   ```sh
   git clone https://github.com/BigOzzyOz/be_join.git
   cd be_join
   ```
2. **Create a virtual environment:**
   ```sh
   python -m venv env
   env\Scripts\activate  # On Windows
   ```
3. **Copy the example.env file:**
   ```sh
   copy example.env .env  # On Windows
   # or
   cp example.env .env    # On Linux/Mac
   ```
   Edit the `.env` file and set your own values for SECRET_KEY, database credentials, etc.
4. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
5. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```
6. **Create a superuser (optional, for admin access):**
   ```sh
   python manage.py createsuperuser
   ```
7. **Run the development server:**
   ```sh
   python manage.py runserver
   ```

## Frontend Application

This backend is designed to be used with the Join frontend application. You can find the frontend project and its setup instructions here:
- **Frontend Repository:** [https://github.com/BigOzzyOz/join](https://github.com/BigOzzyOz/join)

Make sure the frontend is configured to communicate with the API endpoints provided by this backend.

## Project Structure
- `backend_join/` – Django project settings and URLs
- `contacts_app/` – Contact management (models, API, signals, tests)
- `tasks_app/` – Task and subtask management (models, API, tests)
- `user_auth_app/` – User authentication and registration (API, signals, tests)
- `env/` – Python virtual environment (not included in version control)

## Usage
- **Admin interface:** [http://localhost:8000/admin/](http://localhost:8000/admin/)
- **API endpoints:**
  - Tasks: `/api/tasks/`
  - Contacts: `/api/contacts/`
  - Auth: `/auth/`

## API Endpoint Details

### Authentication
- `POST /auth/login/` – Obtain token with username and password
- `POST /auth/register/` – Register a new user and obtain token
- `POST /auth/guest/` – Obtain a guest token
- `GET /auth/status/` – Check authentication status

### Tasks
- `GET /api/tasks/` – List all tasks
- `POST /api/tasks/` – Create a new task
- `GET /api/tasks/{id}/` – Retrieve a specific task
- `PUT /api/tasks/{id}/` – Update a task
- `DELETE /api/tasks/{id}/` – Delete a task
- `GET /api/tasks/summary/` – Get a summary of tasks (counts by status, next urgent due, etc.)

### Contacts
- `GET /api/contacts/` – List all contacts
- `POST /api/contacts/` – Create a new contact
- `GET /api/contacts/{id}/` – Retrieve a specific contact
- `PUT /api/contacts/{id}/` – Update a contact
- `DELETE /api/contacts/{id}/` – Delete a contact

### Example: Authenticated Request
```sh
curl -H "Authorization: Token <your-token>" http://localhost:8000/api/tasks/
```

## Running Tests
```sh
python manage.py test
```

## Demo Data

To create demo contacts and tasks for local testing, run:

```sh
python manage.py shell
```
Then, in the shell:
```python
exec(open("seed_demo_data.py", encoding="utf-8").read())
```

If you encounter issues with the database or want to reset the demo data:
- Delete all contacts and tasks in the Django admin panel, or run:
  ```python
  from contacts_app.models import Contact
  from tasks_app.models import Task, Subtask
  Contact.objects.all().delete()
  Subtask.objects.all().delete()
  Task.objects.all().delete()
  ```
- Then re-run the seed script as above.

**Note:** Before running demo data scripts, make sure you have copied `example.env` to `.env` and adjusted the values for your environment.

This ensures you always have a clean set of demo data for local testing or presentation.

## License
MIT License

## Deployment (Production)

For production deployment (e.g., on a vServer), follow these steps:

1. **Create a .env file:**
   - Place a `.env` file in the project root (see `.example.env`).
   - Make sure the `SECRET_KEY` is in quotes if it contains special characters like `#`.
   - Set `DEBUG=False` and adjust `ALLOWED_HOSTS` for your domain.
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```
4. **Collect static files:**
   ```sh
   python manage.py collectstatic
   ```
5. **Start the server with Gunicorn (example):**
   ```sh
   gunicorn backend_join.wsgi:application
   ```
   (Alternatively: use uWSGI or another WSGI server)

**Notes:**
- The `.env` file should not be committed to version control (see `.gitignore`).
- Adjust database settings in `.env` for your environment.
- For local development, you can still use `python manage.py runserver`.

---
*Deployment section added on April 26, 2025*
