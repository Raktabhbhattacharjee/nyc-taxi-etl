from __future__ import annotations

from collections.abc import Iterator
from decimal import Decimal
from typing import Any

import pandas as pd
from sqlalchemy import Integer, Numeric

from etl.database import SessionLocal
from etl.models import YellowTaxiTrip


DEFAULT_BATCH_SIZE = 1_000
TARGET_COLUMNS = [
    column.name for column in YellowTaxiTrip.__table__.columns if column.name != "id"
]
INTEGER_COLUMNS = {
    column.name
    for column in YellowTaxiTrip.__table__.columns
    if isinstance(column.type, Integer) and column.name != "id"
}
NUMERIC_COLUMNS = {
    column.name
    for column in YellowTaxiTrip.__table__.columns
    if isinstance(column.type, Numeric)
}


def _iter_batches(df: pd.DataFrame, batch_size: int) -> Iterator[pd.DataFrame]:
    """Yield DataFrame slices no larger than batch_size."""
    for start in range(0, len(df), batch_size):
        yield df.iloc[start : start + batch_size]


def _normalize_value(column_name: str, value: Any) -> Any:
    """Convert pandas values into plain Python values suitable for SQLAlchemy."""
    if pd.isna(value):
        return None

    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime()

    if hasattr(value, "item"):
        value = value.item()

    if column_name in INTEGER_COLUMNS:
        return int(value)

    if column_name in NUMERIC_COLUMNS:
        return Decimal(str(value))

    return value


def _row_to_trip(row: pd.Series) -> YellowTaxiTrip:
    """Build a YellowTaxiTrip ORM object from one transformed DataFrame row."""
    values = {
        column: _normalize_value(column, row[column])
        for column in TARGET_COLUMNS
    }
    return YellowTaxiTrip(**values)


def _validate_load_input(transformed_df: pd.DataFrame, batch_size: int) -> None:
    """Validate the load input before opening a database transaction."""
    if batch_size < 1:
        raise ValueError("batch_size must be greater than zero")

    missing_columns = [
        column for column in TARGET_COLUMNS if column not in transformed_df.columns
    ]
    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(f"Missing required load columns: {missing_text}")


def load_data(
    transformed_df: pd.DataFrame,
    batch_size: int = DEFAULT_BATCH_SIZE,
) -> int:
    """
    Load transformed NYC Yellow Taxi records into PostgreSQL in committed batches.

    Returns the number of rows committed successfully. If a batch fails, only the
    current batch is rolled back and the original exception is raised.
    """
    _validate_load_input(transformed_df, batch_size)

    inserted_rows = 0
    session = SessionLocal()

    try:
        for batch_df in _iter_batches(transformed_df, batch_size):
            trips = [_row_to_trip(row) for _, row in batch_df.iterrows()]

            try:
                session.add_all(trips)
                session.commit()
            except Exception:
                session.rollback()
                raise

            inserted_rows += len(trips)
    finally:
        session.close()

    return inserted_rows
