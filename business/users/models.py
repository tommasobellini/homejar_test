from typing import Optional

from bson import ObjectId

from business.models import HomeJarModel


class UserModel(HomeJarModel):
    username: str
    email: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "string",
                "email": "string",
                "active": True,
                "created_at": "string",
                "created_by": "string",
                "modified_at": "string",
                "modified_by": "string",
                "id": "string"
            }
        }
