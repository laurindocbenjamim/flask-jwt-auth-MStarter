

from pydantic import BaseModel, Field, field_validator, FieldValidationInfo
from datetime import datetime
from typing import Optional
from enum import Enum
from markupsafe import escape


class UserType(str, Enum):
    USER_TYPE = "student"

class Status(str, Enum):
    ACTIVE = "active"

class UserCreateRequest(BaseModel):
    user_id: int = Field(..., gt=0, alias="id", description="User ID must be positive")
# Model configurations
# ---
class Config:
    populate_by_email = True
    allow_populate_field_by_email = True
    use_enum_values = True