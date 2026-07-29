from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.deps import get_db
from api.schemas import TripResponse
from etl.models import YellowTaxiTrip


router = APIRouter(prefix="/trips", tags=["trips"])


@router.get("", response_model=list[TripResponse])
def get_trips(
    limit: int = Query(default=20, ge=1, le=200),
    db: Session = Depends(get_db),
) -> list[YellowTaxiTrip]:
    """Return processed taxi trips from PostgreSQL."""
    statement = select(YellowTaxiTrip).order_by(YellowTaxiTrip.id).limit(limit)
    return list(db.scalars(statement).all())
