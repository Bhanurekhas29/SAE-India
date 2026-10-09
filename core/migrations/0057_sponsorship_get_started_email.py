from urllib.parse import quote

from django.db import migrations

SPONSORSHIP_EMAIL = 'APAC_sponsorship@saeindia.org'


def mailto(package_title):
    # address + subject only: the button-link field holds 200 characters
    return f'mailto:{SPONSORSHIP_EMAIL}?subject={quote("Sponsorship enquiry: " + package_title)}'


def apply(apps, schema_editor):
    Package = apps.get_model('core', 'SponsorPackage')
    # only replace the placeholder link, never an address someone set in the admin
    for card in Package.objects.filter(button_link='#contact'):
        card.button_link = mailto(card.title)
        card.save(update_fields=['button_link'])


class Migration(migrations.Migration):
    dependencies = [('core', '0056_sponsorship_packages_brochure')]
    operations = [migrations.RunPython(apply, migrations.RunPython.noop)]
