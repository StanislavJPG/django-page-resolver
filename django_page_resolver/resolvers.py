__all__ = ['page_resolver']


class FlexPageResolver:
    """
    This class contains utilities for determining the page number on which a particular object is located
    in a paginated list (either through a QuerySet or through a ForeignKey relationship).
    """

    @staticmethod
    def get_page_for_nested_object(
        parent_instance,
        target_child_instance,
        related_name: str,
        order_by: str = '-created_at',
        *,
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
            parent_instance: The parent model instance (e.g., Post).
            target_child_instance: The related model instance to locate (e.g., Comment).
            related_name: The related name on the parent that accesses the child objects (e.g., 'comments').
            order_by: Field used to order the queryset. Default is '-created_at'.
            items_per_page: The pagination size (number of items per page).

        Returns:
            The page number (1-based) where the target_child_instance is located, or None if not found.
        """
        if hasattr(parent_instance, related_name):
            related_qs = getattr(parent_instance, related_name).all().order_by(order_by)
            related_ids = list(related_qs.values_list('id', flat=True))

            try:
                child_index = related_ids.index(target_child_instance.id)
            except ValueError:
                return None

            page_number = (child_index // items_per_page) + 1
            return page_number

    @staticmethod
    def get_page_for_queryset_object(
        target_instance,
        items_per_page: int,
        queryset=None,
        order_by: str = '-created_at',
    ) -> int | None:
        """
        Determine the page number of a given object within a paginated, ordered queryset.

        Example:
            page_number = page_resolver.get_page_for_queryset_object(
                target_instance=comment,
                items_per_page=15
            )

        Args:
            target_instance: The instance whose page number we want to find.
            items_per_page: Number of items per page for pagination.
            queryset: Optional queryset to search in. If not provided, will use target_instance's model.
            order_by: Field to order the queryset by. Default is '-created_at'.

        Returns:
            The 1-based page number where the target_instance is located, or None if not found.
        """
        if queryset is None:
            queryset = target_instance.__class__.objects.all().order_by(order_by)

        ordered_ids = list(queryset.values_list('id', flat=True))
        try:
            instance_index = ordered_ids.index(target_instance.id)
        except ValueError:
            return None

        page_number = (instance_index // items_per_page) + 1
        return page_number


page_resolver = FlexPageResolver()
