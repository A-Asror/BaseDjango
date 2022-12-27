from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from jwt import api_jwt

from src.users.models import JwtModel


def token_generator(uid, format_time):
    data_token = {"id": uid, "exp": timezone.localtime(timezone.now()) + timedelta(**format_time), "iat": timezone.localtime(timezone.now())}  # minutes, days
    token = api_jwt.encode(data_token, settings.SECRET_KEY, algorithm="HS256")
    return token


def _response(access: str, refresh: str):
    return 200, {"access": access, "refresh": refresh}


class UpdateTokens:
    def __init__(self, request, response):
        self.request = request
        self.response_to = response

    @property
    def access_and_refresh_token(self):
        refresh = token_generator(self.request.user.id, {"days": 30})
        access = token_generator(self.request.user.id, {"days": 40})
        return access, refresh

    @property
    def check_jwt_model_and_update(self):
        jwt_user = self.request.user.jwt
        access, refresh = self.access_and_refresh_token
        jwt_user.access = access
        jwt_user.refresh = refresh
        jwt_user.save()
        return [access, refresh], True

    @property
    def render_access_refresh_token(self):
        access, refresh = self.access_and_refresh_token
        jwt_user = JwtModel.objects.filter(user_id=self.request.user.id).exists()
        if not jwt_user:  # создать новый объект Jwt если его нет
            JwtModel(user_id=self.request.user.id, access=access, refresh=refresh).save()
            return _response(access, refresh)
        return self.response  # обновить токены если они есть в базе

    @property
    def response(self):
        data, exc = self.check_jwt_model_and_update
        if exc:
            return _response(data[0], data[1])
        return 400, {"message": data}
