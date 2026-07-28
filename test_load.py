from pathlib import Path

from etl.extract import extract_data
from etl.validate import validate_data
from etl.clean import clean_data
from etl.transform import transform_data
from etl.load import load_data

print("1. Starting")

csv_path = Path("data/raw/yellow_tripdata_2026-01.csv")

raw_df = extract_data(csv_path)
print("2. Extract complete")

trusted_df, quarantined_df = validate_data(raw_df)
print("3. Validate complete")

cleaned_df = clean_data(trusted_df)
print("4. Clean complete")

transformed_df = transform_data(cleaned_df)
print("5. Transform complete")

inserted = load_data(transformed_df.head(100), batch_size=100)
print("6. Load complete")

print(f"Rows inserted: {inserted}")