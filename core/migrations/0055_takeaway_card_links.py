from django.db import migrations

AUTHOR = 'https://saeindia.zohobackstage.in/APAC23AuthorRegistration'
DELEGATE = 'https://saeindia.zohobackstage.in/23rdEditionofAsiaPacificAutomotiveEngineeringConference'

# card title -> new destination. "Explore Packages" (Sponsors) already points to #sponsors.
LINKS = {
    'Speakers': AUTHOR,
    'Participants': DELEGATE,
    'Exhibitors': '#exposition',
}


def apply(apps, schema_editor):
    Card = apps.get_model('core', 'TakeawayCard')
    for title, url in LINKS.items():
        # only change a link that still has the placeholder; never overwrite one edited in the admin
        Card.objects.filter(title=title, link_url='#contact').update(link_url=url)


class Migration(migrations.Migration):
    dependencies = [('core', '0054_seed_contact_qr_codes')]
    operations = [migrations.RunPython(apply, migrations.RunPython.noop)]
