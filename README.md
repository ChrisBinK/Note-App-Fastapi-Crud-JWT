# Note-App-Fastapi-Crud-JWT
This is a CRUD FastAPI application that allows users to create and manage notes. The API uses JWT for authentication.

Features: 
- Fastapi for serving API endpoints.
- Alembic  to handle database migrations
- pytestfor testing endpoints
- psycopg2-bin fro database connectivity.

### create a virtual environment 
- `pyhton3 -m venv venv`
 Navigate to the project directory:
- `cd note backend api`
Activate the virtual environment:
On Windows
- `.\venv\Scripts\activate`

On macOs/Linux
- `source venv/bin/activate` 

### Install dependencies
`pip install  -r requirements.txt`

### Database Setup and migrations
Run the following commands to set up the database. You need to create an .env file.
 - `alembic revision --autogenerate -m "Initialise the database tables"`
 - `alembic upgrade head`

### Run server
Start the PAI server by running this command.
- `unvicorn main:app --reload`
The API sercice should be running locally at `http:127.0.0.1:8000`

### To run the test
Run the test suite using:
- `pytest tests/`

### To test the API in the browser
FastAPI provides an interactive API documentation at 
- `http://127.0.0.1:8000/docs#/`

### API Authentication:
 Most API endpoints require authentication, except:
 - POST `api/users/` Create/Register a user
 - POST `api/users/token` Login to obtain  a JWT token, whic is requires for other endpoints in the app




