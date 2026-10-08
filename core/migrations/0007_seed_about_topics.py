from django.db import migrations

CARDS = [
    ('directions_car', 'Future Powertrains – Innovations in ICE, Electrification, Hydrogen and Other Energy Conversion Systems',
     'Electric Vehicles (EVs), Hybrid Powertrains, Hydrogen and Fuel Cell Technologies, Energy Storage Systems and Powertrain Energy Management'),
    ('self_driving_car', 'Automated, Connected, Safe and Smart Mobility Automated.',
     'Advanced Driver Assistance Systems (ADAS) and Automated Driving Systems, Connected Mobility and V2X Communication, Intelligent Transport and Smart Mobility Systems, Emerging Transportation Technologies, App- and Service-Based Ecosystem, Monetisation Models,'),
    ('speed', 'Vehicle Dynamics, Control and Performance',
     'Dynamic Performance, Chassis Tuning, NVH Optimisation, Ride Comfort and Perceived Quality'),
    ('policy', 'Standards, Regulations and Policy Impact on Vehicles',
     'Harmonisation Trends, Regulation Led Vehicle Development, Technology Neutrality and Innovation'),
    ('deployed_code', 'Materials, Light Weighting and Cost-Effective Manufacturing Technologies',
     'Advanced Materials, Lightweight Design Strategies, Design for Manufacturability, Scalable Production Technologies'),
    ('airline_seat_recline_normal', 'Human Factors, Ergonomics and User-Centric Vehicle Design',
     'Driver and Occupant Ergonomics, In-Cabin Comfort, Perceived Quality'),
    ('security', 'Cybersecurity and AI-Enabled Vehicles',
     'Vehicle Cyber-Security, Secure OTA/Software Compliance Mindset, AI Features in Vehicles'),
    ('settings_suggest', 'Vehicle as a Digital Platform',
     'Vehicle Software and Electronics, Software-Defined Vehicles (SDVs), AI-Defined Vehicles'),
    ('terminal', 'Digital Transformation, Digital Twins and Smart Engineering for Faster Time-to-Market',
     'Digitalisation Strategies, Data-Driven Development, Virtual Engineering, Integrated Digital Workflows'),
    ('recycling', 'Energy, Emissions, Environment, Circularity and Life Cycle Assessment (LCA)',
     'Tailpipe and Lifecycle Emissions, Circular Economy Strategies, Recyclable and Sustainable Materials, ESG Metrics'),
]


def seed(apps, schema_editor):
    About = apps.get_model('core', 'AboutSection')
    Stat = apps.get_model('core', 'AboutStat')
    Topics = apps.get_model('core', 'TopicsSection')
    Card = apps.get_model('core', 'TopicCard')

    about, created = About.objects.get_or_create(pk=1, defaults=dict(
        pill_text='ABOUT THE CONFERENCE',
        heading='Driving Innovation in Automotive Engineering',
        description=('Auto Performance brings together global industry leaders, engineers, researchers and '
                     'innovators to explore the latest advancements in automotive technology, sustainability '
                     'and next-generation mobility solutions.'),
        badge_title='AUTO PERFORMANCE', badge_year='2025',
        button_text='Register Now', button_link='#contact',
    ))
    if created:
        for i, (icon, num, label) in enumerate([
                ('calendar_month', '3 Days', 'Conference'),
                ('school', '50+', 'Expert Speakers'),
                ('groups', '1,000+', 'Attendees')], start=1):
            Stat.objects.create(about=about, icon=icon, number=num, label=label, order=i)

    topics, created = Topics.objects.get_or_create(pk=1, defaults=dict(
        eyebrow='TECHNICAL CONCEPTS',
        heading_pre='Technical Topics &', heading_highlight='Innovation Tracks',
        subtext='Explore the latest advancements in automotive technology, sustainability, '
                'and next-generation mobility solutions.',
    ))
    if created:
        for i, (icon, title, desc) in enumerate(CARDS, start=1):
            Card.objects.create(section=topics, icon=icon, title=title, description=desc, order=i)


class Migration(migrations.Migration):
    dependencies = [('core', '0006_about_topics')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
