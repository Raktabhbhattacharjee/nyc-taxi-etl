from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response schema for the health endpoint."""

    status: str
    database: str


class TripResponse(BaseModel):
    """Response schema for one processed yellow taxi trip."""

    id: int
    vendor_id: int
    tpep_pickup_datetime: datetime
    tpep_dropoff_datetime: datetime
    pickup_date: date
    pickup_hour: int
    pickup_day_name: str
    trip_duration_minutes: Decimal
    passenger_count: int | None
    trip_distance: Decimal | None
    fare_per_mile: Decimal | None
    ratecode_id: int | None
    store_and_fwd_flag: str | None
    pu_location_id: int
    do_location_id: int
    payment_type: int
    fare_amount: Decimal | None
    extra: Decimal | None
    mta_tax: Decimal | None
    tip_amount: Decimal | None
    tolls_amount: Decimal | None
    improvement_surcharge: Decimal | None
    total_amount: Decimal | None
    congestion_surcharge: Decimal | None
    airport_fee: Decimal | None
    cbd_congestion_fee: Decimal | None

    model_config = {"from_attributes": True}
