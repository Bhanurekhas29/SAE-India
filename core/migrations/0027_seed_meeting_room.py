from django.db import migrations

DETAILS = [
    ('sell', 'Booking Fee:', 'INR 5,000 per hour (+18% GST extra).'),
    ('schedule', 'Duration:', 'Minimum 2 hours per booking is mandatory.'),
    ('event_available', 'Availability:', 'Limited slots (first-come, first-served basis).'),
]

FEATURES = [
    ('groups', 'Professional Environment',
     'Dedicated space for high-level discussions and strategic collaborations.'),
    ('shield', 'Privacy & Focus',
     'Ideal for confidential meetings, sponsor interactions, and commercial negotiations.'),
    ('location_on', 'Convenience',
     'Located within Yashobhoomi conference arena for seamless access during sessions.'),
    ('redeem', 'Essential Provisions',
     'Complimentary notepads, executive pens, and water bottles per booking.'),
]


def seed(apps, schema_editor):
    Section = apps.get_model('core', 'MeetingRoomSection')
    Detail = apps.get_model('core', 'MeetingRoomDetail')
    Feature = apps.get_model('core', 'MeetingRoomFeature')
    section, created = Section.objects.get_or_create(pk=1, defaults=dict(
        pill_text='B2B CONFIDENTIAL SPACE', title='Business Meeting Room', price='5,000',
        gst_note='* 18% GST extra is applicable', button_text='Book Meeting Room →',
    ))
    if created:
        for i, (icon, label, text) in enumerate(DETAILS, start=1):
            Detail.objects.create(section=section, icon=icon, label=label, text=text, order=i)
        for i, (icon, title, desc) in enumerate(FEATURES, start=1):
            Feature.objects.create(section=section, icon=icon, title=title, description=desc, order=i)


class Migration(migrations.Migration):
    dependencies = [('core', '0026_meeting_room')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
