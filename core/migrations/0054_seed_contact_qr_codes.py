from django.db import migrations

QR_CODES = [
    ('Author registration', 'contact/qr-author-registration.png',
     'https://saeindia.zohobackstage.in/APAC23AuthorRegistration'),
    ('Delegate registration', 'contact/qr-delegate-registration.png',
     'https://saeindia.zohobackstage.in/23rdEditionofAsiaPacificAutomotiveEngineeringConference'),
]


def seed(apps, schema_editor):
    Section = apps.get_model('core', 'ContactSection')
    QR = apps.get_model('core', 'ContactQR')
    section = Section.objects.filter(pk=1).first()
    if section is None:
        return
    if not QR.objects.filter(section=section).exists():
        for i, (label, image, link) in enumerate(QR_CODES, start=1):
            QR.objects.create(section=section, label=label, image=image, link=link, order=i)
    # the old card text talked about a program and brochure; only replace it if it was never edited
    if section.qr_title == 'Scan to Know More':
        section.qr_title = 'Scan to Register'
    if section.qr_subtext == 'Instant access to program, brochure & tickets':
        section.qr_subtext = 'Scan the code for Author or Delegate registration'
    section.save()


class Migration(migrations.Migration):
    dependencies = [('core', '0053_contact_qr_codes')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
