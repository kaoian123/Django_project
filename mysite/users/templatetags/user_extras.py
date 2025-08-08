from django import template

register = template.Library()


@register.filter
def mask_name(name: str) -> str:

    length = len(name)
    if length == 1:
        result = "Ｏ"
    elif length == 2:
        result = name[0] + "Ｏ"
    else:
        result = name[0] + "Ｏ" * (length - 2) + name[-1]

    return result
