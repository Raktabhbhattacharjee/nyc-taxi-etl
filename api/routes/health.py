from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from api.deps import get_db
from api.schemas import HealthResponse


router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)) -> HealthResponse:
    """Confirm that the API is running and PostgreSQL is reachable."""
    db.execute(text("SELECT 1"))
    return HealthResponse(status="ok", database="connected")
