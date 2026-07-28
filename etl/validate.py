from __future__ import annotations

import pandas as pd


ALLOWED_VENDOR_IDS = {1, 2,6,7}
ALLOWED_RATECODES = {1, 2, 3, 4, 5, 6, 99}
ALLOWED_STORE_AND_FWD_FLAGS = {"Y", "N"}
ALLOWED_PAYMENT_TYPES = {0, 1, 2, 3, 4, 5, 6}

MONETARY_COLUMNS = [
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

REQUIRED_COLUMNS = [
    "VendorID",
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "passenger_count",
    "trip_distance",
    "RatecodeID",
    "store_and_fwd_flag",
    "PULocationID",
    "DOLocationID",
    "payment_type",
    *MONETARY_COLUMNS,
]


def validate_required_columns(df: pd.DataFrame) -> None:
    """Raise an error if any columns required for validation are missing."""
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]

    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(f"Missing required columns: {missing_text}")


def _is_allowed_value(series: pd.Series, allowed_values: set[int | str]) -> pd.Series:
    """Return True where a non-null value is part of the allowed value set."""
    return series.isin(allowed_values)


def _is_numeric(series: pd.Series) -> pd.Series:
    """Return True where a non-null value can be interpreted as numeric."""
    return pd.to_numeric(series, errors="coerce").notna()


def _append_message(
    messages: pd.Series,
    mask: pd.Series,
    message: str,
) -> pd.Series:
    """Append a validation message to rows where mask is True."""
    updated_messages = messages.copy()
    updated_messages.loc[mask] = updated_messages.loc[mask].apply(
        lambda current: [*current, message]
    )
    return updated_messages


def validate_vendor_id(df: pd.DataFrame) -> pd.Series:
    """Return True for rows with missing or unofficial TLC vendor IDs."""
    return df["VendorID"].isna() | ~_is_allowed_value(
        df["VendorID"], ALLOWED_VENDOR_IDS
    )


def validate_pickup_datetime(df: pd.DataFrame) -> pd.Series:
    """Return True for rows with missing pickup datetimes."""
    return df["tpep_pickup_datetime"].isna()


def validate_dropoff_datetime(df: pd.DataFrame) -> pd.Series:
    """Return True for rows with missing dropoff datetimes."""
    return df["tpep_dropoff_datetime"].isna()


def validate_datetime_order(df: pd.DataFrame) -> pd.Series:
    """Return True for rows where dropoff datetime is before pickup datetime."""
    pickup_datetime = pd.to_datetime(df["tpep_pickup_datetime"], errors="coerce")
    dropoff_datetime = pd.to_datetime(df["tpep_dropoff_datetime"], errors="coerce")

    return pickup_datetime.notna() & dropoff_datetime.notna() & (
        dropoff_datetime < pickup_datetime
    )


def validate_ratecode(df: pd.DataFrame) -> pd.Series:
    """Return True for rows with non-null rate codes outside TLC values."""
    ratecode = df["RatecodeID"]
    return ratecode.notna() & ~_is_allowed_value(ratecode, ALLOWED_RATECODES)


def validate_store_and_fwd_flag(df: pd.DataFrame) -> pd.Series:
    """Return True for rows with non-null store-and-forward flags outside Y/N."""
    flag = df["store_and_fwd_flag"]
    return flag.notna() & ~_is_allowed_value(flag, ALLOWED_STORE_AND_FWD_FLAGS)


def validate_trip_distance(df: pd.DataFrame) -> pd.Series:
    """Return True for rows with negative trip distance."""
    trip_distance = pd.to_numeric(df["trip_distance"], errors="coerce")
    return trip_distance.notna() & (trip_distance < 0)


def validate_location_ids(df: pd.DataFrame) -> pd.Series:
    """Return True for rows missing required pickup or dropoff location IDs."""
    return df["PULocationID"].isna() | df["DOLocationID"].isna()


def validate_payment_type(df: pd.DataFrame) -> pd.Series:
    """Return True for rows with payment types outside allowed TLC values."""
    return df["payment_type"].isna() | ~_is_allowed_value(
        df["payment_type"], ALLOWED_PAYMENT_TYPES
    )


def validate_monetary_columns_are_numeric(df: pd.DataFrame) -> pd.Series:
    """Return True for rows with non-null monetary values that are not numeric."""
    invalid_mask = pd.Series(False, index=df.index)

    for column in MONETARY_COLUMNS:
        value = df[column]
        invalid_mask = invalid_mask | (value.notna() & ~_is_numeric(value))

    return invalid_mask


def flag_negative_monetary_values(df: pd.DataFrame) -> pd.Series:
    """Return True for rows with negative monetary values needing business review."""
    warning_mask = pd.Series(False, index=df.index)

    for column in MONETARY_COLUMNS:
        value = pd.to_numeric(df[column], errors="coerce")
        warning_mask = warning_mask | (value.notna() & (value < 0))

    return warning_mask


def validate_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Validate raw NYC Yellow Taxi records and separate trusted from quarantined rows.

    The function does not clean or transform business data. It only evaluates
    validation rules and adds validation metadata to returned records.
    """
    validate_required_columns(df)

    validation_errors = pd.Series([[] for _ in range(len(df))], index=df.index)
    validation_warnings = pd.Series([[] for _ in range(len(df))], index=df.index)

    error_checks = [
        (validate_vendor_id(df), "Invalid VendorID"),
        (validate_pickup_datetime(df), "Missing tpep_pickup_datetime"),
        (validate_dropoff_datetime(df), "Missing tpep_dropoff_datetime"),
        (validate_datetime_order(df), "Dropoff datetime is before pickup datetime"),
        (validate_ratecode(df), "Invalid RatecodeID"),
        (validate_store_and_fwd_flag(df), "Invalid store_and_fwd_flag"),
        (validate_trip_distance(df), "Negative trip_distance"),
        (validate_location_ids(df), "Missing PULocationID or DOLocationID"),
        (validate_payment_type(df), "Invalid payment_type"),
        (validate_monetary_columns_are_numeric(df), "Non-numeric monetary value"),
    ]

    for invalid_mask, message in error_checks:
        validation_errors = _append_message(validation_errors, invalid_mask, message)

    negative_money_mask = flag_negative_monetary_values(df)
    validation_warnings = _append_message(
        validation_warnings,
        negative_money_mask,
        "Negative monetary value needs business review",
    )

    quarantine_mask = validation_errors.apply(bool)
    trusted_df = df.loc[~quarantine_mask].copy()
    quarantined_df = df.loc[quarantine_mask].copy()

    trusted_df["validation_warnings"] = validation_warnings.loc[~quarantine_mask]
    quarantined_df["validation_errors"] = validation_errors.loc[quarantine_mask]
    quarantined_df["validation_warnings"] = validation_warnings.loc[quarantine_mask]

    return trusted_df, quarantined_df
