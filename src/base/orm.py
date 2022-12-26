from typing import List, Optional, Tuple, Union

from django.db import models
from django.http import Http404

from src.utils.exceptions import ValidationError


def get_object_or_404(
    model,
    only_fields: Optional[Union[list, tuple, None]] = None,
    select_related: Optional[Union[list, tuple, None]] = None,
    prefetch_related: Optional[Union[list, tuple, None]] = None,
    *args,
    **kwargs,
):
    queryset = model.objects.all()
    if select_related is not None:
        queryset = queryset.select_related(*select_related)
    if prefetch_related is not None:
        queryset = queryset.prefetch_related(*prefetch_related)
    try:
        if only_fields is not None:
            return queryset.only(*only_fields).get(*args, **kwargs)
        return queryset.get(*args, **kwargs)
    except model.DoesNotExist:
        raise Http404("No %s matches the given query." % model._meta.object_name)


def exists_model_from_data(model, raise_exception: bool = False, **kwargs) -> bool:
    """Если raise_exception=True то выдаст ошибку, это похож как serializer.is_valid(raise_exception)."""
    if not issubclass(model, models.Model):
        raise ValidationError(message=f"{model.__class__.__name__} is not a subclass models.Model")
    exist = model.objects.filter(**kwargs).exists()
    if raise_exception and not exist:
        raise Http404("No %s matches the given query." % model._meta.object_name)
    return exist


def base_sql_request(
    model,
    filter_data: Optional[dict] = None,
    q_filter_data: Optional[Union[tuple, list]] = models.Q(),
    execute_data: Optional[dict] = None,
    q_execute_data: Optional[dict] = models.Q(),
    select_related: Optional[Union[list, tuple]] = (None,),
    prefetch_related: Optional[Union[list, tuple]] = (None,),
    only: Optional[Union[list, tuple]] = None,
    defer: Optional[Union[list, tuple]] = None,
    annotate: Optional[dict] = None,
    order_by: Optional[Union[List[str], Tuple[str]]] = None,
):
    qs = (
        model.objects.all()
        .select_related(*select_related)
        .prefetch_related(*prefetch_related)
        .filter(q_filter_data, **filter_data if filter_data is not None else {})
        .annotate(**annotate if annotate is not None else {})
        .only(*only if only is not None else ())
        .defer(*defer if defer is not None else ())
        .order_by(*order_by if order_by is not None else ())
    )

    return qs
