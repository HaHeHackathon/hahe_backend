from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID, uuid4
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    user = "user"

# User model
class User(BaseModel):
    id: Optional[UUID] = uuid4()
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    roles: List[Role]


class StationInfo(BaseModel):
    evaNumber: str
    name: str

