import datetime as dt

from typing import Optional

from pydantic import EmailStr, conint
from ninja import Schema

from src.users import Permissions
from src.base.schemes import BaseScheme


class Message(Schema):
    message: str


class BaseUserSchema(BaseScheme):
    email: Optional[EmailStr]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    permission: Optional[conint(ge=0, le=len(Permissions))]
    dob: Optional[dt.datetime]
    about: Optional[str]
    links: Optional[dict]
    images: Optional[dict]
    is_active: Optional[dict]
