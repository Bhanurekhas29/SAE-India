from urllib.parse import quote

from django.db import migrations

DELEGATE = 'https://saeindia.zohobackstage.in/23rdEditionofAsiaPacificAutomotiveEngineeringConference'
TECHHIVE_EMAIL = 'suman@saeindia.org'   # TechHive desk, Mr. Suman (brochure page 9)


def apply(apps, schema_editor):
    Section = apps.get_model('core', 'TechHiveSection')
    section = Section.objects.filter(pk=1).first()
    if section is None:
        return
    # only replace the old placeholder (#contact); never a link that was set in the admin
    if section.top_button_link == '#contact':
        section.top_button_link = DELEGATE
    if section.matrix_button_link == '#contact':
        section.matrix_button_link = DELEGATE
    if section.apply_button_link == '#contact':
        subject = quote('TechHive startup space application')
        section.apply_button_link = f'mailto:{TECHHIVE_EMAIL}?subject={subject}'
    section.save()


class Migration(migrations.Migration):
    dependencies = [('core', '0059_special_events_and_meeting_room_buttons')]
    operations = [migrations.RunPython(apply, migrations.RunPython.noop)]
