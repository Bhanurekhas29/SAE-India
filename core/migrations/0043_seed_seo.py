from django.db import migrations

TITLE = 'Auto Performance Automotive Engineering Conference | SAEINDIA'
DESCRIPTION = ('Join APAC 23, the Asia Pacific Automotive Engineering Conference, Nov 13-14, 2026 at '
               'Yashobhoomi, New Delhi. Explore mobility innovation, exhibit, sponsor and network.')


def seed(apps, schema_editor):
    SEO = apps.get_model('core', 'SEOSettings')
    seo, _ = SEO.objects.get_or_create(pk=1)
    if not seo.meta_title:
        seo.meta_title = TITLE
    if not seo.meta_description:
        seo.meta_description = DESCRIPTION
    if not seo.meta_keywords:
        seo.meta_keywords = 'APAC 23, automotive engineering conference, SAEINDIA, mobility, New Delhi'
    seo.save()


class Migration(migrations.Migration):
    dependencies = [('core', '0042_footer_use_header_logo')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
