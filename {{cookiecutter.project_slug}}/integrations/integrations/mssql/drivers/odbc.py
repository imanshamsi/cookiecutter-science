from __future__ import annotations

from .base import DbApiConnection, BaseDriver
from ..exceptions import SqlDriverError


class OdbcSqlDriver(BaseDriver):

    def _connect_impl(self) -> DbApiConnection:
        try:
            import pyodbc
        except ImportError as exc:
            raise SqlDriverError(
                "The ODBC driver requires pyodbc to be installed. Install with "
                "`pip install pyodbc`."
            ) from exc

        port = self.port or 1433
        driver_name = self.options.get("driver_name", "ODBC Driver 18 for SQL Server")
        conn_str = (
            f"DRIVER={{{driver_name}}};"
            f"SERVER={self.host},{port};"
            f"DATABASE={self.database};"
            f"UID={self.username};"
            f"PWD={self.password};"
            "Encrypt=yes;"
            "TrustServerCertificate=yes;"
        )

        # allow caller to override connection string fragments
        extra_conn_str = self.options.get("extra_conn_str")
        if extra_conn_str:
            conn_str += f";{extra_conn_str}"

        return pyodbc.connect(conn_str)
