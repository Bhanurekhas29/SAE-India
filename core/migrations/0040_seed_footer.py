from django.db import migrations

# (label, link, highlighted)
LINKS = [
    ('Home', '#home', False), ('About', '#about', False), ('Tracks', '#topics', False),
    ('Speakers', '#committee', False), ('Sponsors', '#partners', False),
    ('Register', '#contact', True), ('Contact', '#contact', False),
]

# Privacy / Terms stay without a destination until the client decides popup / document.
LEGAL = [('Privacy Policy', ''), ('Terms & Conditions', ''), ('Contact', '#contact')]

# Social URLs are not known yet, so the icons stay inactive until the links are added in the admin.
SOCIALS = ['facebook', 'linkedin', 'instagram', 'x']


def seed(apps, schema_editor):
    Footer = apps.get_model('core', 'FooterSection')
    Social = apps.get_model('core', 'FooterSocial')
    Link = apps.get_model('core', 'FooterLink')
    Legal = apps.get_model('core', 'FooterLegalLink')
    footer, created = Footer.objects.get_or_create(pk=1, defaults=dict(
        tagline='Asia Pacific Automotive Engineering Conference • Sustainable Mobility & Technology',
        website_text='saeindia.org/apac23', website_url='https://www.saeindia.org/apac23',
        copyright_text='© 2026 Asia Pacific Automotive Engineering Conference (APAC 23) / SAEINDIA. '
                       'All rights reserved.',
    ))
    if created:
        for i, platform in enumerate(SOCIALS, start=1):
            Social.objects.create(footer=footer, platform=platform, url='', order=i, is_active=False)
        for i, (label, link, hi) in enumerate(LINKS, start=1):
            Link.objects.create(footer=footer, label=label, link=link, is_highlighted=hi, order=i)
        for i, (label, link) in enumerate(LEGAL, start=1):
            Legal.objects.create(footer=footer, label=label, link=link, order=i)


class Migration(migrations.Migration):
    dependencies = [('core', '0039_footer')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
