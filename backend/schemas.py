# import datetime as _dt

# import pydantic as _pydantic


# class _UserBase(_pydantic.BaseModel):
#     email: str


# class UserCreate(_UserBase):
#     hashed_password: str

#     class Config:
#         from_attributes = True


# class User(_UserBase):
#     id: int

#     class Config:
#         from_attributes = True


# class _LeadBase(_pydantic.BaseModel):
#     first_name: str
#     last_name: str
#     email: str
#     company: str
#     note: str


# class LeadCreate(_LeadBase):
#     pass


# class Lead(_LeadBase):
#     id: int
#     owner_id: int
#     date_created: _dt.datetime
#     date_last_updated: _dt.datetime

#     class Config:
#         from_attributes = True

from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    hashed_password: str

    class Config:
        from_attributes = True

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class LeadBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    company: str
    note: str

class LeadCreate(LeadBase):
    pass

class Lead(LeadBase):
    id: int
    owner_id: int
    date_created: datetime
    date_last_updated: datetime

    class Config:
        from_attributes = True

