import os

from django.core.management.commands import compilemessages


class Command(compilemessages.Command):
    def compile_messages(self, locations):
        if os.environ.get('DJANGO_SETTINGS_MODULE'):
            from django.conf import settings
            # If a received location match a locale set, send to compile
            if not any(location[0].startswith(locale) for location in locations for locale in settings.LOCALE_PATHS):
                return
        super(Command, self).compile_messages(locations)
