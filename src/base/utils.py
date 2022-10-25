from typing import Union

from django.db.models import Model, QuerySet, Q
from pydantic import BaseModel

from src.base.ORM import AllCustomRequest

orm = AllCustomRequest


def update(obj: Model, payload: Union[BaseModel, dict]) -> Model:
    if type(payload) is not dict:
        payload = payload.dict(exclude_none=True)
    # update_fields = obj.update_fields(obj)
    # if hasattr(obj, attr) and attr in update_fields and type(new_value) is not dict:
    for attr, new_value in payload.items():
        if hasattr(obj, attr) and type(new_value) is not dict:
            setattr(obj, attr, new_value)
        elif hasattr(obj, attr) and type(new_value) is dict:
            _update_fields_foreign_key_or_one_to_one(obj, attr, new_value)
    obj.save()
    return obj


def _update_fields_foreign_key_or_one_to_one(obj, fk_attr, payload: dict):
    fk_obj = getattr(obj, fk_attr)
    # update_fields = fk_obj.update_fields(obj)
    # if hasattr(fk_obj, attr) and attr in update_fields:
    for attr, value in payload.items():
        if hasattr(fk_obj, attr):
            setattr(fk_obj, attr, value)
    fk_obj.save()


def remove_null_from_Q_object(q_data):
    """
    задача этой функции удалить все Q объекты, где значение атрибута Q, равна на None Q(attr=None)
    result: если все атрибуты Q равны на None Q(attr=None), то вернет пустой tuple и False
     иначе если хоть 1 атрибут Q не равно на None, то он вернет объект Q и True
     True и False нужен узнасть чтоб для фильтрации надоли фильтровать специально под Q объектов
    """
    for num in range(len(q_data) - 1, -1, -1):
        if type(q_data.children[num]) is tuple:
            if type(q_data.children[num][1]) is type(None):
                del q_data.children[num]
        elif type(q_data.children[num]) is Q:
            remove_null_from_Q_object(q_data.children[num])
    if len(q_data) == 0:
        return tuple(), False
    return q_data, True


def update_data(data: QuerySet, model: Union[Model, None] = None, count: Union[QuerySet, None] = None) -> list:
    """
    data: это либо отфилтрованный(.filter()) или целиком взятые(.all()) объекты
    model: это дочерной класс models.Model, он нужен лиж в том случаи, если надо узнать общее кол-во объектов этой
     сущности из БД
    result: вернет либо общее кол-во из data или кол-во сущностей из БД, но если общее кол-во из data равна 0, то ключ
     count не будет добавиться в результат
    """
    list_data: list = list(data)
    if model is not None:
        count = model.objects.count()
        if count != 0:
            list_data.append({"count": count})
    elif count != 0 and count is not None:
        list_data.append({"count": count})
    return list_data


def check_paginate(
        model: Model,
        page: Union[int, None],
        filter_data_kwargs: Union[dict, None] = dict(),
        filter_data_args: Union[tuple, None] = tuple(),
        q_filtered: bool = False,
        page_size: int = 15
):
    """
    page: страница пагинации
    filter_data_kwargs: данные для фильтрации в виде словаря
    filter_data_args: данные для фильтрации в виде tuple
    q_filtered: если filter_data_args=(Sum(...), ...) и в args есть Q()-объект(ы) то ставить q_filtered=True
    page_size: кол-во объектов в 1 запроск, поумолчанию=15
    result: проверить наличие фильтрции и пагинации, и исходя от этого делать раздичные проаерки и выводы
    """
    # если нет никмких параиетров, то вывести данных кол-вом с page_size и добавить общее кол-во объектов
    if page is None and bool(filter_data_kwargs) is False and bool(filter_data_args) is False:
        data: QuerySet = orm(model, end=page_size).limit_all
        return update_data(data, model)
    # если есть что фильтровать,и нет страницы пагинации,то фильтровать и вывести объекты кол-вом указанном в page_size
    elif page is None and bool(filter_data_kwargs or filter_data_args) is True:
        data: QuerySet = orm(model, fd_args=filter_data_args, fd_kwargs=filter_data_kwargs, end=page_size,
                             q_filtered=q_filtered).limit_filter
        count = orm(model, fd_args=filter_data_args, fd_kwargs=filter_data_kwargs, end=page_size,
                    q_filtered=q_filtered).filter.count()
        return update_data(data, count=count)
    # если есть данные для фильтрации и страница(page) не пуст то отфильтровать и передать объекты в соответсвии с page
    elif bool(filter_data_kwargs or filter_data_args) is True and page is not None:
        start = page_size * page
        end = start + page_size
        data: QuerySet = orm(model, fd_kwargs=filter_data_kwargs, fd_args=filter_data_args, start=start, end=end,
                             q_filtered=q_filtered).paginate_filter
        return update_data(data)
    start = page_size * page
    end = start + page_size
    return orm(model, start=start, end=end).paginate_all
