from django.db import migrations

STATS = [
    ('2,000', 'VISITORS', 'Regional mobility delegates & industry observers'),
    ('1,000', 'DELEGATES', 'Registered engineers, executives & scholars'),
    ('200', 'TECHNICAL PRESENTATIONS', 'Peer-reviewed automotive engineering papers'),
    ('80', 'EXHIBITORS', 'Global Tier-1 suppliers, OEMs & deep-tech labs'),
]


def seed(apps, schema_editor):
    Section = apps.get_model('core', 'StatsSection')
    Item = apps.get_model('core', 'StatItem')
    section, created = Section.objects.get_or_create(pk=1)
    if created:
        for i, (number, label, desc) in enumerate(STATS, start=1):
            Item.objects.create(section=section, number=number, suffix='+', label=label,
                                description=desc, order=i)


class Migration(migrations.Migration):
    dependencies = [('core', '0016_stats')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
