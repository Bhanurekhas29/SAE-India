import os

from django.conf import settings
from django.shortcuts import render

from . import models as m


def build_wheel(hero, size=400, r_in=82, r_out=192):
    """Slice geometry for the Hero wheel: an SVG path per slice plus label and icon positions (in % of the wheel)."""
    import math
    if not hero or not hero.show_wheel:
        return []
    slices = live(hero.wheel_slices.all())
    n = len(slices)
    if not n:
        return []
    cx = cy = size / 2
    step = 360 / n

    def pt(r, deg):
        a = math.radians(deg)
        return cx + r * math.cos(a), cy + r * math.sin(a)

    out = []
    for i, sl in enumerate(slices):
        a0, a1 = -90 + i * step, -90 + (i + 1) * step
        mid = (a0 + a1) / 2
        x0, y0 = pt(r_out, a0)
        x1, y1 = pt(r_out, a1)
        x2, y2 = pt(r_in, a1)
        x3, y3 = pt(r_in, a0)
        big = 1 if step > 180 else 0
        d = (f'M{x0:.2f},{y0:.2f} A{r_out},{r_out} 0 {big} 1 {x1:.2f},{y1:.2f} '
             f'L{x2:.2f},{y2:.2f} A{r_in},{r_in} 0 {big} 0 {x3:.2f},{y3:.2f} Z')
        lx, ly = pt((r_in + r_out) / 2 - 9, mid)
        ix, iy = pt(r_out + 2, mid)
        out.append({'title': sl.title, 'icon': sl.icon, 'd': d, 'grad': i % 3,
                    'lx': round(lx / size * 100, 2), 'ly': round(ly / size * 100, 2),
                    'ix': round(ix / size * 100, 2), 'iy': round(iy / size * 100, 2)})
    return out


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
    header = with_items(solo(m.HeaderSettings), 'menu_items', 'button_options')
    seo = m.SEOSettings.objects.filter(pk=1).first()
    credits = solo(m.Credits)

    footer = with_items(solo(m.FooterSection), 'socials', 'links', 'legal_links')
    if footer is not None:
        footer.socials_live = [s for s in footer.socials_live if s.url]

    contact = with_items(solo(m.ContactSection), 'people', 'qr_codes')

    site_name = header.site_name if header else 'SAE India'
    page_title = (seo.meta_title if seo and seo.meta_title else site_name)

    hero = with_items(solo(m.HeroSection), 'taglines', 'info_chips')

    context = {
        'asset_version': asset_version(),
        'page_title': page_title,
        'meta_description': seo.meta_description if seo else '',
        'meta_keywords': seo.meta_keywords if seo else '',
        'og_image': seo.og_image if seo and seo.og_image else None,
        'site_name': site_name,
        'header': header,
        'hero': hero,
        'wheel': build_wheel(hero),
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
        'floating': solo(m.FloatingButtons),
        'legal_pages': list(live(m.LegalPage.objects.all())),
    }
    return render(request, 'core/index.html', context)
