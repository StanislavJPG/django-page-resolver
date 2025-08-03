from django import template
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.simple_tag(takes_context=True)
def classes_by_lookup_url(context, instance_pk, url_lookup):
    """
    Use this simple_tag inside class=""
    Example = class="row {% classes_by_lookup_url comment 'comment' %}"
    """
    request = context['request']
    identifier = f'scroll-instance-{instance_pk}'
    return f'{identifier} bg-warning-subtle rounded fadeDiv' if request.GET.get(url_lookup) == str(instance_pk) else ''


@register.simple_tag(takes_context=True)
def register_scroll_obj_unique_pk(context, instance_pk):
    request = context['request']
    if str(instance_pk) in [value for value in request.GET.values()]:
        return format_html(f'<script>window.scrollToInstance = "{instance_pk}";</script>')
    return ''


@register.simple_tag(takes_context=True)
def render_htmx_pagination(context, htmx_target, **kwargs):
    """

    Render a HTMX User-friendly bootstrap pagination with support of large count of pages.

    Example::
    {% render_bootstrap_pagination '#post-list-js' %}

    Or using class target::
    {% render_bootstrap_pagination '.post-list' %}

    Also, you can use it with additional class kwargs, like so::
    {% render_bootstrap_pagination '#post-list-js' ul_class="some-outstanding-class" li_class="more-class" a_class="text-danger" %}

    """
    page_obj = context.get('page_obj')
    request = context.get('request')

    ul_class = kwargs.get('ul_class', '')
    li_class = kwargs.get('li_class', '')
    a_class = kwargs.get('a_class', '')

    if not page_obj or page_obj.paginator.num_pages <= 1:
        return ''

    def page_link(page, active=False, disabled=False, label=None):
        """Helper to build one-page link item"""
        classes = [f'page-item {li_class}']
        if active:
            classes.append('active')
        if disabled:
            classes.append('disabled')

        href = 'javascript:void(0);'
        if not disabled and not active:
            # build hx-get URL with page param
            sep = '&' if request.GET else '?'
            url = f'{request.get_full_path()}{sep}page={page}'
        else:
            url = href

        link_label = label if label is not None else str(page)

        return format_html(
            '<li class="{classes}"><a class="page-link{disabled_class} {a_class}" href="{href}" '
            'hx-get="{hx_get}" hx-target="{hx_target}" hx-select="{hx_select}" hx-swap="outerHTML">{label}</a></li>',
            classes=' '.join(classes),
            disabled_class=' disabled' if disabled else '',
            a_class=a_class,
            href=href,
            hx_get=url if not (active or disabled) else '',
            hx_target=f'{htmx_target}',
            hx_select=f'{htmx_target}',
            label=link_label,
        )

        # Start building the pagination html

    default_ul_classes = 'justify-content-center flex-wrap'
    html = [f'<nav><ul class="pagination {default_ul_classes if not ul_class else ul_class}">']

    # Previous button
    if page_obj.has_previous():
        html.append(page_link(page_obj.previous_page_number(), label=_('Previous')))
    else:
        html.append(page_link(None, disabled=True, label=_('Previous')))

    # Page numbers with ellipsis logic
    current = page_obj.number
    last = page_obj.paginator.num_pages

    for page in page_obj.paginator.page_range:
        if page == 1 or page == last or (current - 2 <= page <= current + 2):
            html.append(page_link(page, active=(page == current)))
        elif page == current - 3 or page == current + 3:
            # Add ellipsis but only once for each side — so skip repeats
            if not html or html[-1] != '<li class="page-item disabled"><span class="page-link">…</span></li>':
                html.append('<li class="page-item disabled"><span class="page-link">…</span></li>')

    # Next button
    if page_obj.has_next():
        html.append(page_link(page_obj.next_page_number(), label=_('Next')))
    else:
        html.append(page_link(None, disabled=True, label=_('Next')))

    html.append('</ul></nav>')

    return format_html(''.join(html))
