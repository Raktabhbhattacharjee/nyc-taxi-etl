from __future__ import annotations

import re
from collections.abc import Callable

import pandas as pd


TEXT_COLUMNS_TO_UPPERCASE = {"store_and_fwd_flag"}


def _get_string_columns(df: pd.DataFrame) -> list[str]:
    """Return columns that contain string-like values."""
    return df.select_dtypes(include=["object", "string"]).columns.to_list()


def _clean_string_values(series: pd.Series, cleaner: Callable[[str], str]) -> pd.Series:
    """Apply a cleaner only to string values so missing and non-string values stay unchanged."""
    return series.map(lambda value: cleaner(value) if isinstance(value, str) else value)


def trim_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    """Trim leading and trailing whitespace from string columns."""
    cleaned_df = df.copy()

    for column in _get_string_columns(cleaned_df):
        cleaned_df[column] = _clean_string_values(
            cleaned_df[column],
            lambda value: value.strip(),
        )

    return cleaned_df


def normalize_internal_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    """Replace repeated internal whitespace in string columns with a single space."""
    cleaned_df = df.copy()

    for column in _get_string_columns(cleaned_df):
        cleaned_df[column] = _clean_string_values(
            cleaned_df[column],
            lambda value: re.sub(r"\s+", " ", value),
        )

    return cleaned_df


def normalize_text_case(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize safe categorical text formatting without changing business meaning."""
    cleaned_df = df.copy()

    for column in TEXT_COLUMNS_TO_UPPERCASE:
        if column in cleaned_df.columns:
            cleaned_df[column] = _clean_string_values(
                cleaned_df[column],
                lambda value: value.upper(),
            )

    return cleaned_df


def clean_data(trusted_df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply safe formatting cleanup to trusted NYC Yellow Taxi records.

    Cleaning preserves all rows, columns, and missing values. It does not validate,
    transform business fields, convert data types, or create derived columns.
    """
    cleaned_df = trusted_df.copy()

    cleaned_df = trim_whitespace(cleaned_df)
    cleaned_df = normalize_internal_whitespace(cleaned_df)
    cleaned_df = normalize_text_case(cleaned_df)

    return cleaned_df
