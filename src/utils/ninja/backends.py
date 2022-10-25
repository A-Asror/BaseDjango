from typing import Optional, Any

import jwt
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ninja.compatibility import get_headers
from ninja.security.http import HttpAuthBase, logger

from src.users import UserModel
from src.utils.exceptions import AuthenticationFailed


def decode_token(token):
    try:
        decode_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return decode_data
    except Exception:
        msg = _('Invalid token.')
        raise AuthenticationFailed(msg)


def chek_token_life(decode_data):
    exp = decode_data['exp']
    if int(timezone.localtime(timezone.now()).timestamp()) < exp:
        return True
    return False


def validation_user(user):
    if user is None:
        msg = _('Invalid payload. User with *id not found.')
        raise AuthenticationFailed(msg)
    elif user.is_active is False:
        msg = _('Invalid user. the user is blocked.')
        raise AuthenticationFailed(msg)
    elif isinstance(user, AbstractBaseUser) is False:
        msg = _('Invalid user')
        raise AuthenticationFailed(msg)
    try:
        user.jwt
    except UserModel.jwt.RelatedObjectDoesNotExist:  # RelatedObjectDoesNotExist
        msg = _('Invalid token. please log in')
        raise AuthenticationFailed(msg)


class JWTAuthentication(HttpAuthBase):
    openapi_scheme: str = "bearer"
    header: str = "Authorization"
    token: str = None
    request: HttpRequest = None

    def __call__(self, request: HttpRequest) -> Optional[Any]:
        headers = get_headers(request)
        auth_value = headers.get(self.header)
        # auth_value = b'bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjY0NzE4MDcxLCJpYXQiOjE2NjEyNjIwNzF9.2SX6hdmg6xkX369RrUUZZquY5EG2Ml37ETlV4wH_R48'
        if not auth_value:
            return None

        auth_value = auth_value.decode("utf-8")
        auth_header = auth_value.split(" ")

        if auth_header[0].lower() != self.openapi_scheme:
            if settings.DEBUG:
                logger.error(f"Unexpected auth - '{auth_value}'")
            return None

        if 'login/' in request.path or 'register/' in request.path:
            return None
        elif len(auth_header) == 0:
            return None
        elif len(auth_header) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise AuthenticationFailed(msg)
        elif len(auth_header) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise AuthenticationFailed(msg)

        self.token = " ".join(auth_header[1:])
        self.request = request
        return self.authenticate()

    def authenticate(self):
        data = decode_token(self.token)
        if chek_token_life(data):
            return self._authenticate_credentials(data)
        return None

    def _authenticate_credentials(self, payload):

        try:
            user = UserModel.objects.select_related('jwt').defer('jwt__id', 'jwt__created_at', 'jwt__updated_at', 'jwt__user_id').get(pk=payload['id'])
        except Exception:
            msg = _('Invalid payload. User with *id not found.')
            raise AuthenticationFailed(msg)

        validation_user(user)

        if self.request.COOKIES.get('_at', '!@$%^') != user.jwt.refresh:
            msg = _('Invalid access and refresh tokens. No credentials provided.')
            raise AuthenticationFailed(msg)
        return user


class CookieAuthenticate(JWTAuthentication):
    openapi_scheme: str = 'refresh'
    header: str = 'Authorization_Refresh'

    def __call__(self, request: HttpRequest) -> Optional[Any]:
        request.META['HTTP_AUTHORIZATION_REFRESH'] = f"refresh {request.COOKIES.get('_at', '!@$%^')}".encode()
        return super().__call__(request)