from django.db import migrations


def apply(apps, schema_editor):
    Link = apps.get_model('core', 'FooterLink')
    # the footer's "Register" link still has its placeholder (#contact): give it the Author / Delegate choices
    Link.objects.filter(label='Register', link='#contact').update(use_register_dropdown=True)


class Migration(migrations.Migration):
    dependencies = [('core', '0063_footer_link_register_dropdown')]
    operations = [migrations.RunPython(apply, migrations.RunPython.noop)]
