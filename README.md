django-page-resolver
=====
[![PyPI Downloads](https://static.pepy.tech/badge/django-page-resolver)](https://pepy.tech/projects/django-page-resolver)

This is python utility for Django that helps determine the page number on which a specific model instance appears within a paginated queryset or related object set.
It also includes a Django templatetag for rendering HTMX + Bootstrap-compatible pagination with support for large page ranges and dynamic page loading.

Imagine you're working on a Django project where you want to highlight or scroll to a specific item on a paginated list — for example, highlighting a comment on a forum post. 
To do this, you need to calculate which page that comment appears on and then include that page number in the URL, like so:

`localhost:8000/forum/posts/151/?comment=17&page=4`

This allows you to directly link to the page where the target item exists.
Instead of manually figuring this out, use `FlexPageResolver` or `PageResolverModel`.

See `Usage`.

*Installation*
---
```bash
pip install django-page-resolver
```
Then you have to pass `django_page_resolver` to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
  ...
  'django_page_resolver',
  ...
]
```

*Usage*
----
Using of page-resolver to determing object's page location in paginated queryset.
There is a two ways to do so:
1) Using model mixin `PageResolverModel`:
   ```python
   from django_page_resolver.models import PageResolverModel
   
   class Comment(PageResolverModel):
       ...
   # or
   class Post(PageResolverModel):
       ...
   ```
   And then have next API:
   ```python
   comment = Comment.objects.get(pk=27)
   comment_page_number = comment.get_page_from_queryset(order_by='-relevancy_value', paginate_by=15)
   # comment_page_number -> return 3
   
   # OR
   
   post = Post.objects.get(pk=120)
   comment_page_number_from_post = post.get_fk_paginated_page(target_child_instance=comment, related_name='comments', order_by='-relevancy_value', paginate_by=15)
   # comment_page_number_from_post -> return 3
   ```
2) Using `page_resolver` class instance to do the same as was described above.
   ```python
   from django_page_resolver.resolvers import page_resolver
   
   comment = Comment.objects.get(pk=27)
   comment_page_number = page_resolver.get_page_from_queryset(target_instance=comment, order_by='-relevancy_value', items_per_page=15)
   # comment_page_number -> return 3
   
   # OR
   
   post = Post.objects.get(pk=120)
   comment_page_number_from_post = page_resolver.get_page_from_nested_object(
     parent_instance=post,
     target_child_instance=comment,
     related_name='comments',
     order_by='-relevancy_value',
     items_per_page=15
   )
   # comment_page_number_from_post -> return 3
   ```
And you have it!

---
You can have handsome dynamic HTMX+Bootstrap HTML paginator via templatetag!

**Prerequisites:**
1) [HTMX js-library.](https://htmx.org/docs/#installing)
2) [Bootstrap 5.0+](https://getbootstrap.com/docs/5.3/getting-started/download/)

Load `page_resolvers` templatetags into your HTML:
`{% load page_resolvers %}`

Then just pass `render_htmx_pagination` templatetag with htmx_target argument in your HTML code like so:

`{% render_htmx_pagination "#comment-list-body-js" %}`

That will render default [bootstrap pagination](https://getbootstrap.com/docs/5.3/components/pagination/) with HTMX and nice-UI large pages count support and i18n.
You can also add some classes to every element in pagination:

`{% render_bootstrap_pagination '#post-list-js' ul_class="some-outstanding-class" li_class="more-class" a_class="text-danger" %}`

And this is what you get then:

![Pagination example](https://s14.gifyu.com/images/bNSVQ.gif)

*Contributing*
---
You’re welcome to contribute to django-page-resolver by submitting pull requests, suggesting ideas, or helping improve the project in any way.
Let’s make this library better together!
