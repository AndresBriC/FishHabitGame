# Backend contributor notes

- Keep route handlers thin. Put game rules and transaction orchestration in application services as the feature set grows.
- Use Pydantic request and response models for every public endpoint beyond the health check.
- Use one database transaction per player action that changes game state.
- Add an Alembic migration for every model/schema change; do not alter prior migrations.
- Tests must not require a running production database. Use isolated test dependencies or a disposable test database.
