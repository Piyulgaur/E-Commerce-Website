from atexit import register
from django import template

register=template.Library()

@register.filter(name='cart_quantity')
def cart_quantity(product,cart):
    keys=cart.keys()
    for id in keys:
        if int(id)==product.id:
            return cart.get(id)
    return 0;

@register.filter(name='total_price')
def total_cart_price(products,cart):
    sum=0
    for p in products:
        sum=sum+p.price*cart_quantity(p,cart)

    return sum