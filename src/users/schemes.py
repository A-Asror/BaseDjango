import datetime as dt
from secrets import compare_digest as compare_secret_data

from typing import Optional, Dict, Union

import pydantic as pdc

from src.users.models import Permissions
from src.base.schemes import BaseScheme
from src.utils.ninja.exceptions import ValidationError


def check_age(dob: dt.date) -> dt.date:
    min_age = dt.datetime.today().year - 14
    if not (1940 < dob.year <= min_age):
        raise ValidationError(status_code=400, message="year not valid")
    return dob


class TokenScheme(pdc.BaseModel):
    access: str


class BaseUserSchema(BaseScheme):
    username: Optional[str]
    email: Optional[pdc.EmailStr]
    phone: Optional[str]
    fullname: Optional[str]
    permission: Optional[pdc.conint(ge=0, le=len(Permissions))]
    dob: Optional[dt.datetime]
    about: Optional[str]
    links: Optional[dict]
    images: Optional[dict]
    is_active: Optional[bool]


class RegisterSchemaIn(BaseScheme):
    username: str  # required
    email: pdc.EmailStr  # required
    phone: str  # required
    fullname: Optional[str]
    permission: Optional[pdc.conint(ge=2, le=len(Permissions))]
    dob: Optional[dt.datetime]
    about: Optional[str]
    links: Optional[dict]
    images: Optional[dict]
    password: str = pdc.Field(min_length=8, max_length=50)
    confirm_password: str = pdc.Field(min_length=8, max_length=50)

    @pdc.validator("dob")
    def validate_dob(cls, dob: dt.date):
        return check_age(dob)

    @pdc.root_validator
    def check_passwords_match(cls, values: Dict[str: Union[bool, dt.date, str, int]]):
        password, confirm_password = values.get("password"), values.pop("confirm_password")
        # Если пароли не совпадают то вывести ошибку
        if bool(password and confirm_password) and compare_secret_data(password, confirm_password):
            raise ValidationError(message="Passwords do not match", status_code=400)
        return values
