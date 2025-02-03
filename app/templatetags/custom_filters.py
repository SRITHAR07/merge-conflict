from django import template

register = template.Library()

@register.filter
def get_key(dictionary, key):
    """Custom template filter to dynamically get dictionary keys."""
    return dictionary.get(key, "")
