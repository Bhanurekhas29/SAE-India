from datetime import datetime
from zoneinfo import ZoneInfo

from django.db import migrations


def seed(apps, schema_editor):
    Hero = apps.get_model('core', 'HeroSection')
    Tagline = apps.get_model('core', 'HeroTagline')
    Chip = apps.get_model('core', 'HeroInfoChip')
    hero, created = Hero.objects.get_or_create(pk=1, defaults=dict(
        pill_text='GLOBAL AUTOMOTIVE TECHNOLOGY CONFERENCE',
        heading_pre='Auto', heading_highlight='Performance',
        heading_post='Automotive Engineering Conference',
        edition_label='23RD EDITION',
        event_datetime=datetime(2026, 11, 13, 9, 0, tzinfo=ZoneInfo('Asia/Kolkata')),
        primary_button_text='Register Now', primary_button_link='#contact',
        secondary_button_text='Learn More', secondary_button_link='#about',
        overlay_text='Shaping the Future of Mobility',
    ))
    if created:
        for i, t in enumerate(['Innovation', 'Sustainability', 'Next-Gen Mobility'], start=1):
            Tagline.objects.create(hero=hero, text=t, order=i)
        Chip.objects.create(hero=hero, icon='calendar_month', text='Nov 13-14, 2026', order=1)
        Chip.objects.create(hero=hero, icon='location_on',
                            text='Grand Horizon Convention Center, New York, USA', order=2)


class Migration(migrations.Migration):
    dependencies = [('core', '0004_hero_section')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
