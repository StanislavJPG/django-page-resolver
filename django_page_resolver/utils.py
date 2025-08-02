def _get_position_page(qs, target, order_field: str = None, *, items_per_page: int):
    if not order_field:
        order_field = 'created_at'

    descending = order_field.startswith('-')
    field_name = order_field.lstrip('-')

    if not hasattr(target, field_name):
        raise ValueError(f"Target object does not have field '{field_name}'")

    lookup = '__gt' if descending else '__lt'
    position = qs.filter(**{field_name + lookup: getattr(target, field_name)}).count()

    page = position // items_per_page + 1

    return page
