
# Gold Shop API - Backend Service

This is the backend service for the Gold Shop Management application, built with FastAPI. It provides a robust, documented, and secure RESTful API for all application data and business logic.

## ✨ Features

-   Modern, asynchronous framework using **FastAPI**.
    
-   **SQLAlchemy ORM** for database interaction.
    
-   **Pydantic** for robust data validation and serialization.
    
-   **Alembic** for safe and version-controlled database migrations.
    
-   **Poetry** for deterministic dependency management.
    
-   **JWT-based authentication** with a role and permission system.
    
-   Fully containerized for production with **Docker**.
    

## 🛠️ Local Development Setup

Follow these steps to run the backend service on your local machine for development.

### Prerequisites

-   Python 3.11+
    
-   [Poetry](https://www.google.com/search?q=https://python-poetry.org/docs/%23installation "null") for package management.
    
-   [Docker](https://www.docker.com/products/docker-desktop/ "null") and Docker Compose for running services.
    

### 1. Install Dependencies

Navigate to the `backend` directory and use Poetry to install all the required Python packages.

```
cd backend
poetry install

```

### 2. Start Dependent Services

The backend requires a PostgreSQL database and a Redis instance to run. The development Docker Compose setup handles this for you. From the **root `CaptainDock` directory**, run:

```
make up-dev

```

This will start the database and Redis containers in the background.

### 3. Run the FastAPI Server

Once the database container is running, you can start the FastAPI application. **In a new terminal**, navigate to the `backend` directory and run:

```
poetry run uvicorn app.main:app --reload

```

Your API will now be running at `http://localhost:8000` and will automatically restart whenever you make a code change. The interactive API documentation (Swagger UI) is available at `http://localhost:8000/docs`.

## 🗄️ Database Migrations (Alembic)

This project uses Alembic to manage database schema changes. It's like version control for your database.

### The Workflow

Never manually alter the database schema. Always follow this process:

1.  **Change a Model:** Make a change to a model file in `app/models/`. For example, add a new column to the `Contact` model.
    
2.  **Generate a Migration Script:** From the **root `CaptainDock` directory**, run:
    
    ```
    make db-migrate
    
    ```
    
    Alembic will compare your models to the database and generate a new script in `alembic/versions/`.
    
3.  **Apply the Migration:** To apply the new changes to your development database, run:
    
    ```
    make db-upgrade
    
    ```
    
4.  **Commit:** Commit both your model changes and the newly generated migration script to Git.
    

### Reverting a Migration (Development Only)

If you need to undo the last migration in your local development environment, you can run:

```
make db-downgrade

```

## ⚙️ Utilities

The `Makefile` in the root directory provides several useful commands for managing your local development database.

-   **Create an Admin User:**
    
    ```
    make create-admin
    
    ```
    
-   **Truncate the Database (DANGEROUS):** This will delete all data and reset the database to a clean slate.
    
    ```
    make truncate-db
    
    ```
    

## 📁 Project Structure

The backend code is organized into a clean, modular structure:

-   `app/api/`: Contains the API endpoints (routers).
    
-   `app/core/`: Core application settings, security, and exception handling.
    
-   `app/db/`: Database session management and base model classes.
    
-   `app/models/`: SQLAlchemy ORM models that define database tables.
    
-   `app/repository/`: The data access layer that handles all database queries.
    
-   `app/schema/`: Pydantic schemas for data validation and serialization.
    
-   `app/services/`: The business logic layer where all operations are orchestrated.
    
-   `scripts/`: Standalone scripts for administrative tasks.
    
-   `alembic/`: Contains the database migration scripts.