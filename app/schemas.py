from pydantic import BaseModel, HttpUrl, EmailStr
from typing import Optional
from enum import Enum

class PPMEnum(str, Enum):
    venmo = "Venmo"
    cashapp = "CashApp"
    paypal = "PayPal"
    zelle = "Zelle"

# Schema for client requests to create a new user
# Designed as the writeable fields for a user
class UserCreate(BaseModel):
    email: EmailStr
    display_name: str
    photo_url: HttpUrl

# Schema for responses, potentially including more information
#   designed as the read only fields for a user, separate from the create fields
class UserResponse(BaseModel):
    uid: str
    email: EmailStr
    display_name: str
    photo_url: HttpUrl
    # Additional fields used in responses but not in creation
    # ppm: Optional[PPMEnum]
    # ppm_identifier: Optional[str]
