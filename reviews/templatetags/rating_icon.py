from django import template
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter
def rating_icon(rating):
    return mark_safe('<span class="glyphicon glyphicon-star"></span>' * rating)
