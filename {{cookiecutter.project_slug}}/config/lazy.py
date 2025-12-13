from typing import Any
import os 
from .loader import Settings
from config.env import load_environment, get_env, BASE_DIR


class LazySettings:
    def __init__(self):
        self._wrapped = None
        self._settings_module = None
        
    def _setup(self):
        if self._wrapped is not None:
            return
        
        load_environment(os.path.join(BASE_DIR, '.env.example'))

        dev_mode = get_env("DEV_MODE", "True").lower() in ("true", "1", "yes")
        self._settings_module = (
            "config.settings.production" if not dev_mode else "config.settings.development"
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
