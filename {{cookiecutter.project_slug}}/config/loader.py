import importlib
from typing import Any, Dict


class Settings:
    def __init__(self, settings_module: str):
        self.settings_module = settings_module
        self._settings: Dict[str, Any] = {}
        self._load_settings()

    def _load_settings(self) -> None:
        try:
            module = importlib.import_module(self.settings_module)

        except ModuleNotFoundError as e:
            raise ImportError(f'Settings module "{self.settings_module}" not found.') from e

        for name in dir(module):
            self._settings[name] = getattr(module, name)

    def get(self, name: str, default=None) -> Any:
        return self._settings.get(name, default)

    def __getattr__(self, name: str) -> Any:
        if name in self._settings:
            return self._settings[name]
        raise AttributeError(f'Setting "{name}" not found.')

    def __repr__(self):
        return f'<Settings module={self.settings_module}>'
