from django.db import migrations

DELIVERABLES = [
    ('person', '1 Complimentary Delegate Pass', 'Full delegate access per confirmed registration'),
    ('inventory_2', '2×2 = 4 sq. mtr. Expo Space', 'Turnkey / Raw Space footprint within Innovation Pavilion'),
    ('co_present', '1 TechHive Presentation', 'Dedicated showcase stage slot to pitch before mobility leaders'),
]

RATES = [
    ('SAEINDIA Member', 'Save ₹2,500 with membership', '', '₹15,000', '₹17,500'),
    ('SAEINDIA Non-Member', 'Global Industry professionals & non-affiliates', '', '₹18,000', '₹20,000'),
    ('Academia Faculty', 'Recognized universities, colleges & research institutions', '', '₹10,000', '₹12,000'),
    ('Author', 'Accepted paper presenting authors', '', '₹8,000', '₹8,000'),
]


def seed(apps, schema_editor):
    Section = apps.get_model('core', 'TechHiveSection')
    Deliverable = apps.get_model('core', 'TechHiveDeliverable')
    Rate = apps.get_model('core', 'DelegateRate')
    section, created = Section.objects.get_or_create(pk=1, defaults=dict(
        pill_text='TECHHIVE & DELEGATE REGISTRATION',
        heading='Startup Incubator & Attendance Packages',
        subtext='Fostering mobility startups alongside global automotive engineering academia, '
                'researchers, and industry delegates.',
        top_button_text='Register as Delegate',
        panel_tag1='MOBILITY STARTUP LAUNCHPAD', panel_tag2='DEEP-TECH HUB',
        panel_title='TechHive / Startup',
        panel_description='Dedicated platform for emerging innovators, hardware inventors, and mobility '
                          'tech entrepreneurs.',
        fee_price='50,000', fee_gst_note='18% GST extra is applicable',
        apply_button_text='APPLY FOR TECHHIVE STARTUP SPACE →',
        matrix_title='DELEGATE INVESTMENT MATRIX',
        matrix_subtitle='International & National Attendance Rates.',
        matrix_badge='Early Bird Active till Sep 15, 2026',
        early_column_title='Till Sep 15, 2026', standard_column_title='After Sep 15, 2026',
        matrix_gst_note='18% GST extra is applicable on all delegate categories.',
        matrix_button_text='REGISTER AS DELEGATE →',
    ))
    if created:
        for i, (icon, title, sub) in enumerate(DELIVERABLES, start=1):
            Deliverable.objects.create(section=section, icon=icon, title=title, subline=sub, order=i)
        for i, (cat, desc, note, early, std) in enumerate(RATES, start=1):
            Rate.objects.create(section=section, category=cat, order=i, early_price=early, standard_price=std,
                                description=desc if cat != 'SAEINDIA Member' else '',
                                note=desc if cat == 'SAEINDIA Member' else note)


class Migration(migrations.Migration):
    dependencies = [('core', '0029_techhive')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
