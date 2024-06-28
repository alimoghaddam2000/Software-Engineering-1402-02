from django import template

register = template.Library()

@register.filter
def index(arr, idx):
    try:
        return arr[int(idx)]
    except (IndexError, ValueError, TypeError):
        return None
