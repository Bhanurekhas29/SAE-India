from django.db import migrations

SLICES = [
    ('Connected & Intelligent Vehicles', 'sensors'),
    ('Cybersecurity & Functional Safety', 'security'),
    ('Software Defined Vehicles', 'memory'),
    ('Smart Manufacturing & Industry 4.0', 'precision_manufacturing'),
    ('Safety, Styling & Vehicle Performance', 'speed'),
    ('Electrification & Energy Solutions', 'bolt'),
    ('Mobility Systems & Components', 'settings_suggest'),
    ('Powertrain & Advanced Technologies', 'engineering'),
]


def seed(apps, schema_editor):
    Hero = apps.get_model('core', 'HeroSection')
    Slice = apps.get_model('core', 'HeroWheelSlice')
    hero = Hero.objects.first()
    if hero and not Slice.objects.filter(hero=hero).exists():
        for i, (title, icon) in enumerate(SLICES, start=1):
            Slice.objects.create(hero=hero, title=title, icon=icon, order=i)


class Migration(migrations.Migration):
    dependencies = [('core', '0066_hero_wheel')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
