from etl.pipeline import run_pipeline


def main() -> None:
    """Run the NYC Yellow Taxi ETL pipeline from the command line."""
    run_pipeline()


if __name__ == "__main__":
    main()
