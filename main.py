from etl.extract import extract_data


def main():
    df = extract_data("data/raw/yellow_tripdata_2026-01.csv")

    print(df.shape)
    print(df.head())


if __name__ == "__main__":
    main()