from enum import Enum
from typing import AnyStr, Optional

from django.contrib.postgres.indexes import BrinIndex
from django.db import models
from django.utils import timezone


class BandManager(models.Manager):
    @property
    def get_search_fields(self):
        if hasattr(self.model, "search_fields"):
            return self.get_queryset().search_fields
        return []


class BaseModel(models.Model):
    created_at = models.DateTimeField(editable=False, null=True, blank=True)
    updated_at = models.DateTimeField(editable=False, null=True, blank=True)
    objects = BandManager()

    class Meta:
        abstract = True
        indexes = (BrinIndex(fields=("created_at", "updated_at")),)

    def save(self, update: Optional[dict] = None, update_fields: Optional[list[AnyStr]] = None, *args, **kwargs):
        from src.base.utils import get_list_dict_keys, setattr_for_save_obj

        if not self.id:
            self.created_at = timezone.localtime(timezone.now())
        self.updated_at = timezone.localtime(timezone.now())
        setattr_for_save_obj(self, update)
        new_update_fields = get_list_dict_keys(update) if (update is not None) else None
        if new_update_fields is not None:
            if (update_fields is not None) and isinstance(update_fields, list):
                update_fields += new_update_fields
            else:
                update_fields = new_update_fields
        return super(BaseModel, self).save(*args, update_fields=update_fields, **kwargs)

    @classmethod
    def update_fields(cls, user, **data):
        """
        Метод для перечислений доступных для изменений аттрибутов, исходя от роли пользователя.

        Метод должен возвращать список аттрибутов.
        Example: ['username', 'email', ....]
        """
        raise NotImplementedError

    def get_upload_url(self):
        """Метод получения Пути для сохранения файла."""
        raise NotImplementedError


class BaseEnum(Enum):
    @classmethod
    def get_choice(cls):
        return [(attr.value, attr.name) for attr in cls]


class ActiveVerifiedMode:
    """Абстрактный класс где будут использовать аттрибуты active и verified."""

    active = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
