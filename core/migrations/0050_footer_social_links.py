from django.db import migrations

# platform -> (order, address). X (Twitter) has no account yet, so it stays switched off.
SOCIALS = {
    'linkedin': (1, 'https://www.linkedin.com/company/saeindia'),
    'facebook': (2, 'https://www.facebook.com/SAEINDIADIGITAL'),
    'youtube': (3, 'https://www.youtube.com/@SAEINDIADigital'),
    'instagram': (4, 'https://www.instagram.com/saeindiadigital'),
}


def apply(apps, schema_editor):
    Footer = apps.get_model('core', 'FooterSection')
    Social = apps.get_model('core', 'FooterSocial')
    footer = Footer.objects.filter(pk=1).first()
    if footer is None:
        return
    for platform, (order, url) in SOCIALS.items():
        row = Social.objects.filter(footer=footer, platform=platform).first()
        if row is None:
            Social.objects.create(footer=footer, platform=platform, url=url, order=order, is_active=True)
        elif not row.url:                    # never overwrite an address someone typed in the admin
            row.url, row.order, row.is_active = url, order, True
            row.save()
    Social.objects.filter(footer=footer, platform='x', url='').update(is_active=False, order=9)


class Migration(migrations.Migration):
    dependencies = [('core', '0049_seed_header_button_options')]
    operations = [migrations.RunPython(apply, migrations.RunPython.noop)]
