from pydantic import BaseModel, ConfigDict


class ConfigBaseModelResponseDTO(BaseModel):
    """Настроенный BaseModel для ResponseDTO"""

    model_config = ConfigDict(from_attributes=True)
