from __future__ import annotations

from pathlib import Path

from etl.clean import clean_data
from etl.extract import extract_data
from etl.load import DEFAULT_BATCH_SIZE, load_data
from etl.transform import transform_data
from etl.validate import validate_data


DEFAULT_RAW_FILE_PATH = Path("data/raw/yellow_tripdata_2026-01-sample-100.csv")


def run_pipeline(
    file_path: str | Path = DEFAULT_RAW_FILE_PATH,
    batch_size: int = DEFAULT_BATCH_SIZE,
) -> int:
    """
    Run the complete NYC Yellow Taxi ETL workflow and return loaded row count.

    The pipeline preserves the existing stage responsibilities: extract reads,
    validate splits records, clean formats trusted records, transform creates the
    target schema, and load inserts the transformed rows into PostgreSQL.
    """
    print("=" * 60)
    print("NYC TAXI ETL PIPELINE STARTED")
    print("=" * 60)

    print("\n[1/5] Starting extraction...")
    raw_df = extract_data(file_path)
    print(f"Extraction completed. Raw rows: {len(raw_df):,}")
    print(f"Raw columns: {raw_df.shape[1]}")

    print("\n[2/5] Starting validation...")
    trusted_df, quarantined_df = validate_data(raw_df)
    print("Validation completed.")
    print(f"Trusted rows: {len(trusted_df):,}")
    print(f"Quarantined rows: {len(quarantined_df):,}")

    print("\n[3/5] Starting cleaning...")
    cleaned_df = clean_data(trusted_df)
    print(f"Cleaning completed. Cleaned rows: {len(cleaned_df):,}")

    print("\n[4/5] Starting transformation...")
    transformed_df = transform_data(cleaned_df)
    print("Transformation completed.")
    print(f"Transformed rows: {len(transformed_df):,}")
    print(f"Transformed columns: {transformed_df.shape[1]}")

    assert len(trusted_df) == len(cleaned_df), "Cleaning changed row count"
    assert len(cleaned_df) == len(transformed_df), "Transformation changed row count"

    print("\n[5/5] Starting load...")
    inserted_rows = load_data(transformed_df, batch_size=batch_size)
    print(f"Loading completed. Inserted rows: {inserted_rows:,}")

    print("\n" + "=" * 60)
    print("ETL PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)

    return inserted_rows
