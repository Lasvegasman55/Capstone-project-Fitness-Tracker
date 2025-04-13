from django import template
from datetime import timedelta, date

register = template.Library()

@register.filter
def divide(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0
    
@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except ValueError:
        return 0
    
@register.filter
def subtract(value, arg):
    try:
        return float(value) - float(arg)
    except ValueError:
        return 0

@register.filter
def add_days(value, days):
    try:
        return value + timedelta(days=int(days))
    except (ValueError, TypeError):
        return value

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, None)