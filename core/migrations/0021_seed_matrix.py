from django.db import migrations

TIERS = [('Title Sponsor', '₹25,00,000', True), ('Platinum', '₹15,00,000', False),
         ('Gold', '₹10,00,000', False), ('Silver', '₹6,00,000', False), ('Bronze', '₹3,00,000', False)]

NA = ('na', '', '')
DASH = ('dash', '', '')
YES = ('yes', '', '')


def T(text, sub=''):
    return ('text', text, sub)


def B(text, sub=''):
    return ('bold', text, sub)


def G(text):
    return ('badge', text, '')


# (category title, [(row label, [cell x 5 tiers])])
MATRIX = [
    ('1. EXECUTIVE & THOUGHT LEADERSHIP PRESENCE', [
        ('Presence at Keynote / Plenary Session',
         [B('Inaugural / Valedictory'), T('Keynote'), T('Panel Discussion'), NA, NA]),
        ('Presence at Technical Session',
         [B('Chair / Keynote'), T('Chair / Keynote'), T('Chair of Session'), T('Chair of Session'), NA]),
    ]),
    ('2. BRANDING, COLLATERAL & MEDIA EXPOSURE', [
        ('Logo in Event Backdrop & other marketing',
         [G('Large logo'), G('Medium logo'), T('Small logo'), T('Small logo'), T('Small logo')]),
        ('Sponsor Promo Video to be played during breaks',
         [B('3 mins video', '4 times a day'), T('3 mins video', '3 times a day'),
          T('1 mins video', '3 times a day'), T('1 mins video', '2 times a day'), NA]),
        ('Brochure / pamphlet in all delegate kits', [YES, YES, YES, NA, NA]),
    ]),
    ('3. EXPOSITION FOOTPRINT & HOSPITALITY', [
        ('Exposition Booth',
         [B('36 sq. mtr. Expo Space (Raw)'), T('18 sq. mtr. Expo Space (Raw space)'),
          T('9 sq. mtr. Expo Space (Raw)'), NA, NA]),
        ('Complimentary Delegates', [B('10'), B('7'), B('5'), B('3'), B('1')]),
        ('VIP Lounge Access', [YES, YES, DASH, DASH, DASH]),
    ]),
]


def seed(apps, schema_editor):
    Section = apps.get_model('core', 'MatrixSection')
    Tier = apps.get_model('core', 'MatrixTier')
    Category = apps.get_model('core', 'MatrixCategory')
    Row = apps.get_model('core', 'MatrixRow')
    Cell = apps.get_model('core', 'MatrixCell')

    section, created = Section.objects.get_or_create(pk=1, defaults=dict(
        title='EXECUTIVE DELIVERABLES MATRIX',
        note='Full brochure comparison across 5 official tiers',
    ))
    if not created:
        return
    tiers = [Tier.objects.create(section=section, name=n, price=p, is_highlighted=h, order=i)
             for i, (n, p, h) in enumerate(TIERS, start=1)]
    for c_order, (cat_title, rows) in enumerate(MATRIX, start=1):
        category = Category.objects.create(section=section, title=cat_title, order=c_order)
        for r_order, (label, cells) in enumerate(rows, start=1):
            row = Row.objects.create(category=category, label=label, order=r_order)
            for tier, (style, text, sub) in zip(tiers, cells):
                Cell.objects.create(row=row, tier=tier, style=style, text=text, subtext=sub)


class Migration(migrations.Migration):
    dependencies = [('core', '0020_matrix')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
