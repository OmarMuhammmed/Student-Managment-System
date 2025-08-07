from django import template

register = template.Library()

@register.filter
def lookup(dictionary, key):
    """Template filter to lookup dictionary values"""
    return dictionary.get(key, False)

@register.filter
def mul(value, arg):
    """Template filter to multiply two values"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0