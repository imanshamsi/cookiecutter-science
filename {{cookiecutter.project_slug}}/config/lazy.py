from typing import Any

from .settings.base import DEBUG
from .loader import Settings
from config.env import load_environment, get_env


class LazySettings:
    def __init__(self):
        self._wrapped = None
        self._settings_module = None
        
    def _setup(self):
        if self._wrapped is not None:
            return
        
        env = get_env("APP_ENV", "dev")
        self._settings_module = (
            "config.settings.production" if env == "prod" else "config.settings.development"
        )
        self._wrapped = Settings(self._settings_module)

    def __getattr__(self, name: str) -> Any:
        self._setup()
        return getattr(self._wrapped, name)

    def get(self, name: str, default=None) -> Any:
        self._setup()
        return self._wrapped.get(name, default)

    def reload(self) -> None:
        self._wrapped = None
        self._settings_module = None

    def __reduce__(self):
        return '<LazySettings loader>'
