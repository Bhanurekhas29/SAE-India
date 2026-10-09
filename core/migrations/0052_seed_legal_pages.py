from django.db import migrations

TERMS_SUBTITLE = (
    'APAC23 – Asia Pacific Automotive Engineering Conference & Expo\n'
    '13–14 November 2026 | Yashobhoomi Convention Centre, New Delhi'
)

# Left out on purpose until the client completes them:
#  - "Cancellation after the deadline or non-attendance:" (section 3, no text given)
#  - "Event postponement or cancellation policy:" (section 4, no text given)
#  - the internal note "These details must be published before registrations are accepted."
TERMS = '''These Terms & Conditions govern registration and participation in APAC23, organised by SAEINDIA. Please read them before completing your registration.

## 1. Registration

Participants must provide accurate registration and billing information. Registration is confirmed after the applicable payment has been received and SAEINDIA has issued a confirmation.

Member, student or other concessionary categories may require supporting documentation. Access to the event is subject to registration verification and venue requirements.

## 2. Fees and Payments

Registration fees, applicable taxes and package inclusions will be displayed before payment. Participants should check their selected category and billing details before completing checkout.

Travel, accommodation, visas and other personal expenses are the participant’s responsibility unless expressly included in the purchased package.

Payment failures, duplicate payments or discrepancies should be reported with the transaction reference to the organising team.

## 3. Cancellation, Refunds and Substitution

Cancellation and substitution requests must be submitted in writing to ilangois@saeindia.org.

The following policy will apply:

- Cancellation deadline: 24 hrs
- Refund eligibility and deductions: No refund Online payment
- Participant substitution: As mentioned in the brochure
- Refund processing period: 15 Days

## 4. Programme Changes

SAEINDIA may make reasonable changes to speakers, session timings, programme content or exhibition arrangements. Material changes will be communicated through official event channels.

If the event is postponed, relocated or cancelled, registered participants will be informed of the arrangements available to them.

## 5. Event Access and Conduct

Participants must comply with venue safety rules and instructions from authorised event staff. Credentials must not be shared or used by another person without an approved substitution.

Harassment, discrimination, unsafe behaviour, disruption and unauthorised solicitation are prohibited. SAEINDIA may restrict access or remove a participant for serious breaches, subject to applicable law.

## 6. Authors and Presenters

Authors and presenters must comply with the submission, registration and presentation requirements communicated by the technical committee.

Paper acceptance does not replace registration. Programme scheduling and publication are subject to the applicable technical review and publication conditions. Submission alone does not guarantee acceptance or publication.

## 7. Exhibitors and Sponsors

Exhibitors and sponsors are also subject to their accepted booking terms, package conditions, exhibition manual and venue rules.

Where these general terms conflict with an expressly agreed provision in a separate exhibitor or sponsorship agreement, that specific provision will govern the relevant booking.

## 8. Intellectual Property and Recording

Presentations, papers, logos and other event materials remain the property of their respective owners. Attendance does not grant permission to reproduce or commercially distribute those materials.

Recording or live-streaming sessions requires prior permission from SAEINDIA and, where applicable, the speaker or rights holder.

## 9. Personal Information and Event Media

Personal information will be handled as described in the APAC23 Privacy Policy.

Photography and video recording may occur during the event. Participants with concerns should contact the organising team. Individual testimonials and promotional interviews will require separate permission.

## 10. Travel, Safety and Personal Property

Participants are responsible for arranging their travel documents, accommodation and any insurance they consider appropriate.

Please follow venue safety instructions and take reasonable care of personal belongings. Liability for loss, damage or injury will be determined in accordance with applicable law.

## 11. Circumstances Beyond Reasonable Control

Events beyond SAEINDIA’s reasonable control, including government restrictions, natural disasters, transport disruption or venue unavailability, may affect delivery of the event.

SAEINDIA will communicate material impacts and the applicable postponement or cancellation arrangements. Nothing in these terms excludes rights or remedies that cannot lawfully be excluded.

## 12. Governing Law and Disputes

These terms are governed by the laws of India. Please contact SAEINDIA first so that any concern can be addressed promptly.
'''


def seed(apps, schema_editor):
    Legal = apps.get_model('core', 'LegalPage')
    Footer = apps.get_model('core', 'FooterSection')
    Link = apps.get_model('core', 'FooterLegalLink')
    Legal.objects.get_or_create(slug='terms', defaults=dict(
        title='Terms & Conditions', subtitle=TERMS_SUBTITLE, content=TERMS, order=1))
    footer = Footer.objects.filter(pk=1).first()
    if footer:
        # only fill an empty link, never overwrite one that was typed in the admin
        Link.objects.filter(footer=footer, label='Terms & Conditions', link='').update(link='#legal-terms')


class Migration(migrations.Migration):
    dependencies = [('core', '0051_legal_pages')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
