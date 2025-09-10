#!/bin/sh

# This script is the entrypoint for the production Docker container.
# It ensures that database migrations are applied before the main application starts.

# Exit immediately if a command exits with a non-zero status.
set -e

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Then, execute the command passed to this script (the Dockerfile's CMD).
# This will start the Uvicorn server.
exec "$@"
