# Stage 1: Builder - Install dependencies
FROM python:3.9-slim as builder

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Configure Poetry to not create virtual environments
RUN poetry config virtualenvs.create false

# Copy dependency definition files
COPY pyproject.toml poetry.lock ./

# Install only production dependencies
RUN poetry install --no-root --only main


# Stage 2: Runner - The final, lean image
FROM python:3.9-slim

WORKDIR /app

# Copy the installed Python libraries from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy the executables (like uvicorn) from the builder stage
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the application source code and Alembic configuration
COPY ./app /app/app
COPY ./alembic /app/alembic
COPY alembic.ini /app/

# Set the command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

