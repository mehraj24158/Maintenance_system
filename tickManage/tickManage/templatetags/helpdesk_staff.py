"""
django-tickManage - A Django powered ticket tracker for small enterprise.

templatetags/tickManage_staff.py - The is_tickManage_staff template filter returns True if the user qualifies as Service Request staff.
"""
import logging
from django.template import Library
from django.db.models import Q

from tickManage.decorators import is_tickManage_staff


logger = logging.getLogger(__name__)
register = Library()


@register.filter(name='is_tickManage_staff')
def tickManage_staff(user):
    try:
        return is_tickManage_staff(user)
    except Exception as e:
        logger.exception("'tickManage_staff' template tag (django-tickManage) crashed")
