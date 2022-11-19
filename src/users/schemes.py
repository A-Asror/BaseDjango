import datetime as dt

from typing import Optional

from pydantic import EmailStr, conint

from src.users.models import Permissions
from src.base.schemes import BaseScheme


class BaseUserSchema(BaseScheme):
    username: Optional[EmailStr]
    email: Optional[str]
    phone: Optional[str]
    fullname: Optional[str]
    permission: Optional[conint(ge=0, le=len(Permissions))]
    dob: Optional[dt.datetime]
    about: Optional[str]
    links: Optional[dict]
    images: Optional[dict]
    is_active: Optional[bool]
