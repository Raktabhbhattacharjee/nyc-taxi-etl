from __future__ import annotations

import pandas as pd


DATETIME_COLUMNS = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
]

NUMERIC_COLUMNS = [
    "VendorID",
    "passenger_count",
    "trip_distance",
    "RatecodeID",
    "PULocationID",
    "DOLocationID",
    "payment_type",
    "fare_amount",
    "extra",
    "mta_tax",
    "tip_amount",
    "tolls_amount",
    "improvement_surcharge",
    "total_amount",
    "congestion_surcharge",
    "Airport_fee",
    "cbd_congestion_fee",
]

COLUMN_RENAME_MAP = {
    "VendorID": "vendor_id",
    "RatecodeID": "ratecode_id",
    "PULocationID": "pu_location_id",
    "DOLocationID": "do_location_id",
    "Airport_fee": "airport_fee",
}

PREFERRED_COLUMN_ORDER = [
    "vendor_id",
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "pickup_date",
    "pickup_hour",
    "pickup_day_name",
    "trip_duration_minutes",
    "passenger_count",
    "trip_distance",
    "fare_per_mile",
    "ratecode_id",
    "store_and_fwd_flag",
    "pu_location_id",
    "do_location_id",
    "payment_type",
    "fare_amount",
    "extra",
    "mta_tax",
    "tip_amount",
    "tolls_amount",
    "improvement_surcharge",
    "total_amount",
    "congestion_surcharge",
    "airport_fee",
    "cbd_congestion_fee",
]

METADATA_COLUMNS_TO_DROP = [
    "validation_warnings",
]


def convert_datetime_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert pickup and dropoff datetime columns to pandas datetime values."""
    transformed_df = df.copy()

    for column in DATETIME_COLUMNS:
        if column in transformed_df.columns:
            transformed_df[column] = pd.to_datetime(transformed_df[column])

    return transformed_df


def convert_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert known numeric columns to numeric values for analytics and loading."""
    transformed_df = df.copy()

    for column in NUMERIC_COLUMNS:
        if column in transformed_df.columns:
            transformed_df[column] = pd.to_numeric(transformed_df[column])

    return transformed_df


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add time-based analytical columns from pickup and dropoff timestamps."""
    transformed_df = df.copy()

    pickup_datetime = transformed_df["tpep_pickup_datetime"]
    dropoff_datetime = transformed_df["tpep_dropoff_datetime"]

    transformed_df["pickup_date"] = pickup_datetime.dt.date
    transformed_df["pickup_hour"] = pickup_datetime.dt.hour
    transformed_df["pickup_day_name"] = pickup_datetime.dt.day_name()
    transformed_df["trip_duration_minutes"] = (
        dropoff_datetime - pickup_datetime
    ).dt.total_seconds() / 60

    return transformed_df


def add_fare_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add fare metrics used for trip-level analysis."""
    transformed_df = df.copy()

    transformed_df["fare_per_mile"] = (
        transformed_df["fare_amount"] / transformed_df["trip_distance"]
    ).where(transformed_df["trip_distance"] > 0)

    return transformed_df


def rename_columns_for_target_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Rename selected TLC columns to PostgreSQL-friendly snake_case names."""
    return df.rename(columns=COLUMN_RENAME_MAP)


def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Place commonly used analytical columns first while preserving all columns."""
    ordered_columns = [
        column for column in PREFERRED_COLUMN_ORDER if column in df.columns
    ]
    remaining_columns = [
        column for column in df.columns if column not in ordered_columns
    ]

    return df[ordered_columns + remaining_columns]


def remove_etl_metadata_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Remove ETL metadata columns that do not belong in the analytical trips table."""
    return df.drop(columns=METADATA_COLUMNS_TO_DROP, errors="ignore")


def transform_data(cleaned_df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform cleaned NYC Yellow Taxi records into the final analytical dataset.

    This stage applies business logic for analytics and PostgreSQL loading. It
    does not read raw data, validate records, quarantine rows, or load data.
    """
    transformed_df = cleaned_df.copy()

    transformed_df = convert_datetime_columns(transformed_df)
    transformed_df = convert_numeric_columns(transformed_df)
    transformed_df = add_time_features(transformed_df)
    transformed_df = add_fare_features(transformed_df)
    transformed_df = rename_columns_for_target_schema(transformed_df)
    transformed_df = remove_etl_metadata_columns(transformed_df)
    transformed_df = reorder_columns(transformed_df)

    return transformed_df
