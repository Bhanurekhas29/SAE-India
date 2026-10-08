from django.db import migrations

# Details taken from the APAC23 brochure (page 9). Avigha is from the design only, so she is
# inactive until her phone and email are confirmed.
COORDINATORS = [
    ('Mr. U. D. Bhangale', '+91 98102 71130', 'ed.udbhangale@saenis.org', True),
    ('Mr. Praveensingh Jadhav', '+91 97115 14560', 'pravins.jadhav@maruti.co.in', True),
    ('Mr. Jayawant Hardikar', '+91 99023 81670', 'APAC_sponsorship@saeindia.org', True),
    ('Mr. Ajay Nair', '+91 93846 97969', 'ajay@saeindia.org', True),
    ('Ms. Avigha', '', 'avigha@saeindia.org', False),
]

DESKS = [
    ('EXPOSITION DESK', 'Mr. Ilangovan', '+91 88704 71511', 'ilangois@saeindia.org'),
    ('DELEGATE DESK', 'Ms. Shantha Priya', '+91 73387 48891', 'priya@saeindia.org'),
    ('TECHHIVE DESK', 'Mr. Suman', '+91 98402 10293', 'suman@saeindia.org'),
]


def seed(apps, schema_editor):
    Section = apps.get_model('core', 'CoordinatorsSection')
    Coordinator = apps.get_model('core', 'Coordinator')
    Desk = apps.get_model('core', 'DeskCard')
    section, created = Section.objects.get_or_create(pk=1, defaults=dict(
        eyebrow='BROCHURE OFFICIAL DIRECTORY',
        heading='Sponsorship & Event Desk Coordinators',
        side_text='Direct contact points for sponsors, exhibitors, delegates & startups',
    ))
    if created:
        for i, (name, phone, email, active) in enumerate(COORDINATORS, start=1):
            Coordinator.objects.create(section=section, name=name, phones=phone, emails=email,
                                       order=i, is_active=active)
        for i, (tag, name, phone, email) in enumerate(DESKS, start=1):
            Desk.objects.create(section=section, tag=tag, name=name, phones=phone, emails=email, order=i)


class Migration(migrations.Migration):
    dependencies = [('core', '0037_coordinators')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
