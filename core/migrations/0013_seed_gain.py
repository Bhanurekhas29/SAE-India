from django.db import migrations

CARDS = [
    ('memory', 'Industry Insights', 'Latest trends & future opportunities.'),
    ('menu_book', 'Practical Knowledge', 'Real-world case studies & solutions.'),
    ('diversity_3', 'Networking', 'Connect with global industry leaders.'),
    ('trending_up', 'Business Growth', 'New partnerships & collaborations.'),
]


def seed(apps, schema_editor):
    Section = apps.get_model('core', 'GainSection')
    Card = apps.get_model('core', 'GainCard')
    section, created = Section.objects.get_or_create(pk=1, defaults=dict(
        pill_text='Key Takeaways', heading="What You'll Gain",
        video_caption='Learn, Network, Grow',
    ))
    if created:
        for i, (icon, title, desc) in enumerate(CARDS, start=1):
            Card.objects.create(section=section, icon=icon, title=title, description=desc, order=i)


class Migration(migrations.Migration):
    dependencies = [('core', '0012_gain')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
