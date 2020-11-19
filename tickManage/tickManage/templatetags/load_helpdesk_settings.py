"""
django-tickManage - A Django powered ticket tracker for small enterprise.

templatetags/load_tickManage_settings.py - returns the settings as defined in
                                    django-tickManage/tickManage/settings.py
"""
from django.template import Library
from tickManage import settings as tickManage_settings_config


def load_tickManage_settings(request):
    try:
        return tickManage_settings_config
    except Exception as e:
        import sys
        print("'load_tickManage_settings' template tag (django-tickManage) crashed with following error:",
              file=sys.stderr)
        print(e, file=sys.stderr)
        return ''


register = Library()
register.filter('load_tickManage_settings', load_tickManage_settings)
