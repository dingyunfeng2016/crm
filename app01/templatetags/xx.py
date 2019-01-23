from django import template

register = template.Library()
from django.utils.safestring import mark_safe

@register.simple_tag
def sql_list(arg):
    str = "<select>"

    for i in range(1,arg+1):
        temp = "<option id={0}> {1} 平方是{2} </option>".format(i,i,i*i)
        str = str + temp

    str = str + "</select>"

    return mark_safe(str)

