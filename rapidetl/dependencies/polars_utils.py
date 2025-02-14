import polars as pl

def read_csv(path: str) -> pl.DataFrame:
    """
    Read a CSV file into a Dataframe.
    """
    return pl.read_csv(path)

def write_csv(df: pl.DataFrame, path: str) -> None:
    """
    Write a Polars DataFrame to a CSV file
    """
    df.write_csv(path)