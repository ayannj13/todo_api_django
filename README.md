# ToDo API (Django REST Framework)

This is a simple **Task Management API (ToDo list)** which is built with **Django REST Framework**. It lets users to register and login to manage their tasks with the CRUD operations. Here, JWT tokens handle authentication, and every user can only manage their own tasks.

## Features of the system
- User model with `username`, `first_name`, `last_name`, and password.
- Task model with `title`, `description`, `status` (status can be: `NEW`, `IN_PROGRESS`, `COMPLETED`).
- CRUD operations for tasks:
  - List all tasks (only authenticated users).
  - List only your tasks.
  - View details of a task.
  - Create a new task.
  - Update task (only owner).
  - Delete task (only owner).
- Mark task as completed (extra endpoint).
- Filter tasks by status (`?status=NEW` or etc.).
- Pagination on task list.
- JWT authentication and authorization. (users must log in with to get a token, it's required for API requests.)
- PostgreSQL database support.

## Installation guide

1. **Clone the repository**:
   git clone https://github.com/ayannj13/todo_api_django.git
   cd todo_api_django

2. **Create virtual environment and install the requirements from txt file**:
   python3 -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate      # Windows

This project uses a simple `requirements.txt` so anyone can install the needed Python packages with one command.
After activating your virtualenv run this command to install the needed packages:

   pip install -r requirements.txt 

Note: PostgreSQL server itself is not a Python package, so it’s not listed here. Install PostgreSQL on your machine separately. The psycopg[binary] line above is the Python driver that lets Django connect to PostgreSQL.

3. **Configure database (PostgreSQL)**:
   Open todo_project/settings.py. Update the DATABASES section with your own PostgreSQL credentials.
   For example:
   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'todo_db',
        'USER': 'your_postgres_username', #put your own postgres username
        'PASSWORD': 'your_postgres_password', #put your own postgres password
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
4. **Run the migrations**:
   python manage.py migrate

5. **Create a superuser (admin)**:
   python manage.py createsuperuser

6. **Start the server**:
   python manage.py runserver
Here, API will be available at: http://127.0.0.1:8000/api/ 
and Admin panel: http://127.0.0.1:8000/admin/

## Run with Docker

**Prerequisite:** Install and run Docker Desktop.

1. **Copy env template and adjust values if needed**:
   cp .env.example .env

This creates your local `.env` file from the template.  
Update it with any custom values if it's needed (by default it will just work).

2. **Build & start**:
   docker compose up -d --build

3. **Create an admin inside the container**:
   docker compose exec web python manage.py createsuperuser

4. **Open**:
- API root: http://127.0.0.1:8000/api/
- Admin: http://127.0.0.1:8000/admin/

5. **Run tests inside the container (optional for checking)**:
   docker compose exec web python manage.py test api -v 2

6. **Stop**:
   docker compose down

## Authentication (JWT) and Registration

7. **Register (sign up)**  
Create a user account via the public endpoint:

   curl -X POST http://127.0.0.1:8000/api/register/ \
   -H "Content-Type: application/json" \
   -d '{"username":"your_user","first_name":"Your","last_name":"Name","password":"your_pass"}'

**You should consider that password must be 6+ characters. Also, it is write-only and never returned in responses.**

8. **Get a JWT token by sending username/password**:
   curl -X POST http://127.0.0.1:8000/api/token/ \
   -H "Content-Type: application/json" \
   -d '{"username": "your_user", "password": "your_pass"}' #give username and password in the respective fields.

The response will be shown as an access and refresh token. 

9. **Copy the value of "access" and export it as TOKEN**:
Export your token once so you don’t need to paste it every time:

   export TOKEN='put the access token here.'

Now you can use **$TOKEN** in all requests given below.

Note: If you log in as another user and want to get another token, you can give them different names and use them in the requests.

## API Endpoints
All requests (except login) require an **access token**. Replace `$TOKEN` with your exported token.  
Also, when needed, replace `<task_id>` with the ID of the corresponding task (for example `1`). 

**Task Endpoints**

1. **List all the tasks**:
   curl http://127.0.0.1:8000/api/tasks/ \
  -H "Authorization: Bearer $TOKEN"

2. **List only my tasks**:
   curl http://127.0.0.1:8000/api/tasks/my/ \
   -H "Authorization: Bearer $TOKEN"

3. **Create a new task**:
   curl -X POST http://127.0.0.1:8000/api/tasks/ \
   -H "Authorization: Bearer $TOKEN" \
   -H "Content-Type: application/json" \
   -d '{"title": "Buy milk", "description": "2L semi-skimmed"}'

4. **Get task details**:
   curl http://127.0.0.1:8000/api/tasks/<task_id>/ \
   -H "Authorization: Bearer $TOKEN"

For example, getting details of task with ID= 1:
   curl http://127.0.0.1:8000/api/tasks/1/ 
   -H "Authorization: Bearer $TOKEN"

5. **Update a task (task owner only)**:
   curl -X PATCH http://127.0.0.1:8000/api/tasks/<task_id>/ \
   -H "Authorization: Bearer $TOKEN" \
   -H "Content-Type: application/json" \
   -d '{"title": "Buy milk and bread"}'

6. **Deleting a task (task owner only)**:
   curl -X DELETE http://127.0.0.1:8000/api/tasks/<task_id>/ \
   -H "Authorization: Bearer $TOKEN"

7. **Mark as completed**:
   curl -X POST http://127.0.0.1:8000/api/tasks/<task_id>/complete/ \
   -H "Authorization: Bearer $TOKEN"

8. **Filtering tasks by status**:
   curl "http://127.0.0.1:8000/api/tasks/?status=COMPLETED" \
   -H "Authorization: Bearer $TOKEN"

9. **Pagination (automatic)**:
When listing tasks, results are paginated by default. You’ll see fields like `count`, `next`, and `previous`.  
To get the next page of tasks, follow the URL in the `"next"` field.
For example:
   curl "http://127.0.0.1:8000/api/tasks/?page=2" \
   -H "Authorization: Bearer $TOKEN"
This will return the second page of tasks.

## Running Tests

Run all the unit tests with:

   python manage.py test api -v 2

Run a specific test file:

   python manage.py test api.tests.test_create_task -v 2 

Replace test_create_task with any test file inside api/tests.

**Notes**

Admin users can log in at /admin/ and see all users and tasks. Normal users can interact with the system only through the API endpoints.

JWT tokens expire, so if your access token expires, you don’t need to log in again. 
Use the refresh token:

   curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
   -H "Content-Type: application/json" \
   -d '{"refresh": "<refresh_token>"}'

This will return a new access token which you can export again as $TOKEN. 
