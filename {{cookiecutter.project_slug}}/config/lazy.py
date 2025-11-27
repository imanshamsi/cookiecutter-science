from typing import Any

from .settings.base import DEBUG
from .loader import Settings


class LazySettings:
    def __init__(self):
        self._settings_module = (
            'config.settings.development'
            if DEBUG
            else 'config.settings.production'
        )
        self._wrapped: Settings | None = None

    def _setup(self):
        if self._wrapped is None:
            self._wrapped = Settings(self._settings_module)

    def __getattr__(self, name: str) -> Any:
        self._setup()
        return getattr(self._wrapped, name)

    def get(self, name: str, default=None) -> Any:
        self._setup()
        return self._wrapped.get(name, default)

    def reload(self) -> None:
        self._wrapped = None

    def __reduce__(self):
        return '<LazySettings loader>'
