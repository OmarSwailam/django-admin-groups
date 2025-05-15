from django import template
from django.utils.text import slugify

register = template.Library()

@register.filter
def to_slug(value):
    return slugify(value)