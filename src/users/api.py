from ninja import Router

from src.base.schemes import Message
from src.users import schemes
from src.users.models import UserModel
from src.utils.ninja.code_status import message_code_status
from src.utils.ninja.exceptions import ValidationError

router = Router()


@router.post("/register/", response={message_code_status: Message}, tags=["users"])
def register(request, payload: schemes.RegisterSchemaIn):
    data = payload.dict()
    password = data.pop("password")
    if UserModel.objects.filter(username=data['username'], email=data['email']).exists():
        raise ValidationError(f"A user with the same email: {data['username']} or username: {data['email']} already exists")
    user = UserModel(**data)
    user.set_password(password)
    user.save()
    return 200, {"message": "User created"}


@router.post("/login/", response={message_code_status: Message}, tags=["users"])
def login(request, payload: schemes.LoginSchema, response: HttpResponse):
    payload = payload.dict()
    request.user = authenticate(request, email=payload['email'], password=payload['password'])
    if request.user:
        return UpdateTokens(request=request, response=response).render_access_refresh_token
    return 401, {'message': 'User not found!'}


@router.get("/refresh/", response={message_code_status: schemes.Message}, tags=["users"], auth=RefreshAuth())
def get(request, response: HttpResponse):
    return UpdateTokens(request, response).response


@router.get("/logout/", response={message_code_status: schemes.Message}, tags=["users"], auth=IsAuthenticate())
def logout(request, response: HttpResponse):
    JwtModel.objects.filter(user_id=request.user.pk).delete()
    response.delete_cookie(key='_at')
    return {'message': 'logout'}