from django.db import models


class PageResolverModel(models.Model):
    class Meta:
        abstract = True

    def get_paginated_page(self, queryset=None, *, paginate_by: int):
        """Here we can flexibly get page number by queryset itself to find its paginated page location"""

        if not queryset:
            queryset = self.__class__.objects.all().order_by('-created_at')

        ids = list(queryset.values_list('id', flat=True))
        try:
            index = ids.index(self.pk)
        except ValueError:
            return None

        page_number = (index // paginate_by) + 1
        return page_number
