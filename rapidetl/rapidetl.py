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

def run_pipeline(config_path: str, progress_callback=None) -> None:
    """
    Load JSON config, Validate and execute the pipeline
    """
    
    # Load JSON configuration
    config = load_json(config_path)
    if progress_callback:
        progress_callback("Loading configuration", 0.2)

    # Validate JSON structure using pydantic
    vconfig = validate_config(config, PipelineConfig)
    if progress_callback:
        progress_callback("Validating configuration", 0.3)

    # Load Data from sources
    data = {}
    for i, source in enumerate(vconfig.source):
        if source.type == "csv":
            if progress_callback:
                progress_callback(f"Loading source {i+1}/{len(vconfig.source)}", 0.4 + (i * 0.2))
            connector = CSVConnector()
            data.update(connector.load(source.config))
        else:
            raise ValueError(f"Unsupported source type: {source.type}")
    
    # Write Data to Sink
    for i, sink in enumerate(vconfig.sink):
        if sink.type == "csv":
            if progress_callback:
                progress_callback(f"Writing to sink {i+1}/{len(vconfig.sink)}", 0.7 + (i * 0.2))
            connector = CSVConnector()
            connector.write(data, sink.config)
        else:
            raise ValueError(f"Unsupported sink type: {sink.type}")
    
    if progress_callback:
        progress_callback("Pipeline complete", 1.0)


