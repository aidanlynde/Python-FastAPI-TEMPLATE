from typing import List, Optional
from pydantic import BaseModel, HttpUrl
from enum import Enum

class UserProfile(BaseModel):
    uid: str
    email: str
    full_name: str
    age: int
    gender: str
    height: float
    weight: float






# # class GroupMember(BaseModel):
# #     user: User
# #     hasPaid: bool

# # class Group(BaseModel):
# #     members: List[GroupMember]
# #     name: str
# #     price: float  # Use float for price