import os

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.core.management.base import BaseCommand

MARKER = 'site-data-loaded'


class Command(BaseCommand):
    help = (
        'Runs at every deploy. Loads the saved site content (core/fixtures/site_data.json) once, '
        'and creates the first admin user from DJANGO_SUPERUSER_* variables if no user exists.'
    )

    def handle(self, *args, **options):
        if Group.objects.filter(name=MARKER).exists():
            self.stdout.write('Site content already loaded - leaving the database as it is.')
        else:
            call_command('loaddata', 'site_data.json', verbosity=0)
            Group.objects.create(name=MARKER)
            self.stdout.write(self.style.SUCCESS('Site content loaded.'))

        User = get_user_model()
        username = os.getenv('DJANGO_SUPERUSER_USERNAME')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
        if username and password and not User.objects.exists():
            User.objects.create_superuser(
                username=username, password=password,
                email=os.getenv('DJANGO_SUPERUSER_EMAIL', ''),
            )
            self.stdout.write(self.style.SUCCESS(f'Admin user "{username}" created.'))
        elif not User.objects.exists():
            self.stdout.write('No admin user yet - set DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD.')
