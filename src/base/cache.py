import re
from datetime import timedelta

from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.utils import timezone


class OLDVersionGetSetCacheData:
    CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

    @property
    def str_key(self):
        list_key = [self.filter_data, self.annotate_data, self.select_related_fields, self.prefetch_related_data, self.request.query_params]
        str_list_key = ''.join(str(key) for key in list_key)
        key = ''.join(dict.fromkeys(str_list_key))
        return key

    @property
    def get_model_name(self):  # рботает только в POST and Patch методах
        return self.model

    @property
    def get_correct_cache_key(self):
        remove_duplicate = self.str_key
        not_correct_key = re.sub(r'[^a-zA-Z0-9]', '', str(remove_duplicate))
        search_data = 'search' + self.request.query_params.get('search', '')
        return self.get_model_name + not_correct_key + search_data

    @property
    def get_del_valid_key(self):
        model_name = self.get_model_name
        # print(model_name, 1)
        no_valid_keys = set(cache.keys(model_name+'*'))
        # print(no_valid_keys, 2)
        no_valid_keys_pk = set(cache.keys(model_name+'pk*'))
        # print(no_valid_keys_pk, 3)
        update_keys = cache.keys(model_name+f'pk{self.filter_data}*')
        # print(update_keys, 4)
        valid_keys = no_valid_keys.difference(no_valid_keys_pk)
        # print(valid_keys, 5)
        # print(list(valid_keys)+list(update_keys), 6)
        return list(valid_keys)+list(update_keys)

    @property
    def get_cache(self):
        # a = self.get_del_valid_key
        return cache.get(self.get_correct_cache_key)

    def del_cache(self):
        cache.delete_many(self.get_del_valid_key)

    # @property
    def set_cache(self, data_cached):
        correct_key = self.get_correct_cache_key
        print(correct_key)
        cache.set(correct_key, data_cached, self.CACHE_TTL)
        return data_cached


class AuthUserCache:
    @classmethod
    def set_payload_cache(cls, key, payload):
        cache.set(key, payload, 60*30)

    def del_cache_user(self, key):
        cache.delete(key)

    @classmethod
    def get_cache(cls, key):
        return cache.get(key)

    def del_cache_data(self, jwt=None, pk=None):
        if jwt is None:
            jwt = self.request.user.jwt.access
        if pk is None:
            pk = self.request.user.pk
        filter_data = self.filter_data_kwargs
        self.filter_data_kwargs = {'pk': pk}
        self.del_cache()
        self.filter_data_kwargs = filter_data
        self.del_cache_user(jwt)


class GetSetDelaCacheANDUpdateVersion:
    # CACHE_TTL = 60*60*24*200
    CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
    version = 2

    @property
    def str_key(self):
        list_key = [self.filter_data_kwargs, self.annotate_data, self.select_related_fields, self.prefetch_related_data, self.request.query_params]
        str_list_key = ''.join(str(key) for key in list_key)
        key = ''.join(dict.fromkeys(str_list_key))
        return key

    @property
    def get_model_name(self):  # рботает только в POST and Patch методах
        return self.model

    @property
    def get_correct_cache_key(self):
        remove_duplicate = self.str_key
        not_correct_key = re.sub(r'[^a-zA-Z0-9]', '', str(remove_duplicate))
        search_data = 'search' + self.request.query_params.get('search', '')
        return self.get_model_name + not_correct_key + search_data

    @property
    def get_del_valid_key(self):
        model_name = self.get_model_name
        print(model_name, 1)
        no_valid_keys = set(cache.keys(model_name+'*'))
        print(no_valid_keys, 2)
        no_valid_keys_pk = set(cache.keys(model_name+'pk*'))
        print(no_valid_keys_pk, 3)
        update_keys = cache.keys(model_name +f'pk{self.filter_data_kwargs}*')
        print(update_keys, 4)
        valid_keys = no_valid_keys.difference(no_valid_keys_pk)
        print(valid_keys, 5)
        print(list(valid_keys)+list(update_keys), 6)
        return list(valid_keys)+list(update_keys)

    def get_cache(self, **kwargs):
        # cache.delete('TestModelpk1QueryDictsearch')
        # print(self.get_correct_cache_key)
        version = kwargs.get('version', None)
        if version is None:
            version = 1
        return cache.get(self.get_correct_cache_key, version=version)

    def set_cache(self, data_cached):
        # print(data_cached)
        list_id = []
        try:
            list_id.append(data_cached['id'])
        except TypeError:
            [list_id.append(obj['id']) for obj in data_cached]
        correct_key = self.get_correct_cache_key
        print(correct_key)
        print(list_id)
        cache.set(correct_key, data_cached, self.CACHE_TTL)
        cache.set(correct_key, list_id, self.CACHE_TTL, self.version)

    def del_cache(self, **kwargs):
        pk = kwargs.get('pk', None)
        correct_keys = self.get_del_valid_key
        print(correct_keys)
        print(pk)
        list_del_keys = []
        if pk is None:
            list_del_keys.append(self.get_correct_cache_key)
        cache_data = cache.get_many(correct_keys, version=2)
        print(cache_data)
        for key, data in cache_data.items():
            for id_obj in data:
                if id_obj == pk:
                    list_del_keys.append(key)
                    break
        print(list_del_keys)
        if len(list_del_keys) >= 1:
            cache.delete_many(list_del_keys)

    def del_cache_data(self, **kwargs):
        pk = kwargs.get('pk', None)
        if pk is None:
            pk = ''
        filter_data = self.filter_data_kwargs
        self.filter_data_kwargs = pk
        self.del_cache(**kwargs)
        self.filter_data_kwargs = filter_data
