from urllib.parse import quote

from django.db import migrations

SPONSORSHIP_EMAIL = 'APAC_sponsorship@saeindia.org'   # sponsorship team (brochure page 9)
EXPO_EMAIL = 'ilangois@saeindia.org'                    # exposition desk, Mr. Ilangovan (brochure page 9)


def mailto(address, subject):
    return f'mailto:{address}?subject={quote(subject)}'


def apply(apps, schema_editor):
    Card = apps.get_model('core', 'SpecialSponsorCard')
    Meeting = apps.get_model('core', 'MeetingRoomSection')
    # only replace the old placeholder (#contact); never a link that was set in the admin
    for card in Card.objects.filter(button_link='#contact'):
        card.button_link = mailto(SPONSORSHIP_EMAIL, f'Special event enquiry: {card.name}')
        card.save(update_fields=['button_link'])
    section = Meeting.objects.filter(pk=1, button_link='#contact').first()
    if section:
        section.button_link = mailto(EXPO_EMAIL, 'Meeting room booking')
        section.save(update_fields=['button_link'])


class Migration(migrations.Migration):
    dependencies = [('core', '0058_exposition_buttons')]
    operations = [migrations.RunPython(apply, migrations.RunPython.noop)]
