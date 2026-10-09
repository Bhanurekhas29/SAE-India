from django.core.mail import get_connection
from django.db import models


ICON_HELP = (
    "Enter a Google Material Symbols icon name (e.g. bolt, cloud, headset_mic). "
    "Browse available names at fonts.google.com/icons"
)


class SingletonModel(models.Model):
    """Exactly one row per model."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # never deletable

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class HeaderSettings(SingletonModel):
    is_active = models.BooleanField(
        'Show header', default=True,
        help_text='Untick to remove the header from the website.')
    site_name = models.CharField(max_length=120, default='SAE India', help_text='Used as the logo alt text.')
    logo = models.ImageField(upload_to='header/', blank=True, help_text='Shown large in the sticky header; links to the top of the page.')
    show_button = models.BooleanField('Show header button', default=True)
    button_text = models.CharField(max_length=40, blank=True, default='Register Now')
    button_link = models.CharField(max_length=200, blank=True, default='#contact',
                                   help_text='Section anchor like #contact, or a full URL.')
    button_new_tab = models.BooleanField('Open button link in a new tab', default=False)

    class Meta:
        verbose_name = 'Header & Menu'
        verbose_name_plural = 'Header & Menu'

    def __str__(self):
        return 'Header & Menu'


class MenuItem(models.Model):
    header = models.ForeignKey(HeaderSettings, on_delete=models.CASCADE, related_name='menu_items')
    label = models.CharField(max_length=60)
    link = models.CharField(max_length=200, help_text='Section anchor like #about, or a full URL.')
    open_in_new_tab = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Menu item'
        ordering = ['order', 'id']

    def __str__(self):
        return self.label


class HeroSection(SingletonModel):
    is_active = models.BooleanField(
        'Show this section on the website', default=True,
        help_text='Untick to remove the whole Hero section from the live site.')
    menu_anchor = models.SlugField(
        'Section ID / anchor', max_length=40, default='home',
        help_text='Menu links point here, e.g. "home" is reached with #home.')

    pill_text = models.CharField('Pill tag text', max_length=120, blank=True)
    pill_show_dot = models.BooleanField('Show dot before pill text', default=True)

    heading_pre = models.CharField('Heading: first part', max_length=100, blank=True, help_text='e.g. Auto')
    heading_highlight = models.CharField(
        'Heading: highlighted word', max_length=100, blank=True,
        help_text='Shown in the accent colour with an underline, e.g. Performance')
    heading_post = models.CharField('Heading: second line', max_length=200, blank=True,
                                    help_text='e.g. Automotive Engineering Conference')

    show_countdown = models.BooleanField('Show countdown', default=True)
    edition_label = models.CharField(max_length=60, blank=True, help_text='e.g. 23RD EDITION')
    event_datetime = models.DateTimeField(
        'Event date & time', null=True, blank=True,
        help_text='Countdown target, in India time (IST).')
    countdown_ended_text = models.CharField(max_length=80, default='Event started')

    primary_button_text = models.CharField(max_length=40, blank=True)
    primary_button_link = models.CharField(max_length=200, blank=True, help_text='Section anchor like #contact, or a full URL.')
    show_primary_button = models.BooleanField('Show primary button', default=True)
    secondary_button_text = models.CharField(max_length=40, blank=True)
    secondary_button_link = models.CharField(max_length=200, blank=True)
    show_secondary_button = models.BooleanField('Show secondary button', default=True)

    background_image = models.ImageField(upload_to='hero/', blank=True,
                                         help_text='Full-width hero background (the car and city image).')
    overlay_text = models.CharField('Text on the image', max_length=120, blank=True,
                                    help_text='Script text shown over the image, e.g. Shaping the Future of Mobility')

    class Meta:
        verbose_name = 'Hero Section'
        verbose_name_plural = 'Hero Section'

    def __str__(self):
        return 'Hero Section'


class HeroTagline(models.Model):
    hero = models.ForeignKey(HeroSection, on_delete=models.CASCADE, related_name='taglines')
    text = models.CharField(max_length=60)
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Tagline'
        ordering = ['order', 'id']

    def __str__(self):
        return self.text


class HeroInfoChip(models.Model):
    hero = models.ForeignKey(HeroSection, on_delete=models.CASCADE, related_name='info_chips')
    icon = models.CharField(max_length=60, default='event', help_text=ICON_HELP)
    text = models.CharField(max_length=150)
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Info chip'
        ordering = ['order', 'id']

    def __str__(self):
        return self.text


class AboutSection(SingletonModel):
    is_active = models.BooleanField(
        'Show this section on the website', default=True,
        help_text='Untick to remove the whole About section from the live site.')
    menu_anchor = models.SlugField(
        'Section ID / anchor', max_length=40, default='about',
        help_text='Menu links point here, e.g. "about" is reached with #about.')
    pill_text = models.CharField('Pill tag text', max_length=120, blank=True)
    heading = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField('Circular photo', upload_to='about/', blank=True)

    show_badge = models.BooleanField('Show round badge on photo', default=True)
    badge_icon = models.CharField(max_length=60, default='directions_car', help_text=ICON_HELP)
    badge_title = models.CharField(max_length=80, blank=True, help_text='e.g. AUTO PERFORMANCE')
    badge_year = models.CharField(max_length=20, blank=True, help_text='e.g. 2026')

    show_button = models.BooleanField('Show button', default=True)
    button_text = models.CharField(max_length=40, blank=True)
    button_link = models.CharField(max_length=200, blank=True, help_text='Section anchor like #contact, or a full URL.')

    class Meta:
        verbose_name = 'About Section'
        verbose_name_plural = 'About Section'

    def __str__(self):
        return 'About Section'


class AboutStat(models.Model):
    about = models.ForeignKey(AboutSection, on_delete=models.CASCADE, related_name='stats')
    icon = models.CharField(max_length=60, default='star', help_text=ICON_HELP)
    number = models.CharField(max_length=30, help_text='e.g. 1,000+ or 3 Days')
    label = models.CharField(max_length=60, help_text='e.g. Attendees')
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Stat card'
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.number} {self.label}'


class TopicsSection(SingletonModel):
    is_active = models.BooleanField(
        'Show this section on the website', default=True,
        help_text='Untick to remove the whole Topics section from the live site.')
    menu_anchor = models.SlugField(
        'Section ID / anchor', max_length=40, default='topics',
        help_text='Menu links point here, e.g. "topics" is reached with #topics.')
    eyebrow = models.CharField('Small label above heading', max_length=80, blank=True)
    heading_pre = models.CharField('Heading: first part', max_length=150, blank=True)
    heading_highlight = models.CharField('Heading: highlighted part', max_length=150, blank=True,
                                         help_text='Shown in the accent colour.')
    subtext = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Topics Section'
        verbose_name_plural = 'Topics Section'

    def __str__(self):
        return 'Topics Section'


class TopicCard(models.Model):
    section = models.ForeignKey(TopicsSection, on_delete=models.CASCADE, related_name='cards')
    icon_image = models.ImageField(
        'Icon image', upload_to='topics/icons/', blank=True,
        help_text='Upload the round icon shown at the top-left of the card (PNG, SVG or WebP, square).')
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    image = models.ImageField(
        'Card photo', upload_to='topics/', blank=True,
        help_text='Background photo shown at the top-right of the card, fading out diagonally behind the icon and title.')
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Topic card'
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class TakeawaysSection(SingletonModel):
    is_active = models.BooleanField(
        'Show this section on the website', default=True,
        help_text='Untick to remove the whole Key Takeaways section from the live site.')
    menu_anchor = models.SlugField(
        'Section ID / anchor', max_length=40, default='takeaways',
        help_text='Menu links point here, e.g. "takeaways" is reached with #takeaways.')
    pill_text = models.CharField('Pill tag text', max_length=120, blank=True)
    pill_show_dot = models.BooleanField('Show dot before pill text', default=True)
    heading = models.CharField(max_length=200, blank=True)
    subtext = models.TextField(blank=True)
    show_link = models.BooleanField('Show top-right link', default=True)
    link_text = models.CharField(max_length=60, blank=True)
    link_url = models.CharField(max_length=200, blank=True, help_text='Section anchor like #topics, or a full URL.')

    class Meta:
        verbose_name = 'Key Takeaways Section'
        verbose_name_plural = 'Key Takeaways Section'

    def __str__(self):
        return 'Key Takeaways Section'


class TakeawayCard(models.Model):
    section = models.ForeignKey(TakeawaysSection, on_delete=models.CASCADE, related_name='cards')
    icon = models.CharField(max_length=60, default='star', help_text=ICON_HELP)
    title = models.CharField(max_length=80)
    track_label = models.CharField(
        max_length=30, blank=True,
        help_text='Leave empty to number automatically (Track 01, Track 02...).')
    values_label = models.CharField(max_length=60, default='CORE VALUES')
    bullets = models.TextField(help_text='One bullet per line.')
    link_text = models.CharField('Action link text', max_length=60, blank=True)
    link_url = models.CharField('Action link URL', max_length=200, blank=True,
                                help_text='Section anchor like #contact, or a full URL.')
    accent_color = models.CharField('Left bar colour', max_length=7, default='#F59E0B',
                                    help_text='Hex colour, e.g. #F59E0B')
    bullet_color = models.CharField('Bullet dot colour', max_length=7, default='#059669',
                                    help_text='Hex colour, e.g. #059669')
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Takeaway card'
        ordering = ['order', 'id']

    def __str__(self):
        return self.title

    @property
    def bullet_list(self):
        return [line.strip() for line in self.bullets.splitlines() if line.strip()]


class GainSection(SingletonModel):
    is_active = models.BooleanField(
        'Show this section on the website', default=True,
        help_text='Untick to remove the whole "What You\'ll Gain" section from the live site.')
    menu_anchor = models.SlugField(
        'Section ID / anchor', max_length=40, default='gain',
        help_text='Menu links point here, e.g. "gain" is reached with #gain.')
    pill_text = models.CharField('Pill tag text', max_length=120, blank=True)
    pill_show_dot = models.BooleanField('Show dot before pill text', default=True)
    heading = models.CharField(max_length=200, blank=True)

    show_video = models.BooleanField('Show video box', default=True)
    video_thumbnail = models.ImageField(upload_to='gain/', blank=True,
                                        help_text='Cover image shown in the video box.')
    video_url = models.URLField('Video link', blank=True,
                                help_text='YouTube / Vimeo link opened when the play button is clicked.')
    video_caption = models.CharField(
        max_length=120, blank=True,
        help_text='Words shown at the bottom of the video, separated by commas, e.g. Learn, Network, Grow')

    class Meta:
        verbose_name = "What You'll Gain Section"
        verbose_name_plural = "What You'll Gain Section"

    def __str__(self):
        return "What You'll Gain Section"

    @property
    def caption_words(self):
        return [w.strip() for w in self.video_caption.split(',') if w.strip()]


class GainCard(models.Model):
    section = models.ForeignKey(GainSection, on_delete=models.CASCADE, related_name='cards')
    icon = models.CharField(max_length=60, default='star', help_text=ICON_HELP)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=250, blank=True)
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Gain card'
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class CommitteeSection(SingletonModel):
    is_active = models.BooleanField(
        'Show this section on the website', default=True,
        help_text='Untick to remove all committees from the live site.')
    menu_anchor = models.SlugField(
        'Section ID / anchor', max_length=40, default='committee',
        help_text='Menu links point here, e.g. "committee" is reached with #committee.')

    class Meta:
        verbose_name = 'Committee Section'
        verbose_name_plural = 'Committee Section'

    def __str__(self):
        return 'Committee Section'


class Committee(models.Model):
    section = models.ForeignKey(CommitteeSection, on_delete=models.CASCADE, related_name='committees')
    pill_text = models.CharField('Pill tag text', max_length=80, default='Members')
    pill_show_dot = models.BooleanField('Show dot before pill text', default=True)
    title = models.CharField(max_length=150, help_text='e.g. Steering Committee')
    background_image = models.ImageField(upload_to='committees/', blank=True,
                                         help_text='Faint blurred photo behind this committee.')
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Committee'
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class CommitteeMember(models.Model):
    name = models.CharField(max_length=120, help_text='Include the title, e.g. Dr. G. Nagarajan')
    designation = models.CharField(max_length=250, blank=True, help_text='Organisation / position line.')
    photo = models.ImageField(upload_to='members/', blank=True,
                              help_text='Square photo. Leave empty to show the default avatar.')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Committee Member'
        verbose_name_plural = 'Committee Members'
        ordering = ['name']

    def __str__(self):
        return self.name


class CommitteeRole(models.Model):
    member = models.ForeignKey(CommitteeMember, on_delete=models.CASCADE, related_name='roles')
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name='roles')
    role = models.CharField(max_length=100, help_text='e.g. Patron, SC Chair, Member')
    order = models.PositiveIntegerField(default=0, help_text='Position inside the committee. Lower numbers first.')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Committee role'
        ordering = ['committee__order', 'order', 'id']

    def __str__(self):
        return f'{self.member} - {self.committee} ({self.role})'


class StatsSection(SingletonModel):
    is_active = models.BooleanField(
        'Show this section on the website', default=True,
        help_text='Untick to remove the whole Stats section from the live site.')
    menu_anchor = models.SlugField(
        'Section ID / anchor', max_length=40, default='stats',
        help_text='Menu links point here, e.g. "stats" is reached with #stats.')
    background_image = models.ImageField(upload_to='stats/', blank=True,
                                         help_text='Blurred photo behind the stats panel.')
    hover_color = models.CharField('Number colour on hover', max_length=7, default='#FCD34D',
                                   help_text='Hex colour the numbers turn when hovered, e.g. #FCD34D')

    class Meta:
        verbose_name = 'Stats Section'
        verbose_name_plural = 'Stats Section'

    def __str__(self):
        return 'Stats Section'


class StatItem(models.Model):
    section = models.ForeignKey(StatsSection, on_delete=models.CASCADE, related_name='items')
    number = models.CharField(max_length=20, help_text='Digits only, e.g. 2,000 (counts up on scroll).')
    suffix = models.CharField(max_length=10, blank=True, default='+', help_text='Shown after the number, e.g. +')
    label = models.CharField(max_length=80, help_text='e.g. VISITORS')
    description = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Stat'
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.number}{self.suffix} {self.label}'


class SponsorshipSection(SingletonModel):
    is_active = models.BooleanField(
        'Show this section on the website', default=True,
        help_text='Untick to remove the whole Sponsorship section from the live site.')
    menu_anchor = models.SlugField(
        'Section ID / anchor', max_length=40, default='sponsors',
        help_text='Menu links point here, e.g. "sponsors" is reached with #sponsors.')
    pill_icon = models.CharField(max_length=60, blank=True, default='workspace_premium', help_text=ICON_HELP)
    pill_text = models.CharField('Pill tag text', max_length=120, blank=True)
    heading = models.CharField(max_length=200, blank=True)
    subtext = models.TextField(blank=True)
    show_tagline = models.BooleanField('Show top-right tagline', default=True)
    tagline_words = models.CharField(
        max_length=120, blank=True,
        help_text='Words separated by commas, e.g. Partner, Grow, Lead')
    background_image = models.ImageField(upload_to='sponsorship/', blank=True,
                                         help_text='Blurred photo behind the section.')

    class Meta:
        verbose_name = 'Sponsorship: Packages'
        verbose_name_plural = 'Sponsorship: Packages'

    def __str__(self):
        return 'Sponsorship Section'

    @property
    def tagline_list(self):
        return [w.strip() for w in self.tagline_words.split(',') if w.strip()]


class SponsorPackage(models.Model):
    section = models.ForeignKey(SponsorshipSection, on_delete=models.CASCADE, related_name='packages')
    tier_label = models.CharField('Tier pill', max_length=30, help_text='e.g. PLATINUM')
    title = models.CharField('Package name', max_length=80, help_text='e.g. Platinum Sponsor')
    currency_symbol = models.CharField(max_length=5, default='$')
    price = models.CharField(max_length=30, help_text='e.g. 25,000')
    price_unit = models.CharField(max_length=20, blank=True, default='/USD')
    description = models.CharField(max_length=250, blank=True)
    benefits = models.TextField(help_text='One benefit per line.')
    button_text = models.CharField(max_length=40, default='Get Started')
    button_link = models.CharField(max_length=200, blank=True, default='#contact',
                                   help_text='Section anchor like #contact, or a full URL.')
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first. Card numbers (01, 02...) follow this.')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Sponsor package'
        ordering = ['order', 'id']

    def __str__(self):
        return self.title

    @property
    def benefit_list(self):
        return [line.strip() for line in self.benefits.splitlines() if line.strip()]


class MatrixSection(SingletonModel):
    is_active = models.BooleanField(
        'Show this section on the website', default=True,
        help_text='Untick to remove the whole Deliverables Matrix from the live site.')
    menu_anchor = models.SlugField(
        'Section ID / anchor', max_length=40, default='deliverables',
        help_text='Menu links point here, e.g. "deliverables" is reached with #deliverables.')
    title = models.CharField(max_length=150, blank=True)
    note = models.CharField('Note (top-right of title bar)', max_length=200, blank=True)
    first_column_title = models.CharField(max_length=80, default='Deliverables & Entitlements')

    class Meta:
        verbose_name = 'Sponsorship: Deliverables Matrix'
        verbose_name_plural = 'Sponsorship: Deliverables Matrix'

    def __str__(self):
        return 'Deliverables Matrix'


class MatrixTier(models.Model):
    section = models.ForeignKey(MatrixSection, on_delete=models.CASCADE, related_name='tiers')
    name = models.CharField(max_length=60, help_text='Column heading, e.g. Platinum')
    price = models.CharField(max_length=40, blank=True, help_text='e.g. ₹15,00,000')
    is_highlighted = models.BooleanField('Highlight column', default=False)
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first (left).')
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Tier (column)'
        ordering = ['order', 'id']

    def __str__(self):
        return self.name


class MatrixCategory(models.Model):
    section = models.ForeignKey(MatrixSection, on_delete=models.CASCADE, related_name='categories')
    title = models.CharField(max_length=150, help_text='e.g. 1. EXECUTIVE & THOUGHT LEADERSHIP PRESENCE')
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Category (row group)'
        verbose_name_plural = 'Categories (row groups)'
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class MatrixRow(models.Model):
    category = models.ForeignKey(MatrixCategory, on_delete=models.CASCADE, related_name='rows')
    label = models.CharField(max_length=200, help_text='Row heading, e.g. Presence at Technical Session')
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first inside the category.')
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Sponsorship: Matrix Row'
        verbose_name_plural = 'Sponsorship: Matrix Rows'
        ordering = ['category__order', 'order', 'id']

    def __str__(self):
        return self.label


class MatrixCell(models.Model):
    STYLES = [
        ('text', 'Normal text'), ('bold', 'Bold text'), ('badge', 'Badge'),
        ('yes', 'Yes (green tick)'), ('dash', 'Dash'), ('na', 'Not applicable'),
    ]
    row = models.ForeignKey(MatrixRow, on_delete=models.CASCADE, related_name='cells')
    tier = models.ForeignKey(MatrixTier, on_delete=models.CASCADE, related_name='cells')
    style = models.CharField(max_length=10, choices=STYLES, default='text')
    text = models.CharField(max_length=150, blank=True,
                            help_text='Leave empty for Yes / Dash / Not applicable (they show their own text).')
    subtext = models.CharField('Small text below', max_length=100, blank=True, help_text='e.g. 4 times a day')

    class Meta:
        verbose_name = 'Cell'
        ordering = ['tier__order', 'id']

    def __str__(self):
        return f'{self.row} / {self.tier}'


class ExpositionSection(SingletonModel):
    is_active = models.BooleanField(
        'Show this section on the website', default=True,
        help_text='Untick to remove the whole Exposition section from the live site.')
    menu_anchor = models.SlugField(
        'Section ID / anchor', max_length=40, default='exposition',
        help_text='Menu links point here, e.g. "exposition" is reached with #exposition.')
    pill_text = models.CharField('Pill tag text', max_length=150, blank=True)
    heading = models.CharField(max_length=200, blank=True)
    subtext = models.TextField(blank=True)

    show_top_button = models.BooleanField('Show top-right button', default=True)
    top_button_text = models.CharField(max_length=40, blank=True)
    top_button_link = models.CharField(max_length=200, blank=True, default='#contact',
                                       help_text='Section anchor like #contact, or a full URL.')

    venue_image = models.ImageField(upload_to='exposition/', blank=True)
    venue_tag = models.CharField('Venue tag', max_length=50, blank=True, help_text='e.g. LIVE VENUE VIEW')
    venue_title = models.CharField(max_length=200, blank=True)
    venue_subtext = models.CharField(max_length=200, blank=True)

    show_pass_box = models.BooleanField('Show pass entitlements box', default=True)
    pass_title = models.CharField(max_length=80, blank=True, default='Exhibitor Pass Entitlements')
    pass_tag = models.CharField(max_length=40, blank=True, default='Official Inclusions')
    pass_count = models.CharField(max_length=10, blank=True, default='2×', help_text='Shown in the round badge')
    pass_headline = models.CharField(max_length=120, blank=True)
    pass_subline = models.CharField(max_length=160, blank=True)
    pass_includes = models.CharField('Pass includes', max_length=250, blank=True)
    pass_excludes = models.CharField('Pass excludes', max_length=250, blank=True)
    gst_footnote = models.CharField(max_length=120, blank=True)
    footer_link_text = models.CharField(max_length=60, blank=True)
    footer_link_url = models.CharField(max_length=200, blank=True, default='#contact')

    class Meta:
        verbose_name = 'Sponsorship: Exposition'
        verbose_name_plural = 'Sponsorship: Exposition'

    def __str__(self):
        return 'Exposition Section'


class BoothSpace(models.Model):
    BUTTON_STYLES = [('outline', 'Outline'), ('dark', 'Dark'), ('accent', 'Accent colour')]
    section = models.ForeignKey(ExpositionSection, on_delete=models.CASCADE, related_name='booths')
    icon = models.CharField(max_length=60, default='grid_view', help_text=ICON_HELP)
    size_label = models.CharField(max_length=40, help_text='e.g. 9 sq. mtr.')
    grid_label = models.CharField(max_length=30, blank=True, help_text='e.g. (3 × 3)')
    space_type = models.CharField(max_length=30, blank=True, default='RAW SPACE')
    dimensions = models.CharField(max_length=30, blank=True, help_text='e.g. 3m × 3m')
    category = models.CharField(max_length=80, blank=True, help_text='e.g. STARTUP & SPECIALIST')
    name = models.CharField(max_length=80, help_text='e.g. Standard Turnkey')
    price_label = models.CharField(max_length=40, blank=True, default='VALUE IN INR *')
    currency_symbol = models.CharField(max_length=5, default='₹')
    price = models.CharField(max_length=30, help_text='e.g. 1,50,000')
    gst_note = models.CharField(max_length=80, blank=True, default='*18% GST applicable extra')
    button_text = models.CharField(max_length=40, default='BOOK SPACE')
    button_link = models.CharField(max_length=200, blank=True, default='#contact',
                                   help_text='Section anchor like #contact, or a full URL.')
    button_style = models.CharField(max_length=10, choices=BUTTON_STYLES, default='outline')
    tint_color = models.CharField('Card tint colour', max_length=7, default='#F0FDFA')
    accent_color = models.CharField('Accent colour', max_length=7, default='#0D9488',
                                    help_text='Used for the size block, the flagship border and "Accent" buttons.')
    flagship_tag = models.CharField(max_length=40, blank=True,
                                    help_text='e.g. FLAGSHIP OPTION. Fill this to give the card the highlighted look.')
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Booth space'
        ordering = ['order', 'id']

    def __str__(self):
        return self.name


class SpecialSponsorSection(SingletonModel):
    is_active = models.BooleanField(
        'Show this section on the website', default=True,
        help_text='Untick to remove the whole Special Event Sponsorships section from the live site.')
    menu_anchor = models.SlugField(
        'Section ID / anchor', max_length=40, default='special-sponsorships',
        help_text='Menu links point here, e.g. "special-sponsorships" is reached with #special-sponsorships.')
    pill_text = models.CharField('Pill tag text', max_length=120, blank=True)
    heading = models.CharField(max_length=200, blank=True)
    subtext = models.TextField(blank=True)
    show_tag = models.BooleanField('Show top-right tag', default=True)
    tag_text = models.CharField(max_length=60, blank=True)

    class Meta:
        verbose_name = 'Sponsorship: Special Events'
        verbose_name_plural = 'Sponsorship: Special Events'

    def __str__(self):
        return 'Special Event Sponsorships'


class SpecialSponsorCard(models.Model):
    BUTTON_STYLES = [('outline', 'Outline'), ('dark', 'Dark'), ('accent', 'Accent colour')]
    section = models.ForeignKey(SpecialSponsorSection, on_delete=models.CASCADE, related_name='cards')
    strip_text = models.CharField('Side strip text', max_length=40, help_text='e.g. NETWORKING BREAKS')
    strip_color = models.CharField('Side strip / accent colour', max_length=7, default='#0D9488')
    exclusive_tag = models.CharField(max_length=30, blank=True, help_text='e.g. EXCLUSIVE. Leave empty for none.')
    slot_tag = models.CharField(max_length=30, blank=True, default='Slot Available',
                                help_text='Leave empty to hide.')
    is_highlighted = models.BooleanField('Highlight card (coloured border)', default=False)
    name = models.CharField(max_length=100, help_text='e.g. Hi-Tea Sponsor')
    description = models.CharField(max_length=250, blank=True)
    price_label = models.CharField(max_length=30, blank=True, default='INVESTMENT')
    currency_symbol = models.CharField(max_length=5, default='₹')
    price = models.CharField(max_length=30, help_text='e.g. 3,00,000')
    price_note_prefix = models.CharField('Small price note prefix', max_length=10, blank=True, default='INR',
                                         help_text='Shows as "(INR 3,00,000)" under the price. Leave empty to hide.')
    deliverables_label = models.CharField(max_length=60, blank=True, default='DELIVERABLES & ENTITLEMENTS')
    deliverables = models.TextField(blank=True, help_text='One item per line.')
    passes_label = models.CharField(max_length=40, blank=True, default='Complimentary Passes:')
    passes_value = models.CharField(max_length=40, blank=True, help_text='e.g. 1 Delegate')
    button_text = models.CharField(max_length=40, default='EXPRESS INTEREST')
    button_link = models.CharField(max_length=200, blank=True, default='#contact',
                                   help_text='Section anchor like #contact, or a full URL.')
    button_style = models.CharField(max_length=10, choices=BUTTON_STYLES, default='outline')
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Sponsorship card'
        ordering = ['order', 'id']

    def __str__(self):
        return self.name

    @property
    def deliverable_list(self):
        return [line.strip() for line in self.deliverables.splitlines() if line.strip()]


class MeetingRoomSection(SingletonModel):
    is_active = models.BooleanField(
        'Show this section on the website', default=True,
        help_text='Untick to remove the whole Business Meeting Room section from the live site.')
    menu_anchor = models.SlugField(
        'Section ID / anchor', max_length=40, default='meeting-room',
        help_text='Menu links point here, e.g. "meeting-room" is reached with #meeting-room.')
    pill_text = models.CharField('Pill tag text', max_length=80, blank=True)
    title = models.CharField(max_length=120, blank=True)
    currency_label = models.CharField('Currency', max_length=10, default='INR')
    price = models.CharField(max_length=30, blank=True, help_text='e.g. 5,000')
    price_unit = models.CharField(max_length=20, blank=True, default='/ hour')
    gst_note = models.CharField(max_length=120, blank=True)
    button_text = models.CharField(max_length=40, blank=True)
    button_link = models.CharField(max_length=200, blank=True, default='#contact',
                                   help_text='Section anchor like #contact, or a full URL.')

    class Meta:
        verbose_name = 'Business Meeting Room'
        verbose_name_plural = 'Business Meeting Room'

    def __str__(self):
        return 'Business Meeting Room'


class MeetingRoomDetail(models.Model):
    section = models.ForeignKey(MeetingRoomSection, on_delete=models.CASCADE, related_name='details')
    icon = models.CharField(max_length=60, default='sell', help_text=ICON_HELP)
    label = models.CharField(max_length=60, help_text='Bold part, e.g. Booking Fee:')
    text = models.CharField(max_length=250)
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Detail line'
        ordering = ['order', 'id']

    def __str__(self):
        return self.label


class MeetingRoomFeature(models.Model):
    section = models.ForeignKey(MeetingRoomSection, on_delete=models.CASCADE, related_name='features')
    icon = models.CharField(max_length=60, default='star', help_text=ICON_HELP)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250, blank=True)
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Feature card'
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class TechHiveSection(SingletonModel):
    is_active = models.BooleanField(
        'Show this section on the website', default=True,
        help_text='Untick to remove the whole Startup & Delegate Packages section from the live site.')
    menu_anchor = models.SlugField(
        'Section ID / anchor', max_length=40, default='techhive',
        help_text='Menu links point here, e.g. "techhive" is reached with #techhive.')
    pill_text = models.CharField('Pill tag text', max_length=120, blank=True)
    heading = models.CharField(max_length=200, blank=True)
    subtext = models.TextField(blank=True)
    show_top_button = models.BooleanField('Show top-right button', default=True)
    top_button_text = models.CharField(max_length=40, blank=True)
    top_button_link = models.CharField(max_length=200, blank=True, default='#contact',
                                       help_text='Section anchor like #contact, or a full URL.')

    # TechHive panel
    show_panel = models.BooleanField('Show TechHive panel', default=True)
    panel_tag1 = models.CharField('Tag 1', max_length=50, blank=True)
    panel_tag2 = models.CharField('Tag 2', max_length=50, blank=True)
    panel_title = models.CharField(max_length=100, blank=True)
    panel_description = models.CharField(max_length=250, blank=True)
    fee_label = models.CharField(max_length=40, blank=True, default='REGISTRATION FEE')
    fee_tag = models.CharField(max_length=40, blank=True, default='All Inclusives')
    fee_currency = models.CharField(max_length=10, default='INR')
    fee_price = models.CharField(max_length=30, blank=True, help_text='e.g. 50,000')
    fee_unit = models.CharField(max_length=30, blank=True, default='/ registration')
    fee_gst_note = models.CharField(max_length=120, blank=True)
    deliverables_label = models.CharField(max_length=80, blank=True, default='STARTUP DELIVERABLES & ENTITLEMENTS')
    apply_button_text = models.CharField(max_length=60, blank=True)
    apply_button_link = models.CharField(max_length=200, blank=True, default='#contact')

    # Delegate investment matrix
    show_delegate_matrix = models.BooleanField('Show delegate investment matrix', default=True)
    matrix_title = models.CharField(max_length=100, blank=True)
    matrix_subtitle = models.CharField(max_length=150, blank=True)
    matrix_badge = models.CharField('Top-right badge', max_length=80, blank=True,
                                    help_text='e.g. Early Bird Active till Sep 15, 2026. Leave empty to hide.')
    category_column_title = models.CharField(max_length=40, default='Category')
    category_column_note = models.CharField(max_length=40, blank=True, default='(All Nations)')
    early_column_title = models.CharField(max_length=60, blank=True)
    early_column_note = models.CharField(max_length=40, blank=True, default='EARLY BIRD')
    standard_column_title = models.CharField(max_length=60, blank=True)
    standard_column_note = models.CharField(max_length=40, blank=True, default='Standard Tariff')
    matrix_gst_note = models.CharField(max_length=150, blank=True)
    matrix_button_text = models.CharField(max_length=40, blank=True)
    matrix_button_link = models.CharField(max_length=200, blank=True, default='#contact')

    class Meta:
        verbose_name = 'Startup & Delegate Packages'
        verbose_name_plural = 'Startup & Delegate Packages'

    def __str__(self):
        return 'Startup & Delegate Packages'


class TechHiveDeliverable(models.Model):
    section = models.ForeignKey(TechHiveSection, on_delete=models.CASCADE, related_name='deliverables')
    icon = models.CharField(max_length=60, default='person', help_text=ICON_HELP)
    title = models.CharField(max_length=120)
    subline = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Deliverable'
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class DelegateRate(models.Model):
    section = models.ForeignKey(TechHiveSection, on_delete=models.CASCADE, related_name='rates')
    category = models.CharField(max_length=100, help_text='e.g. SAEINDIA Member')
    description = models.CharField(max_length=200, blank=True)
    note = models.CharField(max_length=100, blank=True, help_text='Green note under the category, e.g. Save ₹2,500 with membership')
    early_price = models.CharField(max_length=30, help_text='e.g. ₹15,000')
    standard_price = models.CharField(max_length=30, help_text='e.g. ₹17,500')
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Delegate rate'
        ordering = ['order', 'id']

    def __str__(self):
        return self.category


class GallerySection(SingletonModel):
    is_active = models.BooleanField(
        'Show this section on the website', default=True,
        help_text='Untick to remove the whole Event Gallery from the live site.')
    menu_anchor = models.SlugField(
        'Section ID / anchor', max_length=40, default='gallery',
        help_text='Menu links point here, e.g. "gallery" is reached with #gallery.')
    pill_text = models.CharField('Pill tag text', max_length=80, blank=True)
    heading = models.CharField(max_length=150, blank=True)
    subtext = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Event Gallery'
        verbose_name_plural = 'Event Gallery'

    def __str__(self):
        return 'Event Gallery'


class GalleryImage(models.Model):
    section = models.ForeignKey(GallerySection, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=200, blank=True, help_text='Also used as the image description (alt text).')
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Gallery photo'
        ordering = ['order', 'id']

    def __str__(self):
        return self.caption or f'Photo {self.pk}'


class PartnersSection(SingletonModel):
    is_active = models.BooleanField(
        'Show this section on the website', default=True,
        help_text='Untick to remove the whole Sponsors & Partners section from the live site.')
    menu_anchor = models.SlugField(
        'Section ID / anchor', max_length=40, default='partners',
        help_text='Menu links point here, e.g. "partners" is reached with #partners.')
    pill_text = models.CharField('Pill tag text', max_length=80, blank=True)
    heading = models.CharField(max_length=150, blank=True)
    autoplay = models.BooleanField('Autoplay (scrolls by itself, pauses on hover)', default=True)
    speed_seconds = models.PositiveSmallIntegerField(
        'Scroll speed (seconds per loop)', default=30,
        help_text='Higher number = slower scroll.')
    show_arrows = models.BooleanField('Show left / right arrows', default=True)

    class Meta:
        verbose_name = 'Sponsors & Partners'
        verbose_name_plural = 'Sponsors & Partners'

    def __str__(self):
        return 'Sponsors & Partners'


class PartnerLogo(models.Model):
    section = models.ForeignKey(PartnersSection, on_delete=models.CASCADE, related_name='logos')
    name = models.CharField(max_length=100, help_text='Company name (also used as the logo description).')
    logo = models.ImageField(upload_to='partners/')
    website = models.URLField(blank=True, help_text='Optional: opens in a new tab when the logo is clicked.')
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Logo'
        ordering = ['order', 'id']

    def __str__(self):
        return self.name


class BannerSection(SingletonModel):
    is_active = models.BooleanField(
        'Show this section on the website', default=True,
        help_text='Untick to remove the whole Registration Banner from the live site.')
    menu_anchor = models.SlugField(
        'Section ID / anchor', max_length=40, default='register',
        help_text='Menu links point here, e.g. "register" is reached with #register.')
    background_image = models.ImageField(upload_to='banner/', blank=True)
    pill_text = models.CharField('Pill tag text', max_length=120, blank=True)
    heading_line1 = models.CharField('Heading: first line (italic)', max_length=150, blank=True)
    heading_line2 = models.CharField('Heading: second line (accent colour)', max_length=100, blank=True)
    description = models.TextField(blank=True)
    button_text = models.CharField(max_length=40, blank=True)
    button_link = models.CharField(max_length=200, blank=True, default='#contact',
                                   help_text='Section anchor like #contact, or a full URL.')

    class Meta:
        verbose_name = 'Registration Banner'
        verbose_name_plural = 'Registration Banner'

    def __str__(self):
        return 'Registration Banner'


class BannerItem(models.Model):
    section = models.ForeignKey(BannerSection, on_delete=models.CASCADE, related_name='items')
    icon = models.CharField(max_length=60, default='event', help_text=ICON_HELP)
    text = models.CharField(max_length=120)
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Banner item'
        ordering = ['order', 'id']

    def __str__(self):
        return self.text


class BannerInfo(models.Model):
    section = models.ForeignKey(BannerSection, on_delete=models.CASCADE, related_name='info_cells')
    icon = models.CharField(max_length=60, default='info', help_text=ICON_HELP)
    label = models.CharField(max_length=80, help_text='Small capital label, e.g. CONFERENCE VENUE')
    value = models.CharField(max_length=150)
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Info strip cell'
        ordering = ['order', 'id']

    def __str__(self):
        return self.label


class ContactSection(SingletonModel):
    is_active = models.BooleanField(
        'Show this section on the website', default=True,
        help_text='Untick to remove the whole Contact section from the live site.')
    menu_anchor = models.SlugField(
        'Section ID / anchor', max_length=40, default='contact',
        help_text='Menu links point here, e.g. "contact" is reached with #contact.')
    eyebrow = models.CharField('Small label above heading', max_length=80, blank=True)
    heading = models.CharField(max_length=200, blank=True)
    side_text = models.CharField('Line on the right of the heading', max_length=200, blank=True)

    show_qr = models.BooleanField('Show QR card', default=True)
    qr_pill_text = models.CharField(max_length=60, blank=True)
    qr_title = models.CharField(max_length=80, blank=True)
    qr_subtext = models.CharField(max_length=200, blank=True)
    qr_image = models.ImageField('QR code image', upload_to='contact/', blank=True)
    qr_background_image = models.ImageField('QR card background photo', upload_to='contact/', blank=True,
                                            help_text='Faint photo behind the dark QR card.')
    qr_caption = models.CharField(max_length=60, blank=True)

    show_strip = models.BooleanField('Show bottom strip', default=True)
    strip_label = models.CharField(max_length=120, blank=True)
    strip_link_text = models.CharField(max_length=150, blank=True)
    strip_link_url = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Contact Section'
        verbose_name_plural = 'Contact Section'

    def __str__(self):
        return 'Contact Section'


class ContactQR(models.Model):
    section = models.ForeignKey(ContactSection, on_delete=models.CASCADE, related_name='qr_codes')
    label = models.CharField(max_length=60, help_text='Shown under the code, e.g. Author registration')
    image = models.ImageField(upload_to='contact/')
    link = models.URLField(blank=True, help_text='Optional: opens in a new tab when the QR code is clicked or tapped.')
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'QR code'
        ordering = ['order', 'id']

    def __str__(self):
        return self.label


class ContactPerson(models.Model):
    section = models.ForeignKey(ContactSection, on_delete=models.CASCADE, related_name='people')
    tag = models.CharField(max_length=40, blank=True, help_text='e.g. SECRETARIAT')
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=150, blank=True)
    phones = models.TextField(blank=True, help_text='One phone number per line (you can add more than one).')
    emails = models.TextField(blank=True, help_text='One email address per line (you can add more than one).')
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Contact person'
        verbose_name_plural = 'Contact people'
        ordering = ['order', 'id']

    def __str__(self):
        return self.name

    @property
    def phone_list(self):
        return [{'display': p.strip(), 'tel': ''.join(c for c in p if c.isdigit() or c == '+')}
                for p in self.phones.splitlines() if p.strip()]

    @property
    def email_list(self):
        return [e.strip() for e in self.emails.splitlines() if e.strip()]


class CoordinatorsSection(SingletonModel):
    is_active = models.BooleanField(
        'Show this section on the website', default=True,
        help_text='Untick to remove the whole Desk Coordinators section from the live site.')
    menu_anchor = models.SlugField(
        'Section ID / anchor', max_length=40, default='coordinators',
        help_text='Menu links point here, e.g. "coordinators" is reached with #coordinators.')
    eyebrow = models.CharField('Small label above heading', max_length=80, blank=True)
    heading = models.CharField(max_length=200, blank=True)
    side_text = models.CharField('Line on the right of the heading', max_length=200, blank=True)
    desk_background_image = models.ImageField(
        'Background photo for the dark desk cards', upload_to='coordinators/', blank=True)

    class Meta:
        verbose_name = 'Desk Coordinators'
        verbose_name_plural = 'Desk Coordinators'

    def __str__(self):
        return 'Desk Coordinators'


class Coordinator(models.Model):
    section = models.ForeignKey(CoordinatorsSection, on_delete=models.CASCADE, related_name='coordinators')
    name = models.CharField(max_length=100)
    phones = models.TextField(blank=True, help_text='One phone number per line (you can add more than one).')
    emails = models.TextField(blank=True, help_text='One email address per line (you can add more than one).')
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Coordinator'
        ordering = ['order', 'id']

    def __str__(self):
        return self.name

    @property
    def phone_list(self):
        return [{'display': p.strip(), 'tel': ''.join(c for c in p if c.isdigit() or c == '+')}
                for p in self.phones.splitlines() if p.strip()]

    @property
    def email_list(self):
        return [e.strip() for e in self.emails.splitlines() if e.strip()]


class DeskCard(models.Model):
    section = models.ForeignKey(CoordinatorsSection, on_delete=models.CASCADE, related_name='desks')
    tag = models.CharField(max_length=40, help_text='e.g. EXPOSITION DESK')
    name = models.CharField(max_length=100)
    phones = models.TextField(blank=True, help_text='One phone number per line (you can add more than one).')
    emails = models.TextField(blank=True, help_text='One email address per line (you can add more than one).')
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Desk card'
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.tag} - {self.name}'

    @property
    def phone_list(self):
        return [{'display': p.strip(), 'tel': ''.join(c for c in p if c.isdigit() or c == '+')}
                for p in self.phones.splitlines() if p.strip()]

    @property
    def email_list(self):
        return [e.strip() for e in self.emails.splitlines() if e.strip()]


class FooterSection(SingletonModel):
    is_active = models.BooleanField(
        'Show footer', default=True,
        help_text='Untick to remove the footer from the website.')
    tagline = models.CharField(max_length=250, blank=True)
    show_website_pill = models.BooleanField('Show website pill', default=True)
    website_text = models.CharField(max_length=100, blank=True, help_text='e.g. saeindia.org/apac23')
    website_url = models.URLField(blank=True)
    copyright_text = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name = 'Footer'
        verbose_name_plural = 'Footer'

    def __str__(self):
        return 'Footer'


class FooterSocial(models.Model):
    PLATFORMS = [
        ('facebook', 'Facebook'), ('linkedin', 'LinkedIn'), ('instagram', 'Instagram'),
        ('x', 'X (Twitter)'), ('youtube', 'YouTube'), ('whatsapp', 'WhatsApp'),
        ('telegram', 'Telegram'), ('other', 'Other'),
    ]
    footer = models.ForeignKey(FooterSection, on_delete=models.CASCADE, related_name='socials')
    platform = models.CharField(max_length=20, choices=PLATFORMS)
    url = models.URLField(blank=True, help_text='Full link to the profile or page. Inactive or empty links are hidden.')
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Social media link'
        ordering = ['order', 'id']

    def __str__(self):
        return self.get_platform_display()


class FooterLink(models.Model):
    footer = models.ForeignKey(FooterSection, on_delete=models.CASCADE, related_name='links')
    label = models.CharField(max_length=60)
    link = models.CharField(max_length=200, help_text='Section anchor like #about, or a full URL.')
    is_highlighted = models.BooleanField('Highlight (accent colour)', default=False)
    open_in_new_tab = models.BooleanField(default=False)
    use_register_dropdown = models.BooleanField(
        'Open the Register Now choices', default=False,
        help_text='Tick to show the Author / Delegate choices (set in Header & Menu) instead of the link above.')
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Footer link'
        ordering = ['order', 'id']

    def __str__(self):
        return self.label


class FooterLegalLink(models.Model):
    footer = models.ForeignKey(FooterSection, on_delete=models.CASCADE, related_name='legal_links')
    label = models.CharField(max_length=60)
    link = models.CharField(max_length=200, blank=True,
                            help_text='Section anchor or full URL. Leave empty until the page / popup / document is ready.')
    open_in_new_tab = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Legal link'
        ordering = ['order', 'id']

    def __str__(self):
        return self.label


class Credits(SingletonModel):
    text = models.CharField(max_length=150, default='Designed & Developed by Vetri IT Systems',
                            help_text='The whole line is shown as a link in the footer.')
    url = models.URLField('Link', default='https://vetriitsystems.com/')
    open_in_new_tab = models.BooleanField(default=True)
    is_active = models.BooleanField('Show credits line', default=True)

    class Meta:
        verbose_name = 'Credits'
        verbose_name_plural = 'Credits'

    def __str__(self):
        return 'Credits'


class FloatingButtons(SingletonModel):
    is_active = models.BooleanField(
        'Show floating buttons', default=True,
        help_text='Untick to remove both floating buttons from the website.')
    show_whatsapp = models.BooleanField('Show WhatsApp button', default=True)
    whatsapp_number = models.CharField(
        max_length=30, default='+91 8870471511',
        help_text='With country code, e.g. +91 8870471511')
    whatsapp_message = models.CharField(
        max_length=250, blank=True, default='Hello! I would like to know more about APAC 23.',
        help_text='Text already typed in when the chat opens. Leave empty for none.')
    show_call = models.BooleanField('Show Call button', default=True)
    call_number = models.CharField(
        max_length=30, default='+91 8870471511',
        help_text='With country code, e.g. +91 8870471511')

    class Meta:
        verbose_name = 'Floating Buttons'
        verbose_name_plural = 'Floating Buttons'

    def __str__(self):
        return 'Floating Buttons'

    @property
    def whatsapp_digits(self):
        return ''.join(c for c in self.whatsapp_number if c.isdigit())

    @property
    def call_tel(self):
        return ''.join(c for c in self.call_number if c.isdigit() or c == '+')


class HeaderButtonOption(models.Model):
    header = models.ForeignKey(HeaderSettings, on_delete=models.CASCADE, related_name='button_options')
    label = models.CharField(max_length=60, help_text='e.g. Register as Author')
    link = models.CharField(max_length=300, help_text='Full web address or a section anchor like #contact.')
    open_in_new_tab = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Header button choice'
        ordering = ['order', 'id']

    def __str__(self):
        return self.label


class LegalPage(models.Model):
    slug = models.SlugField(
        max_length=40, unique=True,
        help_text='Short name used in the link, e.g. "terms". The popup opens from a link to #legal-terms.')
    title = models.CharField(max_length=120)
    subtitle = models.TextField(
        blank=True, help_text='Lines shown under the title (one per line), e.g. the event name and dates.')
    content = models.TextField(
        help_text='Type the text. Start a heading line with ## (for example: ## 1. Registration). '
                  'Start a bullet line with a dash and a space (- like this). Leave a blank line between paragraphs.')
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')
    is_active = models.BooleanField('Show this page', default=True)
    is_delete = models.BooleanField('Deleted', default=False, help_text='Soft delete: hidden on the site.')

    class Meta:
        verbose_name = 'Legal Page'
        verbose_name_plural = 'Legal Pages (popups)'
        ordering = ['order', 'id']

    def __str__(self):
        return self.title

    @property
    def subtitle_lines(self):
        return [line.strip() for line in self.subtitle.splitlines() if line.strip()]

    @property
    def blocks(self):
        """The text as a list of (kind, value) blocks: 'h' heading, 'p' paragraph, 'ul' bullet list."""
        out = []
        for chunk in self.content.replace('\r\n', '\n').split('\n\n'):
            lines = [l.strip() for l in chunk.split('\n') if l.strip()]
            para, bullets = [], []

            def flush():
                if para:
                    out.append(('p', ' '.join(para)))
                    para.clear()
                if bullets:
                    out.append(('ul', list(bullets)))
                    bullets.clear()

            for l in lines:
                if l.startswith('## '):
                    flush()
                    out.append(('h', l[3:].strip()))
                elif l.startswith('- ') or l.startswith('\u2022'):
                    if para:
                        flush()
                    bullets.append(l.lstrip('-\u2022').strip())
                else:
                    if bullets:
                        flush()
                    para.append(l)
            flush()
        return out


class SEOSettings(SingletonModel):
    meta_title = models.CharField(
        'Page title', max_length=70, blank=True,
        help_text='Shown in the browser tab and search results (aim for under 60 characters).')
    meta_description = models.TextField(
        'Meta description', max_length=300, blank=True,
        help_text='Search result summary (aim for 150-160 characters).')
    meta_keywords = models.CharField(max_length=300, blank=True)
    og_image = models.ImageField('Social share image', upload_to='seo/', blank=True)

    class Meta:
        verbose_name = 'SEO'
        verbose_name_plural = 'SEO'

    def __str__(self):
        return 'SEO'


class EmailSettings(SingletonModel):
    smtp_host = models.CharField('SMTP host', max_length=120, default='smtp.gmail.com')
    smtp_port = models.PositiveIntegerField('SMTP port', default=587)
    use_tls = models.BooleanField('Use TLS', default=True)
    use_ssl = models.BooleanField('Use SSL', default=False, help_text='Leave off for Gmail on port 587.')
    smtp_username = models.CharField('Gmail / SMTP email address', max_length=150, blank=True)
    smtp_password = models.CharField(
        'App password', max_length=150, blank=True,
        help_text='Gmail app password (Google Account > Security > App passwords).')
    sender_name = models.CharField(max_length=100, default='SAE India')
    from_email = models.EmailField('From email', blank=True, help_text='Usually the same as the SMTP email address.')
    notification_emails = models.TextField(
        'Send enquiries to', blank=True,
        help_text='One or more email addresses, separated by commas or new lines.')
    subject_prefix = models.CharField(max_length=60, default='[SAE India] ')
    is_active = models.BooleanField('Send emails', default=True)

    class Meta:
        verbose_name = 'Email Settings'
        verbose_name_plural = 'Email Settings'

    def __str__(self):
        return 'Email Settings'

    @property
    def recipients(self):
        raw = self.notification_emails.replace('\n', ',')
        return [e.strip() for e in raw.split(',') if e.strip()]

    @property
    def from_header(self):
        return f'{self.sender_name} <{self.from_email or self.smtp_username}>'

    def get_connection(self):
        return get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host=self.smtp_host, port=self.smtp_port,
            username=self.smtp_username, password=self.smtp_password,
            use_tls=self.use_tls, use_ssl=self.use_ssl, timeout=20,
        )
