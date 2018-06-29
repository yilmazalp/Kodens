from django import template
from polls.models import UserProfile
register = template.Library()


@register.simple_tag
def update_point(data):
    mytext = " ".join(data.split("\n"))
    return mytext

register.filter('update_point', update_point)

