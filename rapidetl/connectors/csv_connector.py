from pathlib import Path
from typing import Dict, Any
import polars as pl
from ..dependencies.polars_utils import read_csv, write_csv

class CSVConnector:
    """
    Handles reading and writing CSV files.
    """

    def load(self, config: Dict[str, Any]) -> Dict[str, pl.DataFrame]:
        """
        Load data from a csv file.
        """
        path = config.get("path")
        if not path:
            raise ValueError("Missing 'path' in CSV source config")
        
        #Read CSV into Polars Dataframe
        df = read_csv(path)
        return {"data": df}
    
    def write(self, data: Dict[str, pl.DataFrame], config: Dict[str, Any]) -> None:
        """
        Write Data to a CSV file
        """
        path = config.get("path")
        if not path:
            raise ValueError("Missing 'path' in CSV sink config")
        
        # Ensure the output dictonary exists 
        output_dir = Path(path).parent
        print(f"output_dir - {output_dir}")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Write Dataframe to CSV
        for name, df in data.items():
            write_csv(df, Path(path))