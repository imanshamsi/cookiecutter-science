from __future__ import annotations
from contextlib import contextmanager
from typing import Any, Dict, Type, Generator

from .config import ConnectionConfig
from .drivers import (
    BaseDriver,
    DbApiConnection,
    OdbcSqlDriver,
    JdbcSqlDriver,
    DdbcSqlDriver
)
from .exceptions import SqlConfigurationError, SqlDriverError, SqlConnectionError


class Driver:

    _DRIVER_MAP: Dict[str, Type[BaseDriver]] = {
        "odbc": OdbcSqlDriver,
        "jdbc": JdbcSqlDriver,
        "ddbc": DdbcSqlDriver,
        "mssql": OdbcSqlDriver,
    }

    @classmethod
    def create_driver(cls, config: ConnectionConfig) -> BaseDriver:
        driver_key = config.normalized_driver()
        driver_cls = cls._DRIVER_MAP.get(driver_key)
        if driver_cls is None:
            raise SqlDriverError(
                f"Unknown driver {driver_key}. "
                f"Supported {sorted(cls._DRIVER_MAP.keys())}"
            )

        options = dict(config.options or {})
        return driver_cls(
            host=config.host,
            database=config.database,
            username=config.username,
            password=config.password,
            port=config.port,
            **options
        )


class SqlServerClient:

    def __init__(self, config: ConnectionConfig) -> None:
        if not config.host or not config.database:
            raise SqlConfigurationError("Missing host or database name.")

        self._config = config
        self._driver: BaseDriver = Driver.create_driver(config)

    @property
    def config(self) -> ConnectionConfig:
        return self._config

    def connect(self) -> DbApiConnection:
        try:
            return self._driver.connect()
        except Exception as exc:
            raise SqlConnectionError(f"Failed to connect to SQL-Server: {exc}")

    @contextmanager
    def session(self) -> Generator[DbApiConnection, None, None]:
        conn = self.connect()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def execute(
        self,
        sql: str,
        params: tuple[Any, ...] | dict[str, Any] | None = None,
        fetch: str | None = None
    ) -> Any:
        """
          Execute a sql command in a session.

          fetch:
              None     -> return rowcount
              "one"    -> return single row
              "all"    -> return list of rows
          """
        with self.session() as conn:
            cursor = conn.cursor()
            if params is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)

            if fetch is None:
                return cursor.rowcount
            if fetch == "one":
                return cursor.fetchone()
            if fetch == "all":
                return cursor.fetchall()

            raise ValueError(f"Unknown fetch mode: {fetch}")
