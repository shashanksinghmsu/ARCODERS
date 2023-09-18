from django import template

register = template.Library()

@register.filter
def splitByComma(value,ani):
    return value.split(",")


@register.filter
def dictonary(h, key):
    return h[key]