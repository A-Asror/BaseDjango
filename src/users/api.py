from src.users import UserModel


@router.post("/register/", response={message_code_status: schemes.Message}, tags=["users"])
def register(request, payload: schemes.RegisterSchema):
    payload = payload.dict()
    if UserModel.objects.filter(username=payload['username'], email=payload['email']).exists():
        return {'message': 'A user with the same email or username already exists', 'code': 401}
    password1 = payload.pop('password1', False)
    password2 = payload.pop('password2', False)
    if not password2 or not password2 or password2 != password1:
        return 400, {'message': 'passwords do not match'}
    payload['password'] = password1
    UserModel.objects.create(**payload)
    return 200, {"message": "User created"}


@router.post("/login/", response={message_code_status: schemes.Message}, tags=["users"])
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