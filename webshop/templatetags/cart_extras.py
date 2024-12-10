from django import template

register = template.Library()

# This is used to multiply quantity and price of the product in a cart
@register.filter
def multiply(value, arg):
    return value * arg