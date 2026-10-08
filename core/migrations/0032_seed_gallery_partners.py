from django.db import migrations


def seed(apps, schema_editor):
    Gallery = apps.get_model('core', 'GallerySection')
    Partners = apps.get_model('core', 'PartnersSection')
    Gallery.objects.get_or_create(pk=1, defaults=dict(
        pill_text='CONFERENCE HIGHLIGHTS', heading='Event Gallery',
        subtext='High-resolution captures and key moments from the APAC Mobility Summit.',
    ))
    Partners.objects.get_or_create(pk=1, defaults=dict(
        pill_text='Our Sponsors & Partners', heading='Supporting Innovation Together',
    ))


class Migration(migrations.Migration):
    dependencies = [('core', '0031_gallery_partners')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
