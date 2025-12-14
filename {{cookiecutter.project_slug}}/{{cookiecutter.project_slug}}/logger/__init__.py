import logging
from config import settings

def configure_logging():
    if getattr(logging, "_cookiecutter_configured", False):
        return

    settings.LOG_DIR.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=settings.LOG_LEVEL,
        filename=settings.LOG_FILE,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(settings.LOG_LEVEL)
    console_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    logging.getLogger().addHandler(console_handler)

    logging._cookiecutter_configured = True

def get_logger(name: str):
    configure_logging()
    return logging.getLogger(name)