# Helpdesk API

REST API for managing helpdesk incidents, users and authentication > Production-oriented REST API for helpdesk incident management.

The project has been developed with FastAPI and PostgreSQL, following a layered architecture and including authentication with JWT, data validation, automated tests, database migrations and Docker containerization.


## Features

- REST API for incident management
- CRUD operations for incidents
- Partial updates using PATCH
- Filtering incidents by different fields 
- Input validation with Pydantic
- PostgreSQL database
- SQLAlchemy 2.0 ORM
- JWT authentication
- Password hashing
- Protected endpoints
- Automated tests with Pytest
- Database migrations with Alembic
- Environment-based configuration
- Docker & Docker Compose support
- Automatic database initialization
- Automatic creation of demo users

## Technologies

| Technology        | Purpose |
|-------------------|---------|
| Python            | Programming language |
| FastAPI           | REST API framework |
| PostgreSQL        | Relational database |
| SQLAlchemy 2.0    | ORM |
| Pydantic          | Data validation |
| PyJWT             | JWT authentication |
| Bcrypt            | Password hashing |
| Pytest            | Automated testing |
| Alembic           | Database migrations |
| Docker            | Containerization |
| Docker Compose    | Container orchestration |

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | Authenticate user and obtain JWT |

### Incidents

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/incidents` | List incidents | Query Params
| GET | `/incidents/{id}` | Get an incident |
| POST | `/incidents` | Create an incident |
| PUT | `/incidents/{id}` | Replace an incident |
| PATCH | `/incidents/{id}` | Partially update an incident |
| DELETE | `/incidents/{id}` | Delete an incident |

⚠️⚠️For complete request and response schemas, use the Swagger documentation.⚠️⚠️


## Project Architecture

The project follows a layered architecture to separate responsibilities.

Client
   │
   ▼
Routers
   │
   ▼
Services
   │
   ▼
SQLAlchemy
   │
   ▼
PostgreSQL

## Project Structure

app/
├── auth/
├── crud/
├── routers/
├── services/
├── config.py
├── database.py
├── models.py
├── schemas.py
├── seed_tables.py
└── main.py

tests/
├── conftest.py
├── test_auth.py
└── test_incidents.py


alembic/
├── versions/
└── env.py

alembic.ini
Dockerfile
docker-compose.yml
requirements.txt
pyproject.toml

## Requirements

✅ Run the project using Docker:

- Docker
- Docker Compose

    
⚠️ The application uses environment variables for configuration. ⚠️

Create a `.env` file based on `.env.example`.



## Running API

1️⃣ **Clonar el repositorio:**

   ```bash
   git clone https://github.com/Rubb-hub/Helpdesk-API.git
   cd Helpdesk-API
   ```

2️⃣ **Create a `.env` file based on `.env.example`.

    ```bash
   cp .env.example .env
   ```
   
   ⚠️⚠️
   > Note: a \`.env.example\` file with sample values is included. Copy it to 
   > \`.env\` before running the project. It doesn't contain any real sensitive 
   > information, but this separation is kept as a good practice.


3️⃣ **Construir y levantar los contenedores:**

   ```bash
   docker-compose up --build 
   ```

    🚀Docker Compose starts:🚀

    - FastAPI application
    - PostgreSQL database

    💡 Database migrations are automatically applied during application startup. (Alembic/versions/cdd7e7da1f7e_initial_scheme-py)

    💡 Two users are automatically created during application startup. (App/seed_tables.py)


4️⃣ **The API will be available at:

    http://localhost:8000
    
    Swagger documentation:
    http://localhost:8000/docs
    


## Demo Users

    ✅ User:ExpAdmin / Pass:expadmin / Rol:Admin
    --> A user that always exists for testing purposes. These credentials are intended exclusively for demonstration purposes and must never be used in a production environment.

    ✅ User:Admin / Pass:*AutomaticGeneration / Rol:Admin 
    --> A user with a randomly generated password that is displayed only during this process. This simulates the realistic creation of a user as part of the migration.


## Authentication

⚠️ The API uses JWT Bearer authentication. ⚠️ 

**Step1
    Get Token -> 
        Post .../auth/login (JSON)

        Header: Content-Type / <application/json>

        {
                "user_login": "",
                "password": ""
        }

Response: ```text Authorization: Bearer <access_token> ```

**Step2
    Access Endpoint using correspond json and token from step1

    Header: Content-Type / <application/json>
            Authorization / Bearer <Token>   


## Testing

The project uses Pytest for automated testing.
-> All fixtures used in tests are located in conftest.py

Run all tests with:

    ```bash
    docker exec -it helpdesk-api pytest -v   
    ```

Tests cover, among other things:

- Authentication
- Incident creation
- Incident retrieval
- Incident update
- Partial updates
- Incident deletion
- Input validation
- Database persistence
- Error handling