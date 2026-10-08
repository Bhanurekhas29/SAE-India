from django.db import migrations

ITEMS = [('Home', '#home'), ('About', '#about'), ('Topics', '#topics'),
         ('Sponsors', '#sponsors'), ('Gallery', '#gallery'), ('Contact', '#contact')]


def seed(apps, schema_editor):
    Header = apps.get_model('core', 'HeaderSettings')
    MenuItem = apps.get_model('core', 'MenuItem')
    header, _ = Header.objects.get_or_create(pk=1, defaults={'site_name': 'SAE India'})
    if not MenuItem.objects.filter(header=header).exists():
        for i, (label, link) in enumerate(ITEMS, start=1):
            MenuItem.objects.create(header=header, label=label, link=link, order=i)


class Migration(migrations.Migration):
    dependencies = [('core', '0002_header_menu')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
