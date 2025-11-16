# Task Manager Project (FastAPI + SQLite + CLI)

This is a small Task Management system.  
It has two parts:

1. **FastAPI backend** → for creating and managing tasks  
2. **CLI tool (command line)** → to use the task system from terminal

I tried to keep the project very simple and easy to understand.

---

# Setup Instructions

Follow these steps one by one.

## 1. Clone or Download the Project
Go to the folder where you want to keep the project.
Open terminal of root folder and paste this command
``` git clone <repo_link> ```

## 2. Create Virtual Environment

### Windows
```
python -m venv venv 
venv\Scripts\activate
```

If you face 'script is disabled in this system' error then run this command
```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
``` 

### Mac / Linux
```
python3 -m venv venv
source venv/bin/activate
```

## 3. Installed required packages
```
pip install -r requirements.txt
```

## 4. Run the FastAPI Server
Start the backend: 
```uvicorn app.main:app --reload```


If it starts successfully, API will be available here:

**http://localhost:8000**

## 5. Check API Documentation
FastAPI provides docs automatically:

**http://localhost:8000/docs**

This page shows all the API endpoints and you can also test them from the browser.

---

# API Endpoints (Basic Overview)

| Method | Endpoint                     | Description |
|--------|------------------------------|-------------|
| POST   | `/tasks`                     | Create a new task |
| GET    | `/tasks`                     | List all tasks (with filters) |
| GET    | `/tasks/{task_id}`           | Get a single task by ID |
| PUT    | `/tasks/{task_id}`           | Update a task |
| PATCH  | `/tasks/{task_id}/status`    | Change task status (open/completed) |
| DELETE | `/tasks/{task_id}`           | Delete a task |

You can try all of these inside `http://localhost:8000/docs`.

---

# CLI Usage (Command Line Tool)

Open a new terminal (keep the API running).  
Make sure the virtual environment is active.

Use the CLI like this:
```python cli/cli.py <command>```

Below are all commands with examples.

---

### 1. Create a task
```python cli/cli.py create "Buy milk" --desc "2 liters" --priority low --due 2025-12-01```

### 2. List all task
```python cli/cli.py list```

### 3. List task by status
```python cli/cli.py list --status open```
```python cli/cli.py list --status completed```

### 4. List task by priority
```python cli/cli.py list --priority high```

### 5. List task by due date filter
```python cli/cli.py list --due-before 2025-12-10```
```python cli/cli.py list --due-after 2025-11-01```

### 6. Get a single task by id
```python cli/cli.py get 1```

### 7. Update a task
```python cli/cli.py update 1 --title "Buy almond milk" --priority medium --due 2025-12-05```

### 8. Mark task as completed
```python cli/cli.py complete 1```

### 9. Reopen a task (Mark as open)
```python cli/cli.py reopen 1```

### 10. Delete a task
```python cli/cli.py delete 1```


---

# Assumptions Made

- I used **SQLite** because it is easy and does not need installation.
- The database is saved in a file called **tasks.db** in the project folder.
- Date format used is always **YYYY-MM-DD**.
- Priority values allowed are only:
  - `low`
  - `medium`
  - `high`
- Task status can be:
  - `open`
  - `completed`
- The CLI always talks to API running on `http://localhost:8000` unless user gives another URL.
- No authentication/login is added to keep the project simple.
- This project is made for learning how API + CLI + database work together.

---

# Thank You
