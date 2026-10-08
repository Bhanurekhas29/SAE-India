import os

from django.conf import settings
from django.shortcuts import render

from . import models as m


def asset_version():
    """Changes whenever main.css / main.js change, so browsers never keep a stale copy."""
    base = os.path.join(settings.BASE_DIR, 'core', 'static', 'core')
    stamps = []
    for rel in ('css/main.css', 'js/main.js'):
        try:
            stamps.append(int(os.path.getmtime(os.path.join(base, rel))))
        except OSError:
            pass
    return max(stamps) if stamps else 0


def live(qs):
    """Only rows that are switched on and not soft-deleted."""
    names = {f.name for f in qs.model._meta.fields}
    flt = {}
    if 'is_active' in names:
        flt['is_active'] = True
    if 'is_delete' in names:
        flt['is_delete'] = False
    return qs.filter(**flt)


def solo(model):
    """The single row of a section, or None when it is missing or switched off."""
    obj = model.objects.filter(pk=1).first()
    if obj is None or getattr(obj, 'is_active', True) is False:
        return None
    return obj


def with_items(obj, *relations):
    """Attach the visible rows of each related manager as <name>_live."""
    if obj is not None:
        for name in relations:
            setattr(obj, f'{name}_live', list(live(getattr(obj, name).all())))
    return obj


def build_committees(section):
    if section is None:
        return None
    committees = list(live(section.committees.all()))
    for committee in committees:
        roles = (m.CommitteeRole.objects
                 .filter(committee=committee, is_active=True, member__is_active=True, member__is_delete=False)
                 .select_related('member').order_by('order', 'id'))
        committee.entries = list(roles)
    section.committees_live = committees
    return section


def build_matrix(section):
    if section is None:
        return None
    tiers = list(live(section.tiers.all()))
    categories = list(live(section.categories.all()))
    for category in categories:
        rows = list(live(category.rows.all()))
        for row in rows:
            by_tier = {c.tier_id: c for c in row.cells.select_related('tier')}
            row.cells_live = [by_tier.get(t.id) for t in tiers]
        category.rows_live = rows
    section.tiers_live = tiers
    section.categories_live = categories
    return section


def index(request):
    header = with_items(solo(m.HeaderSettings), 'menu_items')
    seo = m.SEOSettings.objects.filter(pk=1).first()
    credits = solo(m.Credits)

    footer = with_items(solo(m.FooterSection), 'socials', 'links', 'legal_links')
    if footer is not None:
        footer.socials_live = [s for s in footer.socials_live if s.url]

    contact = with_items(solo(m.ContactSection), 'people')

    site_name = header.site_name if header else 'SAE India'
    page_title = (seo.meta_title if seo and seo.meta_title else site_name)

    context = {
        'asset_version': asset_version(),
        'page_title': page_title,
        'meta_description': seo.meta_description if seo else '',
        'meta_keywords': seo.meta_keywords if seo else '',
        'og_image': seo.og_image if seo and seo.og_image else None,
        'site_name': site_name,
        'header': header,
        'hero': with_items(solo(m.HeroSection), 'taglines', 'info_chips'),
        'about': with_items(solo(m.AboutSection), 'stats'),
        'topics': with_items(solo(m.TopicsSection), 'cards'),
        'takeaways': with_items(solo(m.TakeawaysSection), 'cards'),
        'gain': with_items(solo(m.GainSection), 'cards'),
        'committee': build_committees(solo(m.CommitteeSection)),
        'stats': with_items(solo(m.StatsSection), 'items'),
        'sponsorship': with_items(solo(m.SponsorshipSection), 'packages'),
        'matrix': build_matrix(solo(m.MatrixSection)),
        'exposition': with_items(solo(m.ExpositionSection), 'booths'),
        'special': with_items(solo(m.SpecialSponsorSection), 'cards'),
        'meeting': with_items(solo(m.MeetingRoomSection), 'details', 'features'),
        'techhive': with_items(solo(m.TechHiveSection), 'deliverables', 'rates'),
        'gallery': with_items(solo(m.GallerySection), 'images'),
        'partners': with_items(solo(m.PartnersSection), 'logos'),
        'banner': with_items(solo(m.BannerSection), 'items', 'info_cells'),
        'contact': contact,
        'coordinators': with_items(solo(m.CoordinatorsSection), 'coordinators', 'desks'),
        'footer': footer,
        'credits': credits,
    }
    return render(request, 'core/index.html', context)
