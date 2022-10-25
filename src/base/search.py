from typing import Union


# class DynamicFilter(SearchFilter):
#     pass


class DefaultSearchFields:

    def __init__(self, search_fields: Union[str, list] = 'user', default_fields: Union[list] = None, costumize: Union[bool] = False):
        self.search_fields = search_fields
        self.default_fields = default_fields
        if self.default_fields is None:
            self.default_fields = ['{0}{1}username', '{0}{1}email', '{0}{1}first_name', '{0}{1}last_name']
        if costumize:
            if default_fields is not None:
                self.default_fields = default_fields
            self.customize_fields()

    def customize_fields(self):
        fields = []
        if type(self.search_fields) == list:
            for field in self.search_fields:
                for search_field in self.default_fields:
                    fields.append(search_field.format(field, '__'))
        self.field = fields

    @property
    def get_search_fields(self):  # filter_fields
        return self.field
