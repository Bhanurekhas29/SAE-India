from django.db import migrations

# colours are approximated from the design screenshot
BOOTHS = [
    ('grid_view', '9 sq. mtr.', '(3 × 3)', '3m × 3m', 'STARTUP & SPECIALIST', 'Standard Turnkey', '1,50,000',
     'outline', '#F0FDFA', '#0D9488', ''),
    ('grid_view', '12 sq. mtr.', '(3 × 4)', '3m × 4m', 'TECHNOLOGY SHOWCASE', 'Executive Space', '2,00,000',
     'dark', '#F0F9FF', '#0284C7', ''),
    ('storefront', '18 sq. mtr.', '(3 × 6)', '3m × 6m', 'OEM SUB-SYSTEM', 'Pavilion Bay', '3,00,000',
     'outline', '#ECFDF5', '#10B981', ''),
    ('apartment', '36 sq. mtr.', '(6 × 6)', '6m × 6m', 'FLAGSHIP SHOWCASE', 'Island Pavilion', '6,00,000',
     'accent', '#FFF7D7', '#D97706', 'FLAGSHIP OPTION'),
]


def seed(apps, schema_editor):
    Section = apps.get_model('core', 'ExpositionSection')
    Booth = apps.get_model('core', 'BoothSpace')
    section, created = Section.objects.get_or_create(pk=1, defaults=dict(
        pill_text='GLOBAL MOBILITY EXPO • YASHOBHOOMI ARENA',
        heading='Exposition & Commercial Spaces',
        subtext='Prime turnkey and raw space footprints for automotive OEMs, Tier-1 suppliers, '
                'engineering tech, and mobility startups.',
        top_button_text='Reserve Expo Booth',
        venue_tag='LIVE VENUE VIEW',
        venue_title='Yashobhoomi World-Class Exhibition Arenas & Pavilion Booths',
        venue_subtext="India's International Convention and Expo Centre (IICC), Dwarka, New Delhi",
        pass_headline='2 Complimentary Exhibitor Passes',
        pass_subline='Allocated per confirmed booth booking',
        pass_includes='Exhibition Arena access and lunch for 2 days.',
        pass_excludes='Delegate Kit, Gala Dinner, and access to Plenary & Technical Session.',
        gst_footnote='* 18% GST extra is applicable',
        footer_link_text='Enquire for Custom Pavilion →',
    ))
    if created:
        for i, (icon, size, grid, dims, cat, name, price, style, tint, accent, flag) in enumerate(BOOTHS, start=1):
            Booth.objects.create(section=section, icon=icon, size_label=size, grid_label=grid, dimensions=dims,
                                 category=cat, name=name, price=price, button_style=style,
                                 tint_color=tint, accent_color=accent, flagship_tag=flag, order=i)


class Migration(migrations.Migration):
    dependencies = [('core', '0022_exposition')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
