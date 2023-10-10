from typing import Optional
import uuid
from pydantic import BaseModel, Field

# Custom Pydantic field to handle UUID representation
class UUIDField(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        try:
            return cls(str(uuid.UUID(value)))
        except ValueError:
            raise ValueError("Invalid UUID format")
class HomeJarModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    active: bool = False
    created_at: Optional[str] = None
    created_by: Optional[str] = None
    modified_at: Optional[str] = None
    modified_by: Optional[str] = None