# blog/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='is_admin')
def is_admin(user):
    return user.groups.filter(name="Administrateurs").exists()
