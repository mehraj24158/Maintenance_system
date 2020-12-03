#!/usr/bin/python


from django.utils.translation import ugettext as _
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from tickManage.models import UserSettings
from tickManage.settings import DEFAULT_USER_SETTINGS

User = get_user_model()


class Command(BaseCommand):
    """create_usersettings command"""

    help = _('Check for user without django-tickManage UserSettings '
             'and create settings if required. Uses '
             'settings.DEFAULT_USER_SETTINGS which can be overridden to '
             'suit your situation.')

    def handle(self, *args, **options):
        """handle command line"""
        for u in User.objects.all():
            UserSettings.objects.get_or_create(user=u)
