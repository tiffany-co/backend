# Use a multi-stage build for a smaller and more secure final image.

# --- 1. Builder Stage ---
# This stage installs dependencies.
FROM python:3.11-slim AS builder

WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --only main


# --- 2. Runner Stage ---
# This is the final, lean image that will run in production.
FROM python:3.11-slim AS runner

WORKDIR /app

# Copy the installed packages and executables from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the application code into the final image
COPY ./app /app/app
COPY ./alembic /app/alembic
COPY ./scripts /app/scripts
COPY alembic.ini /app/
COPY ./entrypoint.sh /app/entrypoint.sh

# --- Make the entrypoint script executable ---
RUN chmod +x /app/entrypoint.sh

# --- Set the entrypoint script to be executed on container start ---
ENTRYPOINT ["/app/entrypoint.sh"]

# The default command to be executed by the entrypoint script
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

