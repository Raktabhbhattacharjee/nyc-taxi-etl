from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""


class YellowTaxiTrip(Base):
    """ORM model for transformed NYC Yellow Taxi trip records."""

    __tablename__ = "yellow_taxi_trips"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    vendor_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tpep_pickup_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
    )
    tpep_dropoff_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
    )
    pickup_date: Mapped[date] = mapped_column(Date, nullable=False)
    pickup_hour: Mapped[int] = mapped_column(Integer, nullable=False)
    pickup_day_name: Mapped[str] = mapped_column(String(9), nullable=False)
    trip_duration_minutes: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    passenger_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    trip_distance: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    fare_per_mile: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)

    ratecode_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    store_and_fwd_flag: Mapped[str | None] = mapped_column(String(1), nullable=True)
    pu_location_id: Mapped[int] = mapped_column(Integer, nullable=False)
    do_location_id: Mapped[int] = mapped_column(Integer, nullable=False)
    payment_type: Mapped[int] = mapped_column(Integer, nullable=False)

    fare_amount: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    extra: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    mta_tax: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    tip_amount: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    tolls_amount: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    improvement_surcharge: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )
    total_amount: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    congestion_surcharge: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )
    airport_fee: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    cbd_congestion_fee: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )
