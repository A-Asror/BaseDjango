from django.db.models import Q
from django.http import HttpResponse
from ninja import Router

from src.base.schemes import Message
from src.users import schemes
from src.users.models import UserModel, JwtModel
from src.utils.ninja.code_status import message_code_status
from src.utils.ninja.exceptions import ValidationError
from src.utils.ninja.permissions import RefreshAuth, IsAuthenticate
from src.utils.token import UpdateTokens

router = Router()


@router.post("/register/", response={message_code_status: Message}, tags=["users"])
def register(request, payload: schemes.RegisterSchemeIn):
    data = payload.dict()
    password = data.pop("password")
    if UserModel.objects.filter(username=data['username'], email=data['email']).exists():
        raise ValidationError(f"A user with the same email: {data['username']} or username: {data['email']} already exists")
    user = UserModel(**data)
    user.set_password(password)
    user.save()
    return 200, {"message": "User created"}


@router.post("/login/", response={message_code_status: Message}, tags=["users"])
def login(request, payload: schemes.LoginSchemeIn, response: HttpResponse):
    user = UserModel.objects.filter(Q(email=payload.login) | Q(phone=payload.login) | Q(username=payload.login))

    count_user = user.count()
    user = user.last()

    # Если пользователь с таким логином только 1 и пароли
    if count_user != 1:
        return 401, {"message": "not valid login"}
    elif not user.check_password(payload.password):
        return 401, {"message": "User not found!"}

    if user is not None:
        request.user = user
        return UpdateTokens(request=request, response=response).render_access_refresh_token
    return 401, {'message': 'User not found!'}


@router.get("/refresh/", response={message_code_status: Message}, tags=["users"], auth=RefreshAuth())
def get(request, response: HttpResponse):
    return UpdateTokens(request, response).response


@router.get("/logout/", response={message_code_status: Message}, tags=["users"], auth=IsAuthenticate())
def logout(request, response: HttpResponse):
    JwtModel.objects.filter(user_id=request.user.pk).delete()
    response.delete_cookie(key='_at')
    return {'message': 'logout'}
