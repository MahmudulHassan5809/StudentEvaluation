from django import template
from datetime import datetime, timedelta
from django.db.models import Q
from urllib.parse import urlparse, parse_qs
register = template.Library()


@register.filter
def active_semester(all_course):
    if all_course:
        data = all_course.filter(semester__active=True)
        return data
    return all_course
