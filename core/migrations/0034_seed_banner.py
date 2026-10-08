from django.db import migrations

ITEMS = [
    ('verified', 'Secure Your Pass'),
    ('location_on', 'Yashobhoomi, New Delhi'),
    ('calendar_month', 'Nov 13–14, 2026'),
]

INFO = [
    ('hub', 'BIENNIAL MOBILITY FORUM', '11 APAC Nations Represented'),
    ('location_on', 'CONFERENCE VENUE', 'Yashobhoomi (IICC), Dwarka'),
    ('apartment', 'ORGANIZED UNDER', 'SAEINDIA, FISITA & SAE Intl'),
]


def seed(apps, schema_editor):
    Section = apps.get_model('core', 'BannerSection')
    Item = apps.get_model('core', 'BannerItem')
    Info = apps.get_model('core', 'BannerInfo')
    section, created = Section.objects.get_or_create(pk=1, defaults=dict(
        pill_text='23RD EDITION - APAC GLOBAL GATEWAY',
        heading_line1='Where Industry Meets Opportunity.',
        heading_line2='Join Hands Now!',
        description='Engage directly with 2,000+ delegates, key government policymakers, leading mobility '
                    'OEMs, and pioneering researchers shaping the next era of transportation.',
        button_text='REGISTER NOW →',
    ))
    if created:
        for i, (icon, text) in enumerate(ITEMS, start=1):
            Item.objects.create(section=section, icon=icon, text=text, order=i)
        for i, (icon, label, value) in enumerate(INFO, start=1):
            Info.objects.create(section=section, icon=icon, label=label, value=value, order=i)


class Migration(migrations.Migration):
    dependencies = [('core', '0033_banner')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
