from typing import Union

from django.db.models import QuerySet, Model
from django.http import Http404
from django.shortcuts import get_object_or_404

from src.base.cache import AuthUserCache, GetSetDelaCacheANDUpdateVersion  # OLDVersionGetSetCacheData


# from base.search import DynamicFilter


class BaseCustomRequest(GetSetDelaCacheANDUpdateVersion, AuthUserCache):

    def __init__(
            self,
            model: Model,
            fd_kwargs: dict = dict(),  # filter_data_kwargs
            fd_args: tuple = tuple(),  # filter_data_kwargs
            annotate_data: Union[dict, None] = None,
            aggregate_data: Union[dict, None] = None,
            sr_fields: Union[tuple, None] = None,  # select_related_fields
            prefetch_related_data: Union[tuple, None] = None,
            last_func_bool: bool = False,
            first_func_bool: bool = False,
            start: Union[int, None] = None,
            end: Union[int, None] = None,
            q_filtered: bool = False,
    ):
        self.model = model
        self.filter_data_kwargs = fd_kwargs
        self.filter_data_args = fd_args
        self.q_filtered = q_filtered
        self.annotate_data = annotate_data
        self.aggregate_data = aggregate_data
        self.select_related_fields = sr_fields
        self.prefetch_related_data = prefetch_related_data
        self.last_func_bool = last_func_bool
        self.first_func_bool = first_func_bool
        self.start = start
        self.end = end

    @property
    def all(self) -> QuerySet:
        return self.model.objects.all()

    @property
    def limit_all(self) -> QuerySet:
        return self.model.objects.all()[:self.end]

    @property
    def offset_all(self) -> QuerySet:
        return self.model.objects.all()[self.start:]

    @property
    def paginate_all(self) -> QuerySet:
        return self.model.objects.all()[self.start:self.end]

    @property
    def get(self):
        return get_object_or_404(self.model, *self.filter_data_args, **self.filter_data_kwargs)

    @property
    def filter(self) -> QuerySet:
        if self.q_filtered:
            return self.model.objects.filter(self.filter_data_args, **self.filter_data_kwargs)
        return self.model.objects.filter(*self.filter_data_args, **self.filter_data_kwargs)

    @property
    def limit_filter(self) -> QuerySet:
        if self.q_filtered:
            return self.model.objects.filter(self.filter_data_args, **self.filter_data_kwargs)[:self.end]
        return self.model.objects.filter(*self.filter_data_args, **self.filter_data_kwargs)[:self.end]

    @property
    def offset_filter(self) -> QuerySet:
        if self.q_filtered:
            return self.model.objects.filter(self.filter_data_args, **self.filter_data_kwargs)[self.start:]
        return self.model.objects.filter(*self.filter_data_args, **self.filter_data_kwargs)[self.start:]

    @property
    def paginate_filter(self) -> QuerySet:
        if self.q_filtered:
            return self.model.objects.filter(self.filter_data_args, **self.filter_data_kwargs)[self.start:self.end]
        return self.model.objects.filter(*self.filter_data_args, **self.filter_data_kwargs)[self.start:self.end]

    @property
    def annotate_all(self) -> QuerySet:
        return self.model.objects.annotate(**self.annotate_data)

    @property
    def annotate_filtered(self) -> QuerySet:
        if self.q_filtered:
            return self.model.objects.filter(self.filter_data_args, **self.filter_data_kwargs).annotate(
                **self.annotate_data)
        return self.model.objects.filter(*self.filter_data_args, **self.filter_data_kwargs).annotate(
            **self.annotate_data)

    @property
    def filtered_count(self) -> dict:
        if self.q_filtered:
            print(self.filter_data_args)
            return self.model.objects.filter(self.filter_data_args, **self.filter_data_kwargs).count()
        return self.model.objects.filter(*self.filter_data_args, **self.filter_data_kwargs).count()


class SelectCustomRequest(BaseCustomRequest):
    @property
    def select_related_all(self) -> QuerySet:
        return self.model.objects.select_related(*self.select_related_fields)

    @property
    def select_related_and_annotate_all(self) -> QuerySet:
        return self.model.objects.select_related(*self.select_related_fields).annotate(**self.annotate_data)

    @property
    def select_related_and_filter(self) -> QuerySet:
        return self.model.objects.filter(*self.filter_data_args, **self.filter_data_kwargs).select_related(
            *self.select_related_fields)

    @property
    def select_related_and_annotate_filter(self) -> QuerySet:
        return self.model.objects.filter(*self.filter_data_args, **self.filter_data_kwargs).select_related(
            *self.select_related_fields).annotate(
            **self.annotate_data)

    @property
    def select_related_and_get(self):
        try:
            return self.model.objects.select_related(*self.select_related_fields).get(*self.filter_data_args,
                                                                                      **self.filter_data_kwargs)
        except self.model.DoesNotExist:
            raise Http404('No %s matches the given query.' % self.model._meta.object_name)

    @property
    def select_related_and_annotate_get(self):
        try:
            return self.model.objects.select_related(*self.select_related_fields).annotate(**self.annotate_data).get(
                *self.filter_data_args, **self.filter_data_kwargs)
        except self.model.DoesNotExist:
            raise Http404('No %s matches the given query.' % self.model._meta.object_name)


class PrefetchCustomRequest(BaseCustomRequest):

    @property
    def prefetch_related_all(self) -> QuerySet:
        return self.model.objects.prefetch_related(*self.prefetch_related_data)

    @property
    def prefetch_related_and_annotate_all(self) -> QuerySet:
        return self.model.objects.prefetch_related(*self.prefetch_related_data).annotate(**self.annotate_data)

    @property
    def prefetch_related_and_filter(self) -> QuerySet:
        return self.model.objects.filter(*self.filter_data_args, **self.filter_data_kwargs).prefetch_related(
            *self.prefetch_related_data)

    @property
    def prefetch_related_and_annotate_filter(self) -> QuerySet:
        return self.model.objects.filter(*self.filter_data_args, **self.filter_data_kwargs).prefetch_related(
            *self.prefetch_related_data).annotate(
            **self.annotate_data)

    @property
    def prefetch_related_get(self):
        try:
            return self.model.objects.prefetch_related(*self.prefetch_related_data).get(*self.filter_data_args,
                                                                                        **self.filter_data_kwargs)
        except self.model.DoesNotExist:
            raise Http404('No %s matches the given query.' % self.model._meta.object_name)

    @property
    def prefetch_related_and_annotate_get(self):
        try:
            return self.model.objects.annotate(**self.annotate_data).prefetch_related(
                *self.prefetch_related_data).get(*self.filter_data_args, **self.filter_data_kwargs)
        except self.model.DoesNotExist:
            raise Http404('No %s matches the given query.' % self.model._meta.object_name)


class SelectANDPrefetchCustomRequest(BaseCustomRequest):

    @property
    def select_related_and_prefetch_related_all(self) -> QuerySet:
        return self.model.objects.select_related(*self.select_related_fields).prefetch_related(
            *self.prefetch_related_data)

    @property
    def select_related_and_prefetch_related_and_annotate_all(self) -> QuerySet:
        return self.model.objects.select_related(*self.select_related_fields).prefetch_related(
            *self.prefetch_related_data).annotate(**self.annotate_data)

    @property
    def select_related_and_prefetch_related_and_filter(self) -> QuerySet:
        return self.model.objects.filter(*self.filter_data_args, **self.filter_data_kwargs).select_related(
            *self.select_related_fields).prefetch_related(*self.prefetch_related_data)

    @property
    def select_related_and_prefetch_related_and_annotate_filter(self) -> QuerySet:
        return self.model.objects.filter(*self.filter_data_args, **self.filter_data_kwargs).select_related(
            *self.select_related_fields).prefetch_related(*self.prefetch_related_data).annotate(**self.annotate_data)


class AllCustomRequest(SelectCustomRequest, PrefetchCustomRequest, SelectANDPrefetchCustomRequest):

    def __init__(self, *args, **kwargs):
        super(AllCustomRequest, self).__init__(*args, **kwargs)
