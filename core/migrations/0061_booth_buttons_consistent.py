from django.db import migrations


def apply(apps, schema_editor):
    Booth = apps.get_model('core', 'BoothSpace')
    # Only the 2nd booth had a filled button (the others were outlined). Make the outlined ones
    # filled too, so all four match. The flagship booth keeps its orange accent button.
    Booth.objects.filter(button_style='outline').update(button_style='dark')


class Migration(migrations.Migration):
    dependencies = [('core', '0060_techhive_buttons')]
    operations = [migrations.RunPython(apply, migrations.RunPython.noop)]
