from django.db import migrations

SUBTITLE = (
    'APAC23 – Asia Pacific Automotive Engineering Conference & Expo\n'
    '13–14 November 2026 | Yashobhoomi Convention Centre, New Delhi'
)

# SAMPLE TEXT: placeholder until the client supplies the approved Privacy Policy.
# Edit it any time in the admin under Legal Pages (popups) > Privacy Policy.
PRIVACY = '''This is sample text. This Privacy Policy explains how SAEINDIA collects, uses and protects personal information shared for APAC23. The final policy will replace this text once it is approved.

## 1. Information We Collect

We may collect your name, organisation, designation, email address, phone number and billing details when you register, submit a paper, book a booth or contact the organising team.

## 2. How We Use Your Information

- To process registrations, payments and confirmations
- To share event updates, schedules and important notices
- To manage paper submissions, sponsorships and exhibition bookings
- To improve the event and the website

## 3. Sharing of Information

We do not sell your personal information. It may be shared only with service providers and partners who help us run the event, and where required by law.

## 4. Photography and Event Media

Photography and video recording may take place during the event. Images may be used for event reports and promotional material. Please contact the organising team if you have concerns.

## 5. Data Security and Retention

We take reasonable steps to keep your information secure and keep it only as long as needed for the purposes above or as required by law.

## 6. Your Choices

You may ask to view, correct or delete your information, or stop receiving updates, by writing to the organising team.

## 7. Contact Us

For any questions about this policy, please contact SAEINDIA at ilangois@saeindia.org.
'''


def seed(apps, schema_editor):
    Legal = apps.get_model('core', 'LegalPage')
    Link = apps.get_model('core', 'FooterLegalLink')
    Legal.objects.get_or_create(slug='privacy', defaults=dict(
        title='Privacy Policy', subtitle=SUBTITLE, content=PRIVACY, order=2))
    # only fill an empty link, never overwrite one that was typed in the admin
    Link.objects.filter(label='Privacy Policy', link='').update(link='#legal-privacy')


class Migration(migrations.Migration):
    dependencies = [('core', '0064_seed_footer_register_dropdown')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
