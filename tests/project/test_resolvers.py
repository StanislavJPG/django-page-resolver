import random

from django.core.paginator import Paginator
from django.test import TestCase
from factory.django import get_model

from django_page_resolver.utils import _get_position_page
from tests.factories import CommentFactory, PostFactory


class TestApp(TestCase):
    def setUp(self):
        CommentFactory.create_batch(size=150)
        comment_model = get_model('app', 'Comment')
        self.comments = comment_model.objects.all().order_by('created_at')
        self.paginate_by = 7
        self.random_range_number = random.randint(0, 149)

    def _get_paginator(self, queryset, position_page: int):
        p = Paginator(queryset, self.paginate_by)
        paginated_page = p.get_page(position_page)
        return p, paginated_page

    def test_position_page_util(self):
        comments = self.comments
        target_comment = comments[self.random_range_number]
        position_page = _get_position_page(comments, target_comment, items_per_page=self.paginate_by)
        paginator, paginated_page = self._get_paginator(comments, position_page)

        self.assertIn(target_comment, paginated_page.object_list)
        self.assertEqual(position_page, paginator.page(position_page).number)

    def test_models_resolver_page_from_nested_object(self):
        post = PostFactory.create()
        comments = CommentFactory.create_batch(size=75, post=post)
        target_comment = comments[random.randint(0, 74)]
        position_page = post.get_page_from_nested_object(
            target_child_instance=target_comment, items_per_page=self.paginate_by
        )
        paginator, paginated_page = self._get_paginator(post.comments.all(), position_page)

        self.assertIn(target_comment, paginated_page.object_list)
        self.assertEqual(position_page, paginator.page(position_page).number)

    def test_models_resolver_page_from_queryset(self):
        comments = self.comments
        target_comment = comments[self.random_range_number]

        position_page = target_comment.get_page_from_queryset(queryset=comments, items_per_page=self.paginate_by)
        paginator, paginated_page = self._get_paginator(comments, position_page)
        self.assertIn(target_comment, paginated_page.object_list)
