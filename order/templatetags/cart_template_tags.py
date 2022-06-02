from django import template
from order.models import Order, OrderItem

register = template.Library()
@register.filter
def cart_view(user):
   
    cart=OrderItem.objects.filter(user=user,ordered=False)
    
    return cart

@register.filter
def cart_item_total(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].total_price()
        return 0

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
        return 0
@register.filter
def sort_by(queryset, order):
    return queryset.order_by(order)