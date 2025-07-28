from django.db import models


__all__ = ['PageResolverModel']


class PageResolverModel(models.Model):
    class Meta:
        abstract = True

    def get_page_for_nested_object(
        self, target_child_instance, related_name: str, order_by='-created_at', *, paginate_by: int
    ):
        """
        Imagine that we have model Post. And we have to find specific comment's page of its post.

        We can do next steps:
        post = Post.objects.get(pk=pk)
        comment = post.comments.first()
        comment_page = post.get_fk_paginated_page(comment, 'comments', paginate_by=10)
        """

        if hasattr(self, related_name):
            siblings_qs = getattr(self, related_name).all().order_by(order_by)
            ids = list(siblings_qs.values_list('id', flat=True))

            try:
                index = ids.index(target_child_instance.id)
            except ValueError:
                return None

            page_number = (index // paginate_by) + 1
            return page_number

    def get_page_for_queryset_object(self, queryset=None, order_by='-created_at', *, paginate_by: int):
        """
        Here we can flexibly get page number by queryset itself to find its paginated page location
        """

        if not queryset and order_by:
            queryset = self.__class__.objects.all().order_by(order_by)

        ids = list(queryset.values_list('id', flat=True))
        try:
            index = ids.index(self.pk)
        except ValueError:
            return None

        page_number = (index // paginate_by) + 1
        return page_number
