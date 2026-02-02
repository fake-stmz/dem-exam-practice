from django import template

register = template.Library()

@register.filter
def discount(value, discount_value):
    return value - (value * discount_value / 100)