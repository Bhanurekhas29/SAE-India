from django.db import migrations

PACKAGES = [
    ('PLATINUM', 'Platinum Sponsor', '25,000', 'Maximum brand exposure and premium positioning.',
     ['Logo on all materials', 'Keynote speaking slot', 'VIP access (10 passes)', 'Dedicated brand feature']),
    ('GOLD', 'Gold Sponsor', '15,000', 'High visibility and strong brand presence.',
     ['Logo on website', 'Panel discussion slot', '5 VIP passes', 'Email campaign feature']),
    ('SILVER', 'Silver Sponsor', '10,000', 'Valuable exposure to our engaged audience.',
     ['Logo on website', 'Social media mentions', '3 VIP passes', 'Newsletter feature']),
    ('BRONZE', 'Bronze Sponsor', '5,000', 'Grow your brand with targeted visibility.',
     ['Logo on website', '2 VIP passes', 'Event signage', 'Social media mention']),
    ('SUPPORTER', 'Supporter Sponsor', '2,500', 'Be part of the movement and make an impact.',
     ['Logo on website', 'Event signage', 'Thank you mention', 'Community recognition']),
]


def seed(apps, schema_editor):
    Section = apps.get_model('core', 'SponsorshipSection')
    Package = apps.get_model('core', 'SponsorPackage')
    section, created = Section.objects.get_or_create(pk=1, defaults=dict(
        pill_text='Sponsorship Opportunities', heading='Sponsorship Details',
        subtext='Partner with AutoPerformance and showcase your brand to a global audience of '
                'industry leaders, innovators and decision-makers.',
        tagline_words='Partner, Grow, Lead',
    ))
    if created:
        for i, (tier, title, price, desc, benefits) in enumerate(PACKAGES, start=1):
            Package.objects.create(section=section, tier_label=tier, title=title, price=price,
                                   description=desc, benefits='\n'.join(benefits), order=i)


class Migration(migrations.Migration):
    dependencies = [('core', '0018_sponsorship')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
