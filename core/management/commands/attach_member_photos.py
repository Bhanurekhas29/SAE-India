from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from core.models import CommitteeMember


class Command(BaseCommand):
    help = (
        'Attaches media/members/<slugified name>.jpg to every committee member that has no photo yet. '
        'Safe to run on every deploy: it never replaces a photo that is already set.'
    )

    def handle(self, *args, **options):
        attached = 0
        for member in CommitteeMember.objects.filter(photo=''):
            rel = f'members/{slugify(member.name)}.jpg'
            if (settings.MEDIA_ROOT / rel).exists():
                member.photo.name = rel
                member.save(update_fields=['photo'])
                attached += 1
        self.stdout.write(self.style.SUCCESS(f'Member photos attached: {attached}'))
