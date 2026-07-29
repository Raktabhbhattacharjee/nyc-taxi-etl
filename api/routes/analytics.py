from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from api.deps import get_db
from etl.models import YellowTaxiTrip

DEFAULT_TOP_LIMIT = 10


def get_trips_per_day(db: Session = Depends(get_db)) -> list[dict[str, object]]:
    """Return total taxi trips grouped by pickup date."""
    statement = (
        select(
            YellowTaxiTrip.pickup_date,
            func.count(YellowTaxiTrip.id).label("trip_count"),
        )
        .group_by(YellowTaxiTrip.pickup_date)
        .order_by(YellowTaxiTrip.pickup_date)
    )

    return [
        {"pickup_date": pickup_date, "trip_count": trip_count}
        for pickup_date, trip_count in db.execute(statement).all()
    ]


def get_trips_by_payment_type(
    db: Session = Depends(get_db),
) -> list[dict[str, int]]:
    """Return total taxi trips grouped by payment type."""
    statement = (
        select(
            YellowTaxiTrip.payment_type,
            func.count(YellowTaxiTrip.id).label("trip_count"),
        )
        .group_by(YellowTaxiTrip.payment_type)
        .order_by(YellowTaxiTrip.payment_type)
    )

    return [
        {"payment_type": payment_type, "trip_count": trip_count}
        for payment_type, trip_count in db.execute(statement).all()
    ]


def get_trips_by_vendor(db: Session = Depends(get_db)) -> list[dict[str, int]]:
    """Return total taxi trips grouped by vendor."""
    statement = (
        select(
            YellowTaxiTrip.vendor_id,
            func.count(YellowTaxiTrip.id).label("trip_count"),
        )
        .group_by(YellowTaxiTrip.vendor_id)
        .order_by(YellowTaxiTrip.vendor_id)
    )

    return [
        {"vendor_id": vendor_id, "trip_count": trip_count}
        for vendor_id, trip_count in db.execute(statement).all()
    ]


def get_hourly_demand(db: Session = Depends(get_db)) -> list[dict[str, int]]:
    """Return total taxi trips grouped by pickup hour."""
    statement = (
        select(
            YellowTaxiTrip.pickup_hour,
            func.count(YellowTaxiTrip.id).label("trip_count"),
        )
        .group_by(YellowTaxiTrip.pickup_hour)
        .order_by(YellowTaxiTrip.pickup_hour)
    )

    return [
        {"pickup_hour": pickup_hour, "trip_count": trip_count}
        for pickup_hour, trip_count in db.execute(statement).all()
    ]


def get_top_pickup_locations(
    db: Session = Depends(get_db),
) -> list[dict[str, int]]:
    """Return the busiest pickup locations by trip count."""
    statement = (
        select(
            YellowTaxiTrip.pu_location_id,
            func.count(YellowTaxiTrip.id).label("trip_count"),
        )
        .group_by(YellowTaxiTrip.pu_location_id)
        .order_by(func.count(YellowTaxiTrip.id).desc())
        .limit(DEFAULT_TOP_LIMIT)
    )

    return [
        {"pu_location_id": pu_location_id, "trip_count": trip_count}
        for pu_location_id, trip_count in db.execute(statement).all()
    ]


def get_top_dropoff_locations(
    db: Session = Depends(get_db),
) -> list[dict[str, int]]:
    """Return the busiest dropoff locations by trip count."""
    statement = (
        select(
            YellowTaxiTrip.do_location_id,
            func.count(YellowTaxiTrip.id).label("trip_count"),
        )
        .group_by(YellowTaxiTrip.do_location_id)
        .order_by(func.count(YellowTaxiTrip.id).desc())
        .limit(DEFAULT_TOP_LIMIT)
    )

    return [
        {"do_location_id": do_location_id, "trip_count": trip_count}
        for do_location_id, trip_count in db.execute(statement).all()
    ]
