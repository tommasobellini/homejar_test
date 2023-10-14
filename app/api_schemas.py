import uuid
from datetime import datetime

from pydantic import BaseModel

class HomeJarModel(BaseModel):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    created_by: str
    modified_at: datetime
    modified_by: str

class UserSchema(HomeJarModel):
    name: str
    phone: str
    email: str
    password: str
    super_admin: bool = False
    is_child: bool = False
    account_user: str = None
    settings: dict = None


