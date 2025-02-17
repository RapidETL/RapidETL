import pytest
from rapidetl.rapidetl import RapidETL, run_pipeline
from pathlib import Path

def test_rapidetl_initialization():
    etl = RapidETL()
    assert isinstance(etl, RapidETL)

def test_pipeline_config_validation():
    with pytest.raises(ValueError):
        run_pipeline("nonexistent_file.json") 