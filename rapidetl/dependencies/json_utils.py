import json
from pathlib import Path
from typing import Dict, Any

def load_json(config_path: str) -> Dict[str, Any]:
    """
    LOAD JSON Configuration from a file
    """
    try:
        with open(config_path, "r") as file:
            return json.load(file)
    except Exception as e:
        raise ValueError(f"Failed to load JSON config: {e}")