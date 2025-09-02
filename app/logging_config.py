import logging
from logging.config import dictConfig

def setup_logging():
    """
    Configures the logging for the application with two distinct loggers:
    1. audit: For tracking user actions and important business events.
    2. app: For general application logs, debugging, and errors.
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
            "audit": {
                "format": "%(asctime)s - AUDIT - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "audit_file": {
                "formatter": "audit",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "audit.log",
                "maxBytes": 1024 * 1024 * 5,  # 5 MB
                "backupCount": 10,
            },
            "app_file": {
                "formatter": "default",
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
            "audit": {
                "handlers": ["audit_file"],
                "level": "INFO",
                "propagate": False, # Prevent audit logs from going to the root logger
            },
        },
    }
    dictConfig(log_config)

# Get the configured loggers to be imported by other modules
logger = logging.getLogger("app")
audit_logger = logging.getLogger("audit")

