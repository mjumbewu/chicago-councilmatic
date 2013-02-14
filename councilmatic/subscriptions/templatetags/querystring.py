from django import template
from urllib import urlencode

register = template.Library()

@register.filter
def querystring(d):
    tuples = []
    for k, v in d.items():
        if isinstance(v, (list, tuple)):
            for i in v:
                tuples.append((k, i))
        else:
            tuples.append((k, v))
    return urlencode(tuples)
