import math
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def rating_icon(rating):
    if rating == '':
        return ''
    else:
        new_rating = math.modf(float(rating))
        rem = 5 - new_rating[1]
        if new_rating[0] >= 0.5 and new_rating[0] <= 0.9:
            return mark_safe('<i class="text-secondary fas fa-star"></i>' * int(rating)) + mark_safe('<i class="text-secondary fas fa-star-half-alt"></i>')
        else:
            return mark_safe('<i class="text-secondary fas fa-star"></i>' * int(rating)) + mark_safe('<i class="far fa-star"></i>' * int(rem))
