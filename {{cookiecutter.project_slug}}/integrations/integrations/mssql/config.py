from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Mapping, Any


@dataclass(frozen=True)
class ConnectionConfig:
    driver: str
    host: str
    database: str
    username: str
    password: str
    port: Optional[int] = None
    options: Optional[Mapping[str, Any]] = None

    def normalized_driver(self) -> str:
        return self.driver.lower()
