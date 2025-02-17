from pydantic import BaseModel, ValidationError
from typing import Dict, Any

def validate_config(config: Dict[str, Any], schema: BaseModel) -> BaseModel:
    """
    Validate a configuration dictionary aganist a Pydantic schema
    """
    try:
        return schema(**config)
    except ValidationError as e:
        raise ValueError(f"Invalid JSON config: {e}")