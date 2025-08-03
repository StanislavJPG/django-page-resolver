from django.template import Template, Context
from django.test import TestCase, RequestFactory

from tests.app.factories import CommentFactory


class TestTemplateTags(TestCase):
    def setUp(self):
        self.comment = CommentFactory.create()

    def test_classes_by_lookup_url(self):
        comment = self.comment
        template = Template(
            '<| load page_resolvers |><| classes_by_lookup_url instance_pk={comment_pk} url_lookup="{url_lookup}" |>'.format(
                comment_pk=comment.pk, url_lookup='comment'
            )
            .replace('<|', '{%')
            .replace('|>', '%}')
        )
        factory = RequestFactory()
        request = factory.get(f'/?comment={comment.pk}')
        context = Context({'request': request})
        template = template.render(context)
        self.assertEqual(template, 'scroll-instance-1 bg-warning-subtle rounded fadeDiv')
