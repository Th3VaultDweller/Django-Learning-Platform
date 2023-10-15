from django import template

register = template.Library()


@register.filter
def model_name(obj):
    """Template filter"""
    # In templates it is used as object|model_name
    # to get a model name for an object
    try:
        return obj._meta.model_name
    except AttributeError:
        return None
