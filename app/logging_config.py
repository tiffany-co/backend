import logging
from logging.config import dictConfig

def setup_logging():
    """
    Configures the logging for the application.
    - A colorful, formatted log for the console (Uvicorn's default).
    - A plain, uncolored, formatted log for the app.log file.
    """
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(asctime)s - %(name)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "plain": {
                "format": "%(levelname)s: %(asctime)s - %(name)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "app_file": {
                "formatter": "plain", # Use the new plain formatter
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "app.log",
                "maxBytes": 1024 * 1024 * 5, # 5 MB
                "backupCount": 10,
            },
        },
        "loggers": {
            "app": {
                "handlers": ["default", "app_file"],
                "level": "INFO",
            },
        },
    }
    dictConfig(log_config)

# Get the configured logger to be imported by other modules
logger = logging.getLogger("app")
