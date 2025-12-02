from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class DbApiConnection(Protocol):
    def cursor(self, *args: Any, **kwargs: Any) -> Any: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...
    def close(self) -> None: ...


class BaseDriver(ABC):
    def __init__(
            self,
            host: str,
            database: str,
            username: str,
            password: str,
            port: int | None = None,
            **options: Any
    ) -> None:
        self.host = host
        self.database = database
        self.username = username
        self.password = password
        self.port = port
        self.options = options

    @abstractmethod
    def _connect_impl(self) -> DbApiConnection:
        raise NotImplementedError

    def connect(self) -> DbApiConnection:
        return self._connect_impl()
