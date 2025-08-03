import random

from django.core.paginator import Paginator
from django.template import Template, Context
from django.test import TestCase, RequestFactory
from django.utils.html import format_html

from tests.app.factories import CommentFactory


class TestTemplateTags(TestCase):
    def setUp(self):
        self.comment = CommentFactory.create()

    @staticmethod
    def _get_ready_template_from_templatetag(
        templatetag_name: str,
        str_request: str = '/',
        remaining_template: str = '',
        template_context: dict = None,
        **kwargs,
    ):
        template_kwargs = ' '.join(f'{k}={v}' if not isinstance(v, str) else f'{k}="{v}"' for k, v in kwargs.items())
        template = Template(
            '<| load page_resolvers |><| {templatetag_name} {template_kwargs} |>{remaining_template}'.format(
                templatetag_name=templatetag_name,
                template_kwargs=template_kwargs,
                remaining_template=remaining_template,
            )
            # to prevent screening
            .replace('<|', '{%')
            .replace('|>', '%}')
        )
        factory = RequestFactory()
        request = factory.get(str_request)
        template_context = template_context or {}
        context = Context({'request': request, **template_context})
        return template.render(context)

    def test_classes_by_lookup_url(self):
        comment = self.comment
        template = self._get_ready_template_from_templatetag(
            templatetag_name='classes_by_lookup_url',
            str_request=f'/?comment={comment.pk}',
            instance_pk=comment.pk,
            url_lookup='comment',
        )
        self.assertEqual(template, 'scroll-instance-1 bg-warning-subtle rounded fadeDiv')

    def test_register_scroll_obj_unique_pk(self):
        comment = self.comment
        template = self._get_ready_template_from_templatetag(
            templatetag_name='register_scroll_obj_unique_pk',
            str_request=f'/?comment={comment.pk}',
            instance_pk=comment.pk,
        )
        self.assertEqual(template, '<script>window.scrollToInstance = "1";</script>')

    def test_render_htmx_pagination(self):
        comments = CommentFactory.create_batch(35)
        paginator = Paginator(comments, 7)
        page_obj = paginator.get_page(random.randint(1, paginator.num_pages - 1))

        remaining_template = format_html('<div id="post-list-js"></div>')
        template = self._get_ready_template_from_templatetag(
            templatetag_name='render_htmx_pagination',
            remaining_template=remaining_template,
            template_context={'page_obj': page_obj},
            htmx_target='#post-list-js',
        )
        self.assertNotEqual('', template)  # empty string means that something gone wrong
        self.assertIn('pagination justify-content-center flex-wrap', template)
