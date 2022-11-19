from datetime import datetime as dt
from typing import List

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from src.base.models import BaseModel, BandManager


class UserManager(BaseUserManager, BandManager):
    def create_user(self, email: str, password: str, **extra_fields) -> "UserModel":
        if email is None:
            raise TypeError("Users must have a email.")
        if password is None:
            raise TypeError("Both password fields must be filled")
        if self.model.objects.filter(email=email):
            raise ValidationError(_('пользователь с email %(email) уже существует'), code='email exists',
                                  params={'email': email})
        user: UserModel = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, **extra_fields) -> create_user:
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


Gender = [
    ('Male', 'Male'),
    ('Female', 'Female')
]

Permissions = (
    (1, _("Admin")),
    (2, _("User")),
)


class UserModel(BaseModel, AbstractBaseUser, PermissionsMixin):
    username: str = models.CharField(max_length=255, unique=True)
    email: str = models.EmailField(unique=True)
    phone: str = models.CharField(max_length=13, unique=True)
    fullname: str = models.CharField(max_length=150)
    permission: int = models.IntegerField(choices=Permissions, default=7)
    dob: dt.date = models.DateField(blank=True, null=True)
    about: str = models.TextField(blank=True, null=True)
    links: dict = models.JSONField(blank=True, null=True)  # ссылки соц сетей  default={}
    images: dict = models.JSONField(blank=True, null=True)
    is_active: bool = models.BooleanField(default=True)
    is_superuser: bool = models.BooleanField(default=False)
    is_staff: bool = models.BooleanField(default=False)
    USERNAME_FIELD: str = 'email'
    objects: UserManager = UserManager()

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f'ID: {self.pk}, username: {self.username}'

    @classmethod
    def search_fields(cls):
        return ['username', 'email', 'last_name', 'first_name']

    @classmethod
    def update_fields(cls, user: 'UserModel'):
        fields = ['username', 'email', 'last_name', 'first_name']
        if user.permission == 0:
            fields.extend(('permission', 'is_active'))
        return fields


class JwtModel(BaseModel):
    user: UserModel = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name="jwt")
    access: str = models.TextField()
    refresh: str = models.TextField()

    class Meta:
        db_table = "jwt"
        verbose_name = "Jwt"
        verbose_name_plural = "Jwt"

    def __str__(self):
        return "Model: %s username: %s id: %s" % (self.__name__, self.user.username, self.pk)
