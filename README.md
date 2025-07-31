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
Using of page-resolver to determine object's page location in paginated queryset.<br />
There is a two ways to do so:
1) Using abstract model `PageResolverModel`:<br />

   ```python
   from django_page_resolver.models import PageResolverModel
   
   class Comment(PageResolverModel):
       ...
   
   # OR
   
   class Post(PageResolverModel):
       ...
   ```
   And then you have next API:<br />
   ```python
   comment = Comment.objects.get(pk=27)
   comment_page_number = comment.get_page_from_queryset(order_by='-relevancy_value', items_per_page=15)
   # comment_page_number -> return 3
   
   # OR
   
   post = Post.objects.get(pk=120)
   comment_page_number_from_post = post.get_fk_paginated_page(target_child_instance=comment, order_by='-relevancy_value', items_per_page=15)
   # comment_page_number_from_post -> return 3
   ```
2) Using `page_resolver` class instance to do the same as was described above.<br />
   ```python
   from django_page_resolver.resolvers import page_resolver
   
   comment = Comment.objects.get(pk=27)
   comment_page_number = page_resolver.get_page_from_queryset(
    target_instance=comment, 
    order_by='-relevancy_value', 
    items_per_page=15
   )
   # comment_page_number -> return 3
   
   # OR
   
   post = Post.objects.get(pk=120)
   comment_page_number_from_post = page_resolver.get_page_from_nested_object(
     parent_instance=post,
     target_child_instance=comment,
     order_by='-relevancy_value',
     items_per_page=15
   )
   # comment_page_number_from_post -> return 3
   ```
**Parameters:**<br />

**`get_page_from_nested_object`:<br />**
- `parent_instance`: The parent model instance (e.g., Post). **Required and uses only from `page_resolver` instance**.<br />
- `target_child_instance`: The related model instance to locate (e.g., Comment). **Required**.<br />
- `siblings_qs`: Optional queryset to search in. If not provided, will use target_child_instance's model.<br />
- `related_name`: The related name on the parent that accesses the child objects (e.g., 'comments'). (By default takes `verbose_name_plural` from the Model's meta.)<br />
- `order_by`: Field used to order the queryset. Default is `None`.<br />
- `items_per_page`: The pagination size (number of items per page). **Required**.<br />

---

**`get_page_from_queryset`: <br />**
- `target_instance`: The instance whose page number we want to find. **Required and uses only from `page_resolver` instance**.<br />
- `queryset`: Optional queryset to search in. If not provided, will use target_instance's model. (By default takes default `__class__.objects.all()` queryset from the Model)<br />
- `order_by`: Field to order the queryset by. Default is `None`.<br />
- `items_per_page`: Number of items per page for pagination. **Required**.<br />

And then you have it!

---
Additionaly, you can have handsome dynamic HTMX+Bootstrap HTML paginator via templatetag!

**Prerequisites:**
1) [HTMX js-library.](https://htmx.org/docs/#installing)
2) [Bootstrap 5.0+](https://getbootstrap.com/docs/5.3/getting-started/download/)

Load `page_resolvers` templatetags into your HTML:
`{% load page_resolvers %}`

Then just pass `render_htmx_pagination` templatetag with htmx_target argument in your HTML code like so:

`{% render_htmx_pagination "#comment-list-body-js" %}`

**Note: You need to add `render_htmx_pagination` templatetag inside tag that has htmx_target selector which is you have specified. 
This is required because of rerender the pagination block with objects list while htmx-request. See examples in `examples` folder.**

That will render default [bootstrap pagination](https://getbootstrap.com/docs/5.3/components/pagination/) with HTMX and nice-UI large pages count support and i18n.
You can also add some classes to every element in pagination:

`{% render_bootstrap_pagination '#post-list-js' ul_class="some-outstanding-class" li_class="more-class" a_class="text-danger" %}`

And this is what you get then:

![Pagination example](https://s14.gifyu.com/images/bNSVQ.gif)

*Contributing*
---
You’re welcome to contribute to django-page-resolver by submitting pull requests, suggesting ideas, or helping improve the project in any way.
Let’s make this library better together!
