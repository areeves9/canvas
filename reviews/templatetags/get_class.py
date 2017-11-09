from django import template

register = template.Library()


@register.filter('get_class')
def get_class(instance):
    return instance.__class__.__name__
