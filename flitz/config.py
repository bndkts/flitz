"""Configuration management for Flitz."""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml
from pydantic import BaseModel, Field, field_validator


class Config(BaseModel):
    """Application configuration."""

    font_size: int = Field(
        default=14, description="Font size for the application"
    )
    external_config: Optional[Union[str, List[str]]] = Field(
        default=None, description="Path(s) to external configuration files"
    )

    @field_validator("external_config", mode="before")
    @classmethod
    def validate_external_config(cls, v: Any) -> Any:
        """Convert string to list for external_config."""
        if isinstance(v, str):
            return [v]
        return v

    @staticmethod
    def load() -> "Config":
        """Load configuration from ~/.flitz.yml and external configs."""
        config_path = Path.home() / ".flitz.yml"
        config_data: Dict[str, Any] = {}

        # Load main config if it exists
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f) or {}

        # Load external configs if specified
        external_configs = config_data.get("external_config", [])
        if external_configs:
            if isinstance(external_configs, str):
                external_configs = [external_configs]

            for ext_config_path in external_configs:
                ext_path = Path(ext_config_path).expanduser()
                if ext_path.exists():
                    with open(ext_path, "r", encoding="utf-8") as f:
                        ext_data = yaml.safe_load(f) or {}
                        # External configs can override existing values
                        config_data.update(ext_data)

        return Config(**config_data)
