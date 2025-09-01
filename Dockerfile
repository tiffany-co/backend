# --- Stage 1: Build the application with Poetry ---

# Use an official Python runtime as a parent image
FROM python:3.9-slim as builder

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Configure Poetry to not create virtual environments, as the container is the environment
RUN poetry config virtualenvs.create false

# Copy the dependency files to the working directory
COPY pyproject.toml poetry.lock ./

# Install only production dependencies
# --no-root: Don't install the project itself, only dependencies
# --no-dev: Skip development dependencies
RUN poetry install --no-root --no-dev

# Copy the rest of the application source code
COPY . .


# --- Stage 2: Create the final production image ---

FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the installed dependencies from the builder stage
COPY --from=builder /app/ .

# The command to run the application
# Uvicorn is run with --host 0.0.0.0 to be accessible from outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
