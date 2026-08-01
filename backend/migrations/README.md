# Database migrations

Alembic owns PostgreSQL schema changes for the web application. Do not edit a deployed database manually or rewrite an applied migration.

Create a migration after adding or changing SQLAlchemy models:

```powershell
alembic revision --autogenerate -m "describe change"
```

Apply all pending migrations:

```powershell
alembic upgrade head
```
