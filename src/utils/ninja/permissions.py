from django.http import HttpRequest

from src.utils.ninja.backends import JWTAuthentication, CookieAuthenticate


class BasePermission:

    def __init__(self, chek_permission: bool = False, request: HttpRequest = None, obj=None):
        self.chek_permission = chek_permission
        if self.chek_permission:
            self.__call__ = None
        self.check_object_permissions(request, obj)

    def __call__(self, request):
        request.user = JWTAuthentication()(request)
        return self.has_permission(request)

    def check_object_permissions(self, request, obj):
        return self.has_object_permission(request, obj)

    def has_permission(self, request):
        return True

    @classmethod
    def has_object_permission(cls, request, obj):
        return True


class RefreshAuth(BasePermission):

    def __call__(self, request):
        request.user = CookieAuthenticate()(request)
        return self.has_permission(request)

    def has_permission(self, request):
        return True


class IsAuthenticate(BasePermission):

    def has_permission(self, request):
        return True if bool(request.user) else False
