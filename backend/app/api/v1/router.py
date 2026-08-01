from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Return a lightweight readiness response without touching the database."""
    return {"status": "ok"}
