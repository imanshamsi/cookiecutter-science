from __future__ import annotations

from .base import DbApiConnection, BaseDriver
from ..exceptions import SqlDriverError


class JdbcSqlDriver(BaseDriver): ...