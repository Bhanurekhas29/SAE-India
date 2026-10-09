from django.db import migrations

# old card title -> new content. Prices are the brochure's "Value in INR" (page 4);
# benefit lines are taken from the Executive Deliverables Matrix (same five tiers).
# The short descriptions are the design's original wording, moved to the tier that now sits at that rank.
CARDS = {
    'Platinum Sponsor': dict(
        tier_label='TITLE', title='Title Sponsor', price='25,00,000',
        description='Maximum brand exposure and premium positioning.',
        benefits=['Inaugural / Valedictory session presence', 'Large logo on event backdrop',
                  '36 sq. mtr. Expo Space', '10 complimentary delegates and VIP lounge access']),
    'Gold Sponsor': dict(
        tier_label='PLATINUM', title='Platinum Sponsor', price='15,00,000',
        description='High visibility and strong brand presence.',
        benefits=['Keynote session presence', 'Medium logo on event backdrop',
                  '18 sq. mtr. Expo Space', '7 complimentary delegates and VIP lounge access']),
    'Silver Sponsor': dict(
        tier_label='GOLD', title='Gold Sponsor', price='10,00,000',
        description='Valuable exposure to our engaged audience.',
        benefits=['Panel discussion presence', 'Small logo on event backdrop',
                  '9 sq. mtr. Expo Space', '5 complimentary delegates']),
    'Bronze Sponsor': dict(
        tier_label='SILVER', title='Silver Sponsor', price='6,00,000',
        description='Grow your brand with targeted visibility.',
        benefits=['Chair of a technical session', 'Small logo on event backdrop',
                  'Promo video, 1 min, 2 times a day', '3 complimentary delegates']),
    'Supporter Sponsor': dict(
        tier_label='BRONZE', title='Bronze Sponsor', price='3,00,000',
        description='Be part of the movement and make an impact.',
        benefits=['Small logo on event backdrop', '1 complimentary delegate']),
}


def apply(apps, schema_editor):
    Package = apps.get_model('core', 'SponsorPackage')
    for old_title, new in CARDS.items():
        # only touch a card that still has the original design content ($ prices), never an edited one
        for card in Package.objects.filter(title=old_title, currency_symbol='$'):
            card.tier_label = new['tier_label']
            card.title = new['title']
            card.currency_symbol = '₹'
            card.price = new['price']
            card.price_unit = ''
            card.description = new['description']
            card.benefits = '\n'.join(new['benefits'])
            card.save()


class Migration(migrations.Migration):
    dependencies = [('core', '0055_takeaway_card_links')]
    operations = [migrations.RunPython(apply, migrations.RunPython.noop)]
