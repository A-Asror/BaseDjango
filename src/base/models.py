from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector  # TrigramSimilarity
from django.contrib.postgres.indexes import BrinIndex
from django.utils import timezone
from string import ascii_uppercase
from django.db import models


def get_search_vectors(fields: list):
    return tuple([SearchVector(filed, weight=next(iter(ascii_uppercase))) for filed in fields])


class BandManager(models.Manager):

    @property
    def get_search_fields(self):
        if hasattr(self.model, 'search_fields'):
            return self.get_queryset().search_fields
        return []

    def search(self, text):
        search_query = SearchQuery(text)
        search_vectors = get_search_vectors(self.get_search_fields)
        search_rank = SearchRank(search_vectors, search_query)
        return self.get_queryset().annotate(search=search_vectors).filter(search=search_query)


class BaseModel(models.Model):
    created_at = models.DateTimeField(editable=False, null=True, blank=True)
    updated_at = models.DateTimeField(editable=False, null=True, blank=True)
    objects = BandManager()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.localtime(timezone.now())
        self.updated_at = timezone.localtime(timezone.now())
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        indexes = (
            BrinIndex(fields=('created_at', 'updated_at')),
        )
        abstract = True


class ActiveVerifiedMode:
    active = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
