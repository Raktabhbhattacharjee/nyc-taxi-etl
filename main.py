from etl.extract import extract_data
from etl.validate import validate_data


def main():
    df = extract_data("data/raw/yellow_tripdata_2026-01.csv")

    trusted_df, quarantined_df = validate_data(df)

    print(f"Original rows      : {len(df):,}")
    print(f"Trusted rows       : {len(trusted_df):,}")
    print(f"Quarantined rows   : {len(quarantined_df):,}")

    # Sanity Check 1
    assert len(df) == len(trusted_df) + len(quarantined_df)

    # Sanity Check 2
    print("\nValidation Error Summary")
    print(quarantined_df["validation_errors"].value_counts())

    # Sanity Check 3
    print("\nQuarantined VendorIDs")
    print(quarantined_df["VendorID"].value_counts(dropna=False))

    # Optional: View first few quarantined rows
    print("\nSample Quarantined Rows")
    print(
        quarantined_df[
            ["VendorID", "validation_errors", "validation_warnings"]
        ].head(10)
    )


if __name__ == "__main__":
    main()