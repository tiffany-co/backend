from app.application import create_app

# The main application instance, created by the factory.
# This is the entry point for the Uvicorn server.
app = create_app()

