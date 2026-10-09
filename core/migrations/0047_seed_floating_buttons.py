from django.db import migrations


def seed(apps, schema_editor):
    FloatingButtons = apps.get_model('core', 'FloatingButtons')
    # model defaults hold the number +91 8870471511 and the first WhatsApp message
    FloatingButtons.objects.get_or_create(pk=1)


class Migration(migrations.Migration):
    dependencies = [('core', '0046_floating_buttons')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
