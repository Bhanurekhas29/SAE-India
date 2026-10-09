from urllib.parse import quote

from django.db import migrations

EXPO_EMAIL = 'ilangois@saeindia.org'   # Exposition desk, Mr. Ilangovan (brochure page 9)


def mailto(subject):
    return f'mailto:{EXPO_EMAIL}?subject={quote(subject)}'


def apply(apps, schema_editor):
    Section = apps.get_model('core', 'ExpositionSection')
    Booth = apps.get_model('core', 'BoothSpace')
    # only replace the old placeholder (#contact); never a link that was set in the admin
    for booth in Booth.objects.filter(button_link='#contact'):
        booth.button_link = mailto(f'Booth enquiry: {booth.name} ({booth.size_label})')
        booth.save(update_fields=['button_link'])
    section = Section.objects.filter(pk=1).first()
    if section:
        if section.top_button_link == '#contact':
            section.top_button_link = '#expo-booths'          # scrolls to the booth list
        if section.footer_link_url == '#contact':
            section.footer_link_url = mailto('Custom pavilion enquiry')
        section.save()


class Migration(migrations.Migration):
    dependencies = [('core', '0057_sponsorship_get_started_email')]
    operations = [migrations.RunPython(apply, migrations.RunPython.noop)]
