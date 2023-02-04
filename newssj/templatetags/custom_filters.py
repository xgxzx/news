from django import template

register = template.Library()

words = ['Leo', 'captain', 'place']


@register.filter()
def censor(value):
    value_split = value.split()
    i = -1
    for j in value_split:
        i += 1
        if j in words:
            j = j.replace(j, '***')
            value_split[i] = j
    return f'{" ".join(value_split)}'
