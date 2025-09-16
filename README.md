
# Gold Shop - Backend API

This directory contains the backend API for the Gold Shop Management System. It is a modern, high-performance API built with Python and FastAPI.

## Features

-   **Modern Framework:** Built with [FastAPI](https://fastapi.tiangolo.com/) for high performance and automatic interactive documentation.
    
-   **Clean Architecture:** Follows a clean, service-oriented architecture with a clear separation of concerns (API, Services, Repositories, Models).
    
-   **Database:** Uses [PostgreSQL](https://www.postgresql.org/) with [SQLAlchemy](https://www.sqlalchemy.org/) as the ORM.
    
-   **Migrations:** Database schema changes are managed with [Alembic](https://alembic.sqlalchemy.org/).
    
-   **Authentication:** Secure JWT-based authentication with password hashing.
    
-   **Dependency Management:** Project dependencies are managed with [Poetry](https://python-poetry.org/).
    

## Local Development Setup

These instructions assume you are running the database and Redis services from the root `CaptainDock` directory using `make up-dev`.

1.  **Prerequisites:**
    
    -   Python 3.11+
        
    -   [Poetry](https://www.google.com/search?q=https://python-poetry.org/docs/%23installation)
        
2.  **Navigate to the Backend Directory:** All commands should be run from within this `backend` directory.
    
    ```
    cd backend
    
    ```
    
3.  **Install Dependencies:** Poetry will create a virtual environment and install all the required packages from the `pyproject.toml` file.
    
    ```
    poetry install
    
    ```
    
4.  **Run the Server:** This command starts the Uvicorn server with hot-reloading enabled, which is ideal for development.
    
    ```
    poetry run uvicorn app.main:app --reload
    
    ```
    
    The API will now be running.
    
    -   **API URL:**  `http://localhost:8000`
        
    -   **Interactive Docs (Swagger UI):**  `http://localhost:8000/docs`
        

## Project Structure

The application code is located in the `app/` directory and follows a logical structure:

-   `app/api/`: Contains the API endpoints (routers). Logic is further split into `v1/` for versioning.
    
-   `app/core/`: Core application settings, security utilities, and exception handling.
    
-   `app/db/`: Database session management and the base model configuration.
    
-   `app/models/`: SQLAlchemy database models, defining the table structures.
    
-   `app/repository/`: The repository layer, responsible for all direct database communication.
    
-   `app/schema/`: Pydantic schemas, used for data validation and serialization (API request/response shapes).
    
-   `app/services/`: The service layer, containing all business logic.
    
-   `seeding/`: Contains logic and data for seeding the database with required initial data on startup.
    
-   `scripts/`: Contains standalone utility scripts for administrative tasks (e.g., creating an admin, seeding demo data).
    

## Database Migrations (Alembic)

Alembic is used to manage all changes to the database schema. **All migration commands should be run from the `CaptainDock` root directory using `make`**.

### The Workflow

When you need to make a change to a database table:

1.  **Edit the Model:** Modify the corresponding model file in `app/models/`. For example, add a new column to `app/models/user.py`.
    
2.  **Generate a Migration Script:** Run the `db-migrate` command. Alembic will compare your models to the database and automatically generate a new script in the `alembic/versions/` folder.
    
    ```
    make db-migrate
    
    ```
    
3.  **Apply the Migration:** Run the `db-upgrade` command to apply the new script to your development database.
    
    ```
    make db-upgrade
    
    ```
    
4.  **Revert a Migration (if needed):** To undo the last migration, you can run:
    
    ```
    make db-downgrade
    
    ```
    

## Local Utilities

The following `make` commands (run from the `CaptainDock` root) are available to manage your local development database:

-   `make create-admin`: Runs an interactive script to create a new admin user.
    
-   `make seed-db`: Populates the database with realistic sample data for demo purposes.
    
-   `make truncate-db`: **DANGEROUS!** Deletes all data from all tables and recreates the schema.