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
        empty_stars = rem - 1
        if new_rating[0] >= 0.5 and new_rating[0] <= 0.9:
            return mark_safe('<i style="color: #6EB257" class="fas fa-star"></i>' * int(new_rating[1])) + mark_safe('<i style="color: #6EB257" class="fas fa-star-half-alt"></i>') + mark_safe('<i  style="color: #6EB257" class="far fa-star"></i>' * int(empty_stars))
        else:
            return mark_safe('<i style="color: #6EB257" class="fas fa-star"></i>' * int(new_rating[1])) + mark_safe('<i  style="color: #6EB257" class="far fa-star"></i>' * int(rem))
