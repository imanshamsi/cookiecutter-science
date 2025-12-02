# Science Project Template


**Table of contents:**

- [Purpose](#Purpose)
- [Quick Start](#Quick-Start)
- [High Level Structure](#High-Level-Structure)
- [Environment and Settings](#Environment-and-Settings)
- [Data Layer](#Data-Layer)
- [Selectors](#Selectors)
- [Services](#Services)
- [Tasks](#Tasks)
- [Exception Handling](#Exception-Handling)



## Purpose

This template provides a scalable, predictable structure for data-science and ML teams building production-grade pipelines, experiments, and scheduled tasks.
The rules ensure that:

- Business logic is separated and testable.
- Settings are explicit, environment-driven, and reloadable.
- Tasks are thin wrappers around services.
- Data access is predictable and centralized.
- Documentation is automatically generated from code.

---

## Quick Start

### 1. Create & activate a virtual environment

```bash
cd {{ cookiecutter.project_slug }}/
virtualenv -p python3.10 venv
source venv/bin/activate
pip install -r requirements_dev.txt
pip install -r requirements.txt
```

### 2. Create your `.env`

```bash
cp .env.example .env
```

Fill in the required environment variables.

### 3. Run tests

```bash
pytest -q
```

### 4. Run celery worker

```bash
celery -A {{ cookiecutter.project_slug }}.setup worker -l INFO
```

### 5. Run celery beat
```bash
celery -A {{ cookiecutter.project_slug }}.setup beat -l INFO
```

### 6. Start mkdocs docs server

```bash
mkdocs serve
```

---

# High Level Structure
```
app/
    common/         # shared error types, base models, shared abstractions
    db/             # DB session management + SQLAlchemy models
    models/         # AI level models
    selectors/      # read operations
    services/       # write operations
    tasks/          # celery task wrappers, no business logic
    tests/          # app test files
    utils/          # pure utilities
    setup.py        # celery app build here
config/
    settings/       # base/development/production settings
    env.py          # .env loader + strict access
    loader.py       # dynamic settings importer
    lazy.py         # lazy settings resolver
    celery.py       # celery config
    utils/          # celery helpers
```

## Environment and Settings

### Rules
- Nothing runs without `.env`. Loading happens in `config/env.py`.
- `get_env()` is strict: required variables must exist.
- `LazySettings` chooses between development/production based on `DEBUG` in `base.py`.
- Settings **must not contain** logic. Only constants and configuration.

### What settings control
- DB connection strings
- Celery broker/backend
- Domain name (`APP_DOMAIN`)
- Task modules (`TASK_APPS`)
- Feature flags (optional)

### Bad practices
- Putting secrets directly in Python files.
- Doing computations or business logic in settings.
- Reading environment variables outside of `config.env.get_env()`.

## Data Layer

### Base Model
Located in `app/common/models.py`.

#### Responsibilities:

- Provide timestamps.
- Provide consistent string representation.
- Serve as the parent for all SQLAlchemy declarative models.

```python
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, DeclarativeBase

Model: DeclarativeBase = declarative_base()

class BaseModel(Model):
    __abstract__ = True
    __schema_name__: str = None

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        server_default=func.now()
    )
    updated_at = Column(
        DateTime,
        nullable=True
    )
```

### ORM Models
```
app/db/models/
```

They must:

- Inherit BaseModel.
- Contain relationships, foreign keys, constraints.
- Never contain business logic.

## Selectors
Location: `app/selectors/`
Selectors only fetch data, nothing else.
### Rules
- Must not mutate state.
- May compose other selectors.
- May use raw SQL, SQLAlchemy ORM, or query builders.

### Responsibilities
- Fetching domain objects.
- Applying filters/pagination.
- Fetching IDs for downstream logic.
- Selectors must be pure and deterministic.

`app/selectors/user.py`

```python
"""
Selectors for reading user-related data.
"""

from app.db.session import SessionLocal
from app.db.models.user import User


def user_get_by_id(*, user_id: int) -> User | None:
    """
    Fetch a user by ID.
    Pure read operation.
    """
    with SessionLocal() as db:
        return db.query(User).filter(User.id == user_id).one_or_none()
```

## Services

Location: `app/services/`
Services perform mutations, call external systems, and contain business rules.

### Rules:
- Keyword-only parameters (unless trivial).
- Must call selectors when validation requires reading.
- Must be fully tested.
- Must not import Celery tasks.

### Responsibilities:
- Creating/updating domain entities.
- Complex workflows.
- Cross-model logic.
- Validation that spans entities.

### Prohibited
- No printing.
- No Celery calls directly.

`app/services/user.py`

```python
"""
Services for user business logic.
"""

from app.common.exceptions import ApplicationError
from app.db.session import SessionLocal
from app.db.models.user import User
from app.selectors.user import user_get_by_id


def user_activate(*, user_id: int) -> User:
    """
    Activate a user account.
    This demonstrates a write operation + validation.
    """

    user = user_get_by_id(user_id=user_id)
    if not user:
        raise ApplicationError("User does not exist.", extra={"user_id": user_id})

    if user.is_active:
        return user

    with SessionLocal() as db:
        user.is_active = True
        db.add(user)
        db.commit()
        db.refresh(user)

    return user
```

## Tasks
Location: `app/tasks/`

Tasks wrap services—**they never contain business logic**.
You use the `@taskify` decorator, which wraps the function into a Celery shared task.

### Rules
- Tasks must import services inside the function to avoid circular imports.
- Tasks receive IDs, not objects.

### Tasks contain
- Object lookup
- Call to service
- Nothing else.

### Task registry
`config.utils.celery.register_tasks()` loads tasks from `settings.TASK_APPS`.
If you forget to add the module there, Celery won’t see your tasks. No excuses.

`config/settings/base.py` addition

```
TASK_APPS = [
    "app.tasks.user",
    "app.tasks.example",
    # ...
]
```

```python
"""
Tasks for executing business logic.
"""

from config.utils.celery import taskify


@taskify
def user_activate_task(user_id: int):
    
    # inline to avoid circular imports
    from app.services.user import user_activate
    user_activate(user_id=user_id)
```

### How Celery, Tasks, and Services Fit Together
```code
Celery Beat ──────┐
                  ↓
Celery Worker → Celery Task → Service → DB
```

#### Tasks never
- Touch the DB directly
- Contain business logic
- Call other tasks

## Exception Handling

You define two types:
```
ImproperlyConfigured  # errors during startup
ConfigError           # runtime config issues
ApplicationError      # domain/service-level errors
```

### Rules
- Services raise ApplicationError.
- Tasks may catch and retry.
- Config errors must fail fast; do not silence them.

```python
...
user = user_get_by_id(user_id=user_id)
if not user:
    raise ApplicationError("User does not exist.", extra={"user_id": user_id})
```

## Documentation
```
docs/
    api/            # autogenerated from docstrings
    business/       # problem description
    engineering/    # architecture, pipelines
    model/          # AI models and meta
    glossary.md
    index.md
```
Run
```bash
mkdocs serve -a 0.0.0.0:80
```
