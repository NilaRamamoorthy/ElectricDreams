from django import template

register = template.Library()

@register.filter(name="as_widget")
def as_widget(field, attrs):
    """
    Usage: {{ form.field|as_widget:"class:form-control,placeholder:First Name" }}
    """
    params = {}
    for attr in attrs.split(","):
        key, value = attr.split(":")
        params[key] = value
    return field.as_widget(attrs=params)
