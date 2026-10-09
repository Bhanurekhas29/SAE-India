from django.db import migrations


def apply(apps, schema_editor):
    Card = apps.get_model('core', 'SpecialSponsorCard')
    # Only the Lunch card had a filled button. Fill the outlined ones too so they all match;
    # the highlighted Dinner card keeps its orange accent button.
    Card.objects.filter(button_style='outline').update(button_style='dark')


class Migration(migrations.Migration):
    dependencies = [('core', '0061_booth_buttons_consistent')]
    operations = [migrations.RunPython(apply, migrations.RunPython.noop)]
