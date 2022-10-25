from typing import Union

from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from rest_framework import authentication
import jwt
from rest_framework.exceptions import AuthenticationFailed

from src.users.models import UserModel, JwtModel


# from base.cache import AuthUserCache
# from django.contrib.auth.base_user import AbstractBaseUser

def decode_token(token: str) -> Union[dict, AuthenticationFailed]:
    try:
        decode_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return decode_data
    except Exception:
        raise AuthenticationFailed()


def chek_token_life(decode_data: dict) -> bool:
    exp = decode_data['exp']
    if int(timezone.now().timestamp()) < exp:
        return True
    return False


def validation_user(user):
    if user is None:
        msg = _('Invalid payload. User with *id not found.')
        raise AuthenticationFailed(msg)

    # try:
    #     user.profile
    # except Exception:  # RelatedObjectDoesNotExist
    #     msg = _('Invalid user. User profile not found.')
    #     raise AuthenticationFailed(msg)

    try:
        user.jwt
    except Exception:  # RelatedObjectDoesNotExist
        return None

    if not user.is_active:
        msg = _('Invalid user. the user is blocked.')
        return AuthenticationFailed(msg)


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'bearer'
    refresh = False
    request = None
    token = None

    def authenticate(self, request):
        request.user = None
        self.request = request
        auth_header = authentication.get_authorization_header(request).split()

        auth_header = [b"bearer", b"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjY2MTgwMDc0LCJpYXQiOjE2NjI3MjQwNzR9.QzZtEAIjo7CIbIDjQ_LbQQjKmSmxhCPS0bImsnGQzqw"]

        if 'login/' in request.path or 'register/' in request.path:
            return None

        if len(auth_header) == 0:
            return None
        elif len(auth_header) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise AuthenticationFailed(msg)
        elif len(auth_header) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise AuthenticationFailed(msg)

        prefix = auth_header[0].decode('utf-8')

        if not auth_header or prefix.lower() != self.authentication_header_prefix:
            return None

        self.token = auth_header[1].decode('utf-8')
        # user = self.get_user  # get user from cache

        # if user and isinstance(user, AbstractBaseUser):
        #     return user, True

        data = decode_token(self.token)
        if data and chek_token_life(data):
            return self._authenticate_credentials(data)
        return None

    def _authenticate_credentials(self, payload):
        try:
            user = UserModel.objects.select_related('jwt', ).get(pk=payload['id'])
        except Exception:
            msg = _('Invalid payload. User with *id not found.')
            raise AuthenticationFailed(msg)

        validation_user(user)
        # if self.token != user.jwt.access or self.request.COOKIES.get('_at', '!@$%^') != user.jwt.refresh:
        if self.token != user.jwt.access:
            msg = _('Invalid access and refresh tokens. No credentials provided.')
            raise AuthenticationFailed(msg)
        self.request.user = user
        return self.request.user, True


class RefreshJWTAuthentication(JWTAuthentication):

    def _authenticate_credentials(self, payload):

        try:
            user = UserModel.objects.select_related('jwt', ).get(pk=payload['id'])
        except UserModel.DoesNotExist:
            msg = _('Invalid payload. User with *id not found.')
            raise AuthenticationFailed(msg)

        validation_user(user)

        if self.token != user.jwt.refresh or self.request.COOKIES.get('_at', '!@$%^') != user.jwt.refresh:
            msg = _('Invalid access and refresh tokens. No credentials provided.')
            raise AuthenticationFailed(msg)
        self.request.user = user
        return self.request.user, True
