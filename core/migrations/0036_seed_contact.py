from django.db import migrations

# Contact details are copied exactly as shown in the design screenshot; to be confirmed with the client.
PEOPLE = [
    ('SECRETARIAT', 'Mr. Ajay', 'Conference Secretariat', '+91 931816 97889', 'ajayt@saeindis.org'),
    ('COORDINATION', 'Ms. Ayisha', 'Delegate & Sponsorship Coordination', '+91173977 60949',
     'ayisha@saeindis.org'),
]


def seed(apps, schema_editor):
    Section = apps.get_model('core', 'ContactSection')
    Person = apps.get_model('core', 'ContactPerson')
    section, created = Section.objects.get_or_create(pk=1, defaults=dict(
        eyebrow='DIRECT ASSISTANCE',
        heading='Executive Organizer & Secretariat Contact Hub',
        side_text='Get in touch for delegate, sponsorship, or booth queries.',
        qr_pill_text='INSTANT MOBILE ACCESS', qr_title='Scan to Know More',
        qr_subtext='Instant access to program, brochure & tickets', qr_caption='CAMERA OR QR APP',
        strip_label='Official Conference Digital Headquarters:',
        strip_link_text='www.saeindis.org/apac23/', strip_link_url='https://www.saeindis.org/apac23/',
    ))
    if created:
        for i, (tag, name, role, phone, email) in enumerate(PEOPLE, start=1):
            Person.objects.create(section=section, tag=tag, name=name, role=role,
                                  phones=phone, emails=email, order=i)


class Migration(migrations.Migration):
    dependencies = [('core', '0035_contact')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
