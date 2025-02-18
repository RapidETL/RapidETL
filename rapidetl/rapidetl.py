from pathlib import Path
from typing import Dict, Any, List
from .dependencies import *
from pydantic import BaseModel, ValidationError
from .dependencies.json_utils import load_json
from .dependencies.pydantic_utils import validate_config
from .connectors.csv_connector import CSVConnector

class RapidETL:
    def __init__(self) -> None:
        pass

class SourceConfig(BaseModel):
    type: str
    config: Dict[str, Any]

class SourceSink(BaseModel):
    type: str
    config: Dict[str, Any]

class PipelineConfig(BaseModel):
    name: str
    source: List[SourceConfig]
    sink: List[SourceSink]

def run_pipeline(config_path: str) -> None:
    """
    Load JSON config, Validate and execute the pipeline
    """
    
    # Load JSON configuration
    config = load_json(config_path)

    print(f"Successfully read config - {config}")

    # Validate JSON structure using pydantic
    vconfig = validate_config(config, PipelineConfig)

    print(f"Validated config - {vconfig}")

    # Load Data from sources
    data = {}
    for source in vconfig.source:
        if source.type == "csv":
            connector = CSVConnector()
            data.update(connector.load(source.config))
        else:
            raise ValueError(f"Unsupported source type: {source.type}")
    
    # Write Data to Sink
    for sink in vconfig.sink:
        if sink.type == "csv":
            connector = CSVConnector()
            connector.write(data, sink.config)
        else:
            raise ValueError(f"Unsupported sink type: {sink.type}")
        
    print("Pipeline executed successfully")


