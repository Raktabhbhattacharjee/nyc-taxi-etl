from pathlib import Path

import pandas as pd


def extract_data(file_path: str | Path) -> pd.DataFrame:
    """
    Read the raw NYC Yellow Taxi CSV file and return it as a pandas DataFrame.

    Parameters
    ----------
    file_path : str | Path
        Path to the raw CSV dataset.

    Returns
    -------
    pd.DataFrame
        Raw dataset exactly as read from the source.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.

    pd.errors.EmptyDataError
        If the CSV is empty.
    """
    return pd.read_csv(file_path)