# Todo Service API

A simple Todo Service API built using Python and FastAPI.

## Features

- Get all todos
- Get a todo by ID
- Create a new todo
- Update a todo
- Delete a todo
- Mark a todo as completed
- Search todos
- Get todo statistics
- Basic input validation

## Tech Stack

- Python
- FastAPI
- Pydantic
- JSON

## Project Structure

```text
todo-service/
│
├── main.py
├── models.py
├── storage.py
├── todos.json
├── requirements.txt
└── .gitignore


How to Run
First, activate the virtual environment and install the required packages.
pip install -r requirements.txt
Then start the FastAPI server:

uvicorn main:app --reload
The API documentation can be opened at:
http://127.0.0.1:8000/docs


Data Storage

The Todo data is stored in a local todos.json file.
No database is used in this project.

API Endpoints
Method	  Endpoint	                   Description
GET       	/todos	                    Get all todos
GET	    /todos/{todo_id}	               Get a todo by ID
POST	       /todos	                      Create a todo
PUT      	/todos/{todo_id}	               Update a todo
PATCH	    /todos/{todo_id}/complete   	   Update completion status
DELETE   	/todos/{todo_id}	                 Delete a todo

