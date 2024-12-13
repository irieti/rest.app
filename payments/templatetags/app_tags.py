from django import template

register = template.Library()


@register.filter
def first_matching_order_item(order_items, item):
    for order_item in order_items:
        if order_item.menu_item.id == item.id:
            return order_item
    return None
