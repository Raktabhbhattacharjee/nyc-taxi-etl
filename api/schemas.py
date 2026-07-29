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


class TripsPerDayResponse(BaseModel):
    """Response schema for daily trip counts."""

    pickup_date: date
    trip_count: int


class TripsByPaymentTypeResponse(BaseModel):
    """Response schema for trip counts by payment type."""

    payment_type: int
    trip_count: int


class TripsByVendorResponse(BaseModel):
    """Response schema for trip counts by vendor."""

    vendor_id: int
    trip_count: int


class HourlyDemandResponse(BaseModel):
    """Response schema for trip counts by pickup hour."""

    pickup_hour: int
    trip_count: int


class TopPickupLocationResponse(BaseModel):
    """Response schema for top pickup locations."""

    pu_location_id: int
    trip_count: int


class TopDropoffLocationResponse(BaseModel):
    """Response schema for top dropoff locations."""

    do_location_id: int
    trip_count: int
