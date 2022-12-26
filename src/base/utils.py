from typing import Union

from django.conf import settings
from django.db import transaction
from django.db.models import Model, Q, QuerySet
from ninja import UploadedFile
from pydantic import BaseModel as BaseSchema

from src.base.file_uploader import ImageUploader, check_prefix_image, check_size_image
from src.base.models import BaseModel
from src.utils.exceptions import ValidationError


def get_list_dict_keys(payload: dict) -> list:
    return list(payload.keys())


def create_images(images: list[UploadedFile], url: str, db_kwargs: dict):  # db_files: dict
    """Функция принимает список Изображений для сохранения."""
    for image in images:
        check_size_image(image)  # validation size
        check_prefix_image(image)  # validation prefix
    img = ImageUploader(images, url, db_kwargs)
    return img.create_images()


def update(user, obj: BaseModel, payload: Union[BaseSchema, dict]) -> BaseModel:
    """
    Функция для обновления любого экземпляра models.Model, и любого вложенности Объектов.

    Проверка наличия полей в Объекте, проверяется с помощью встроенного метода python: "hasattr"
    Для изменений полей используется встроенный метод python: "setattr"
    Для изменений вложенных объектов как OneToOneField или ForeignKey используется встроенный метода python: "getattr",
        затем заново вызывается этот же метод: "update" и передается:
        вложенный OneToOneField или ForeignKey Объект. для просмотра этой части смотрите: 49-50 строки
    argument:
    ----------
    user: Это экземпляр UserModel, и этот параметр нужен для того чтоб проверить; Может ли этот пользователь изменить
        аттрибуты, переданного Объекта для изменения, это проверяется с помощью метода update_fields у переданного
        объекта
    obj: Это Объект который будет изменен его аттрибуты
    payload: Это словарь или Экземпляр схемы BaseModel из pydantic(а), в этом параметре передается аттрибуты и их
       значения для изменения Объекта(obj)
    """
    return _update(user, obj, payload)


@transaction.atomic
def _update(user, obj: BaseModel, payload: Union[BaseSchema, dict]) -> BaseModel:
    if type(payload) is not dict:
        payload = payload.dict(exclude_defaults=True)
    update_fields = obj.update_fields(user, **payload)
    for attr, new_value in payload.items():
        obj_attrs: list = get_list_attr_names(obj)
        if hasattr(obj, attr) and not isinstance(new_value, dict) and (attr not in update_fields):
            raise ValidationError(status_code=400, message="permission denied")
        if hasattr(obj, attr) and not isinstance(new_value, dict) or (attr in obj_attrs):
            setattr(obj, attr, new_value)
        elif hasattr(obj, attr) and isinstance(new_value, dict) and (attr not in obj_attrs):
            _update(user, getattr(obj, attr), new_value)
    obj.save(update_fields=get_list_dict_keys(payload))
    return obj


def remove_null_from_Q_object(q_data):
    """
    Задача этой функции удалить все Q объекты.

    Где значение атрибута Q, равна на None Q(attr=None)
    result: если все атрибуты Q равны на None Q(attr=None), то вернет пустой tuple и False
     иначе если хоть 1 атрибут Q не равно на None, то он вернет объект Q и True
     True и False нужен узнать чтоб для фильтрации надо-ли фильтровать специально под Q объектов
    """
    return _remove_null_from_Q_object(q_data)


def _remove_null_from_Q_object(q_data):
    for num in range(len(q_data) - 1, -1, -1):
        if type(q_data.children[num]) is tuple:
            if isinstance(q_data.children[num][1], None):
                del q_data.children[num]
        elif type(q_data.children[num]) is Q:
            remove_null_from_Q_object(q_data.children[num])
    if len(q_data) == 0:
        return tuple(), False
    return q_data, True


def paginator(queryset: QuerySet, page: int, page_size: int = 15) -> QuerySet:
    end = page * page_size
    start = end - page_size
    return queryset[start:end]


def setattr_for_save_obj(obj, update: Union[dict, None]):
    """
    Для автоматизации обновлений.

    Argument:
    ----------
    obj: Object
        obj - Это один из дочериных классов src.models.BaseModel(a)
        Используется при обновлении аттрибутов этого объекта(obj), который был передан в параметре: kwargs
    data: update
        data - Это dict или None
        Используется при обновлении аттрибутов Объекта(obj)
        Если дата None то метод вернет None и не обновит никаких аттрибутов

    Этот метод срабатывает при вызове метода .save() у всех дочериных классах src.models.BaseModel(a)
    Метод упрощает обновлений аттрибутов, пример:
        Обычно чтоб изменить аттрибут объекта пишется:
        obj.attr = new_value
        obj.attr2 = new_value2
        obj.attr3 = new_value3
        ....
        obj.save()
        Чтобы упрощать этот процесс и уменьшить кол-во строк, теперь можно:
        obj.save(update={"attr": "new_value", "attr2": new_value, "attr3": new_value, ....})
    """
    return _setattr_for_save_obj(obj, update)


def _setattr_for_save_obj(obj, update: Union[dict, None]):
    data = update

    if data is None:
        return

    for attr, value in data.items():
        if hasattr(obj, attr):
            setattr(obj, attr, value)


def get_list_attr_names(cls) -> list:
    if isinstance(cls, Model):
        return [field.name for field in cls._meta.fields]
    return []


def reformat_img_url(dict_images: dict):
    data = dict()
    if dict_images is None:
        return data
    domain = settings.DOMAIN_BACK_END
    for key, value in dict_images.items():
        data[key] = domain + value
    return data
