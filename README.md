# Smart Task Management System

A full-stack, responsive Task Management application built with a modern Neo-Brutalism design aesthetic. Features include secure user authentication, a RESTful API, real-time WebSocket updates, PostgreSQL database integration, and an analytics module powered by Pandas and NumPy.

## Features

- **Authentication**: Secure registration, login, and session-based auth.
- **REST APIs**: Complete CRUD operations for tasks.
- **PostgreSQL**: Relational storage for users and tasks.
- **Analytics Module**: Uses Pandas and NumPy to dynamically calculate total, completed, pending, and completion percentage.
- **Real-Time Updates**: Uses Flask-SocketIO to update the task board dynamically without page reloads.
- **Neo-Brutalism UI**: Clean, striking, responsive frontend built with HTML and CSS.

---

## Setup Instructions

### 1. Prerequisites

- **Python 3.8+**
- **PostgreSQL** installed and running on your local machine.

### 2. Database Setup

1. Open your PostgreSQL terminal (e.g., `psql` or pgAdmin).
2. Create a new database for the application:
   ```sql
   CREATE DATABASE task_management_db;
   ```

### 3. Application Setup

1. Open your terminal in the project root directory (`Task_Management`).
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On Mac/Linux: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Update the `.env` file with your actual PostgreSQL username and password.

### 4. Initialize the Database

Open a Python shell inside the virtual environment to create the database tables:
```bash
python
```
```python
from app import create_app
from extensions import db

app = create_app()
with app.app_context():
    db.create_all()
    print("Database tables created!")
exit()
```

### 5. Run the Application

Start the Flask application with SocketIO support:
```bash
python app.py
```
The application will run at `http://127.0.0.1:5000`.

---

## Sample API Requests

If you wish to test the APIs using tools like Postman or cURL, ensure you first log in via the browser to establish a session, or use an API testing tool that stores session cookies.

**Add a Task (POST /api/tasks):**
```json
{
    "title": "Learn WebSockets",
    "description": "Read documentation on Flask-SocketIO.",
    "priority": "High",
    "status": "Pending"
}
```

**Get All Tasks (GET /api/tasks):**
Returns an array of tasks for the authenticated user.

**Update a Task (PUT /api/tasks/<id>):**
```json
{
    "status": "Completed"
}
```

**Delete a Task (DELETE /api/tasks/<id>):**
No body required.
