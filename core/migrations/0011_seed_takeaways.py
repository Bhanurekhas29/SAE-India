from django.db import migrations

CARDS = [
    ('mic', 'Speakers', ['Thought Leadership', 'Industry Influence', 'Knowledge Sharing', 'Brand Authority', 'Networking'],
     'Join as Speaker', '#contact', '#F59E0B', '#059669'),
    ('diversity_3', 'Participants', ['Learning', 'Insights', 'Networking', 'Exposure', 'Innovation'],
     'Register to Attend', '#contact', '#06B6D4', '#0891B2'),
    ('apartment', 'Exhibitors', ['Lead Generation', 'Brand Visibility', 'Product Showcase', 'Customer Engagement', 'Market Reach'],
     'Book a Booth', '#contact', '#10B981', '#059669'),
    ('star', 'Sponsors', ['Brand Recall', 'Visibility', 'Positioning', 'Partnerships', 'ROI'],
     'Explore Packages', '#sponsors', '#84CC16', '#65A30D'),
]


def seed(apps, schema_editor):
    Section = apps.get_model('core', 'TakeawaysSection')
    Card = apps.get_model('core', 'TakeawayCard')
    section, created = Section.objects.get_or_create(pk=1, defaults=dict(
        pill_text='Conference Highlights', heading='Key Takeaways:',
        subtext='Strategic multi-dimensional outcomes delivering high-value engagement across the '
                'mobility engineering ecosystem.',
        link_text='View All Topics', link_url='#topics',
    ))
    if created:
        for i, (icon, title, bullets, link_text, link_url, accent, dot) in enumerate(CARDS, start=1):
            Card.objects.create(section=section, icon=icon, title=title, bullets='\n'.join(bullets),
                                link_text=link_text, link_url=link_url,
                                accent_color=accent, bullet_color=dot, order=i)


class Migration(migrations.Migration):
    dependencies = [('core', '0010_takeaways')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
