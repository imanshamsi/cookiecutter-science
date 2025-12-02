# Technical Documentation

**Table of contents:**

- [SQL Server](#SQL-Server-Connector)
  - [Overview](#Overview)
  - [Installation](#Installation)
  - [Configuration Model](#Configuration-Model)
  - [Fields](#Fields)
  - [Options](#Options)
  - [Using the Connector](#Using-the-Connector)
  - [Query Execution](#Query-Execution)
  - [Troubleshooting](#Troubleshooting)



## SQL Server Connector
### Overview

The SQL Server Connector provides a unified interface for connecting to Microsoft SQL Server from Python using two interchangeable backends:

* **ODBC**
* **JDBC**

The system uses:
* A centralized `ConnectionConfig`
* Strategy-based driver selection
* Context-managed sessions
* Factory-based driver instantiation
* Strict error handling and clean abstractions

The design supports backend services, ETL tasks, and analytics workloads that require reliable, configurable SQL Server access.

### Installation
#### ODBC

Install if you intend to use the ODBC driver:
```bash
pip install pyodbc
```

Linux systems require the Microsoft ODBC driver:
```bash
sudo apt-get update
sudo apt-get install msodbcsql18
```

Confirm the driver is available:
```bash
odbcinst -q -d
```

Expected:
```
[ODBC Driver 18 for SQL Server]
```

#### JDBC

Requires the Microsoft JDBC Driver `.jar` file and Java.

Install:
```bash
pip install jaydebeapi JPype1
```

JVM requirement:
```bash
sudo apt-get install default-jre
```

Place the JDBC driver JAR inside your application, e.g.:
```
libs/jdbc/mssql-jdbc-13.2.1.jre11.jar
```

### Configuration Model
```python
ConnectionConfig(
    driver="jdbc",
    host="192.168.30.78",
    database="DataDb",
    username="username",
    password="password",
    port=6985,
    options={ ... }
)
```

### Fields
| Field        | Description                   |
| ------------ | ----------------------------- |
| **driver**   | `"odbc"` or `"jdbc"`          |
| **host**     | SQL Server host/IP            |
| **database** | Target database               |
| **user**     | SQL Server username           |
| **password** | SQL Server password           |
| **port**     | Defaults to 1433              |
| **options**  | Driver-specific configuration |


### Options
The `options` dictionary allows each backend to support its own features without complicating the top-level connector.
Below is the deep explanation of each backend’s options.

#### ODBC Options

Valid when:
```python
driver="odbc"
```

| Option             | Purpose                                             | Example                                     |
| ------------------ | --------------------------------------------------- | ------------------------------------------- |
| **driver_name**    | Exact ODBC driver name returned by `odbcinst -q -d` | `"ODBC Driver 18 for SQL Server"`           |
| **extra_conn_str** | Additional ODBC parameters                          | `"Encrypt=yes;TrustServerCertificate=yes;"` |

Example ODBC configuration:
```python
options={
    "driver_name": "ODBC Driver 18 for SQL Server",
    "extra_conn_str": "Encrypt=yes;TrustServerCertificate=yes;"
}
```

#### JDBC Options

Valid when:
```python
driver="jdbc"
```

| Option              | Purpose                                          |
| ------------------- | ------------------------------------------------ |
| **driver_jar**      | Absolute path to the JDBC JAR file               |
| **driver_class**    | Class used by the SQL Server JDBC driver         |
| **jdbc_properties** | Extra properties passed into the JDBC connection |

Example JDBC configuration:
```python
options={
    "driver_jar": "/app/libs/jdbc/mssql-jdbc-13.2.1.jre11.jar",
    "driver_class": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
    "jdbc_properties": {
        "encrypt": "false"
    }
}
```

JDBC is generally the cleanest way to connect in environments where ODBC is unavailable or adds complexity, especially in containers.


### Using the Connector

This example loads the JDBC JAR and creates a client.

```python
from integrations.mssql.connector import SqlServerClient
from integrations.mssql.config import ConnectionConfig

JDBC_JAR = "/lib/jdbc/mssql-jdbc-13.2.1.jre11.jar"

config = ConnectionConfig(
    driver="jdbc",
    host="192.168.30.78",
    port=6985,
    database="DataDb",
    username="username",
    password="password",
    options={
        "driver_jar": JDBC_JAR,
        "driver_class": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
        "jdbc_properties": {
            "encrypt": "false"
        }
    }
)

client = SqlServerClient(config)

with client.session() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 10 name FROM sys.tables;")
    print(cursor.fetchall())
```

### Query Execution
Execute a single value:
```python
value = client.execute("SELECT 1", fetch="one")
```

Fetch table list:
```python
tables = client.execute("SELECT name FROM sys.tables", fetch="all")
```

Rowcount only:
```python
count = client.execute("SELECT * FROM sys.objects")
```

Valid values for `fetch`:

| Value   | Description               |
| ------- | ------------------------- |
| `"one"` | Returns first row         |
| `"all"` | Returns entire result set |
| `None`  | Returns rowcount          |

### Troubleshooting

#### ODBC: “Can't open lib”

Cause: malformed driver string.
Correct format:
```
DRIVER={ODBC Driver 18 for SQL Server};
```

---

#### ODBC: certificate verify failed

Fix using:
```
Encrypt=yes;TrustServerCertificate=yes;
```

or disable encryption:
```
Encrypt=no;
```

---

#### JDBC: JVM not found

Install Java:
```bash
sudo apt-get install default-jre
```

Ensure JPype is installed:
```bash
pip install JPype1
```
