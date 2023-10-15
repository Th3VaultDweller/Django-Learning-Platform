from django import template

register = template.Library()

@register.filter
def model_name(obj):
    """Template filter"""
    try:
        return obj._meta.model_name
    except AttributeError:
        return None