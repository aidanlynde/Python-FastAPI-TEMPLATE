# from typing import List, Optional
# from pydantic import BaseModel, HttpUrl
# from enum import Enum

# #Preffered Payment Method
# class PPMEnum(str, Enum):
#     venmo = "Venmo"
#     cashapp = "CashApp"
#     paypal = "PayPal"
#     zelle = "Zelle"

# class User(BaseModel):
#     uid: str
#     email: str
#     display_name: str
#     photo_url: HttpUrl  # Validates URL format
#     # ppm: PPMEnum
#     # ppm_identifier: str






# # class GroupMember(BaseModel):
# #     user: User
# #     hasPaid: bool

# # class Group(BaseModel):
# #     members: List[GroupMember]
# #     name: str
# #     price: float  # Use float for price