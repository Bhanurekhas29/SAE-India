from django.db import migrations

DELIVERABLE = 'Logo in Event Backdrop & other marketing collaterals'

# (strip, colour, exclusive, name, description, price, passes, button, style, highlighted)
CARDS = [
    ('NETWORKING BREAKS', '#0D9488', '', 'Hi-Tea Sponsor',
     'Networking Refreshment & Mid-Session Intermission Partner', '3,00,000', '1 Delegate',
     'EXPRESS INTEREST', 'outline', False),
    ('EXECUTIVE DINING', '#2563EB', '', 'Lunch Sponsor',
     'High-Profile Executive Dining & Keynote Luncheon Partner', '10,00,000', '5 Delegates',
     'EXPRESS INTEREST', 'dark', False),
    ('EVENING GALA - PRIME', '#D97706', 'EXCLUSIVE', 'Dinner Sponsor',
     'Gala Networking Banquet & Presidential Evening Host', '18,00,000', '7 Delegates',
     'RESERVE DINNER GALA', 'accent', True),
    ('EVENING FEATURE', '#059669', '', 'Cultural Program',
     'Grand Cultural Night & Delegates Heritage Evening Partner', '8,00,000', '4 Delegates',
     'EXPRESS INTEREST', 'outline', False),
]


def seed(apps, schema_editor):
    Section = apps.get_model('core', 'SpecialSponsorSection')
    Card = apps.get_model('core', 'SpecialSponsorCard')
    section, created = Section.objects.get_or_create(pk=1, defaults=dict(
        pill_text='TARGETED BRAND EXPERIENCES',
        heading='Special Event Sponsorships',
        subtext='Curated high-touch hospitality and experiential networking properties designed to '
                'position your leadership before key mobility stakeholders and global delegations.',
        tag_text='Exclusive Hospitality Slots',
    ))
    if created:
        for i, (strip, color, excl, name, desc, price, passes, btn, style, hi) in enumerate(CARDS, start=1):
            Card.objects.create(section=section, strip_text=strip, strip_color=color, exclusive_tag=excl,
                                name=name, description=desc, price=price, deliverables=DELIVERABLE,
                                passes_value=passes, button_text=btn, button_style=style,
                                is_highlighted=hi, order=i)


class Migration(migrations.Migration):
    dependencies = [('core', '0024_special_sponsors')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
