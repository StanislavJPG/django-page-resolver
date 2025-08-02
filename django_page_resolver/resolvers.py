__all__ = ['page_resolver']

from django_page_resolver.utils import _get_position_page


class FlexPageResolver:
    """
    This class contains utilities for determining the page number on which a particular object is located
    in a paginated list (either through a QuerySet or through a ForeignKey relationship).
    """

    @staticmethod
    def get_page_from_nested_object(
        parent_instance,
        target_child_instance,
        siblings_qs=None,
        *,
        related_name: str = None,
        order_by: str = None,
        items_per_page: int,
    ) -> int | None:
        """
        Determine the page number of a specific related (child) object within a paginated list
        of related objects belonging to a parent instance.

        Example:
            page_number = page_resolver.get_page_for_nested_object(
                parent_instance=post,
                target_child_instance=comment,
                related_name='comments',
                items_per_page=10
            )

        Args:
            - `parent_instance`: The parent model instance (e.g., Post). Required and uses only from `page_resolver` instance.
            - `target_child_instance`: The related model instance to locate (e.g., Comment). Required.
            - `siblings_qs`: Optional queryset to search in. If not provided, will use target_child_instance's model.
            - `related_name`: The related name on the parent that accesses the child objects (e.g., 'comments'). (By default takes `verbose_name_plural` from the Model's meta.)
            - `order_by`: Field used to order the queryset. Default is `None`.
            - `items_per_page`: The pagination size (number of items per page). Required.

        Returns:
            The page number where the target_child_instance is located, or None if not found.
        """
        if not related_name:
            related_name = target_child_instance.__class__._meta.verbose_name_plural.replace(' ', '_')

        if hasattr(parent_instance, related_name):
            if not siblings_qs:
                siblings_qs = getattr(parent_instance, related_name).all()

            if order_by:
                siblings_qs = siblings_qs.order_by(order_by)

            page_number = _get_position_page(
                siblings_qs, target_child_instance, order_by, items_per_page=items_per_page
            )

            return page_number

    @staticmethod
    def get_page_from_queryset(
        target_instance,
        queryset=None,
        *,
        order_by: str = None,
        items_per_page: int,
    ) -> int | None:
        """
        Determine the page number of a given object within a paginated, ordered queryset.

        Example:
            page_number = page_resolver.get_page_for_queryset_object(
                target_instance=comment,
                order_by='created_at',
                items_per_page=15
            )

        Args:
            - `target_instance`: The instance whose page number we want to find. Required and uses only from `page_resolver` instance.
            - `queryset`: Optional queryset to search in. If not provided, will use target_instance's model. (By default takes default `__class__.objects.all()` queryset from the Model)
            - `order_by`: Field to order the queryset by. Default is `None`.
            - `items_per_page`: Number of items per page for pagination. Required.

        Returns:
            The page number where the target_instance is located, or None if not found.
        """
        if queryset is None:
            queryset = target_instance.__class__.objects.all()

        if order_by:
            queryset = queryset.order_by(order_by)

        page_number = _get_position_page(queryset, target_instance, order_by, items_per_page=items_per_page)

        return page_number


page_resolver = FlexPageResolver()
