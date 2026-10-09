from django.db import migrations

OPTIONS = [
    ('Register as Author', 'https://saeindia.zohobackstage.in/APAC23AuthorRegistration'),
    ('Register as Delegate', 'https://saeindia.zohobackstage.in/23rdEditionofAsiaPacificAutomotiveEngineeringConference'),
]


def seed(apps, schema_editor):
    Header = apps.get_model('core', 'HeaderSettings')
    Option = apps.get_model('core', 'HeaderButtonOption')
    header = Header.objects.filter(pk=1).first()
    if header and not Option.objects.filter(header=header).exists():
        for i, (label, link) in enumerate(OPTIONS, start=1):
            Option.objects.create(header=header, label=label, link=link, order=i, open_in_new_tab=True)


class Migration(migrations.Migration):
    dependencies = [('core', '0048_header_button_options')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
