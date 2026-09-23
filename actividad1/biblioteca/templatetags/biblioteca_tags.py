from django import template

register = template.Library()


@register.filter
def getattribute(obj, attr):

    try:
        valor = getattr(obj, attr)

        if callable(valor):
            return valor()

        return valor

    except AttributeError:
        return ""