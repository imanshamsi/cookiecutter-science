from __future__ import annotations
import os
from typing import Any
from pathlib import Path

from .base import DbApiConnection, BaseDriver
from ..exceptions import SqlDriverError


class JdbcSqlDriver(BaseDriver):

    def _connect_impl(self) -> DbApiConnection:
        try:
            import jaydebeapi as jdbc
        except ImportError as exc:
            raise SqlDriverError(
                "The JDBC driver requires jaydebeapi to be installed. Install with "
                "`pip install jaydebeapi`."
            ) from exc

        port = self.port or 1433
        jdbc_url = self.options.get(
            "jdbc_url",
            f"jdbc:sqlserver://{self.host}:{port};databaseName={self.database}",
        )

        driver_class = self.options.get(
            "driver_class", "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        )

        driver_jar = self.options.get(
            "driver_jar",
            os.path.join(
                Path(__file__).resolve().parent.parent,
                "libs/jdbc/mssql-jdbc-13.2.1.jre11.jar"
            )
        )
        if not driver_jar:
            raise SqlDriverError(
                "JDBC driver requires `driver_jar` option pointing to the "
                "mssql-jdbc.jar file."
            )

        props: dict[str, Any] = {
            "user": self.username,
            "password": self.password,
        }

        # allow extra JDBC props
        props.update(self.options.get("jdbc_properties", {}))

        return jdbc.connect(driver_class, jdbc_url, props, driver_jar)
