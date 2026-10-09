from django import forms
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html

from . import models as m

admin.site.site_header = 'SAE India'
admin.site.site_title = 'SAE India Admin'
admin.site.index_title = 'Website Management'


class SingletonAdmin(admin.ModelAdmin):
    """One row only: the menu item opens the edit form directly."""

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        # Hidden from the "Website" group; SEO / Email Settings are linked under Users instead.
        return getattr(self, 'show_in_website_group', False) and super().has_module_permission(request)

    def changelist_view(self, request, extra_context=None):
        obj = self.model.get_solo()
        opts = self.model._meta
        return redirect(reverse(f'admin:{opts.app_label}_{opts.model_name}_change', args=[obj.pk]))


class MenuItemInline(admin.TabularInline):
    model = m.MenuItem
    extra = 1
    ordering = ('order', 'id')
    fields = ('label', 'link', 'open_in_new_tab', 'order', 'is_active', 'is_delete')


class HeaderButtonOptionInline(admin.TabularInline):
    model = m.HeaderButtonOption
    extra = 1
    verbose_name_plural = 'Register Now choices (dropdown)'
    fields = ('label', 'link', 'open_in_new_tab', 'order', 'is_active', 'is_delete')


@admin.register(m.HeaderSettings)
class HeaderSettingsAdmin(SingletonAdmin):
    show_in_website_group = True
    inlines = [MenuItemInline, HeaderButtonOptionInline]
    fieldsets = (
        ('Header', {'fields': ('is_active', 'site_name', 'logo')}),
        ('Header button', {'fields': ('show_button', 'button_text', 'button_link', 'button_new_tab')}),
    )


class HeroTaglineInline(admin.TabularInline):
    model = m.HeroTagline
    extra = 1
    fields = ('text', 'order', 'is_active', 'is_delete')


class HeroInfoChipInline(admin.TabularInline):
    model = m.HeroInfoChip
    extra = 1
    fields = ('icon', 'text', 'order', 'is_active', 'is_delete')


@admin.register(m.HeroSection)
class HeroSectionAdmin(SingletonAdmin):
    show_in_website_group = True
    inlines = [HeroTaglineInline, HeroInfoChipInline]
    fieldsets = (
        ('Visibility', {'fields': ('is_active', 'menu_anchor')}),
        ('Pill tag', {'fields': ('pill_text', 'pill_show_dot')}),
        ('Heading', {'fields': ('heading_pre', 'heading_highlight', 'heading_post')}),
        ('Countdown', {'fields': ('show_countdown', 'edition_label', 'event_datetime', 'countdown_ended_text')}),
        ('Buttons', {'fields': ('show_primary_button', 'primary_button_text', 'primary_button_link',
                                'show_secondary_button', 'secondary_button_text', 'secondary_button_link')}),
        ('Background', {'fields': ('background_image', 'overlay_text')}),
    )


class AboutStatInline(admin.TabularInline):
    model = m.AboutStat
    extra = 1
    fields = ('icon', 'number', 'label', 'order', 'is_active', 'is_delete')


@admin.register(m.AboutSection)
class AboutSectionAdmin(SingletonAdmin):
    show_in_website_group = True
    inlines = [AboutStatInline]
    fieldsets = (
        ('Visibility', {'fields': ('is_active', 'menu_anchor')}),
        ('Content', {'fields': ('pill_text', 'heading', 'description')}),
        ('Photo & badge', {'fields': ('image', 'show_badge', 'badge_icon', 'badge_title', 'badge_year')}),
        ('Button', {'fields': ('show_button', 'button_text', 'button_link')}),
    )


class TopicCardInline(admin.StackedInline):
    model = m.TopicCard
    extra = 1
    fields = ('title', 'description', 'icon_image', 'image', 'order', 'is_active', 'is_featured', 'is_delete')


@admin.register(m.TopicsSection)
class TopicsSectionAdmin(SingletonAdmin):
    show_in_website_group = True
    inlines = [TopicCardInline]
    fieldsets = (
        ('Visibility', {'fields': ('is_active', 'menu_anchor')}),
        ('Heading', {'fields': ('eyebrow', 'heading_pre', 'heading_highlight', 'subtext')}),
    )


class TakeawayCardForm(forms.ModelForm):
    class Meta:
        model = m.TakeawayCard
        fields = '__all__'
        widgets = {
            'accent_color': forms.TextInput(attrs={'type': 'color'}),
            'bullet_color': forms.TextInput(attrs={'type': 'color'}),
            'bullets': forms.Textarea(attrs={'rows': 6}),
        }


class TakeawayCardInline(admin.StackedInline):
    model = m.TakeawayCard
    form = TakeawayCardForm
    extra = 1
    fields = ('icon', 'title', 'track_label', 'values_label', 'bullets', 'link_text', 'link_url',
              'accent_color', 'bullet_color', 'order', 'is_active', 'is_featured', 'is_delete')


@admin.register(m.TakeawaysSection)
class TakeawaysSectionAdmin(SingletonAdmin):
    show_in_website_group = True
    inlines = [TakeawayCardInline]
    fieldsets = (
        ('Visibility', {'fields': ('is_active', 'menu_anchor')}),
        ('Heading', {'fields': ('pill_text', 'pill_show_dot', 'heading', 'subtext')}),
        ('Top-right link', {'fields': ('show_link', 'link_text', 'link_url')}),
    )


class GainCardInline(admin.StackedInline):
    model = m.GainCard
    extra = 1
    fields = ('icon', 'title', 'description', 'order', 'is_active', 'is_featured', 'is_delete')


@admin.register(m.GainSection)
class GainSectionAdmin(SingletonAdmin):
    show_in_website_group = True
    inlines = [GainCardInline]
    fieldsets = (
        ('Visibility', {'fields': ('is_active', 'menu_anchor')}),
        ('Heading', {'fields': ('pill_text', 'pill_show_dot', 'heading')}),
        ('Video box', {'fields': ('show_video', 'video_thumbnail', 'video_url', 'video_caption')}),
    )


class CommitteeInline(admin.StackedInline):
    model = m.Committee
    extra = 0
    fields = ('title', 'pill_text', 'pill_show_dot', 'background_image', 'order', 'is_active', 'is_delete')


@admin.register(m.CommitteeSection)
class CommitteeSectionAdmin(SingletonAdmin):
    show_in_website_group = True
    inlines = [CommitteeInline]
    fieldsets = (
        ('Visibility', {'fields': ('is_active', 'menu_anchor')}),
    )


class CommitteeRoleInline(admin.TabularInline):
    model = m.CommitteeRole
    extra = 1
    fields = ('committee', 'role', 'order', 'is_active')


@admin.register(m.CommitteeMember)
class CommitteeMemberAdmin(admin.ModelAdmin):
    inlines = [CommitteeRoleInline]
    list_display = ('thumb', 'name', 'designation', 'committees', 'is_active', 'is_featured', 'is_delete')
    list_display_links = ('thumb', 'name')
    list_filter = ('is_active', 'is_featured', 'is_delete', 'roles__committee')
    search_fields = ('name', 'designation', 'roles__role')
    list_per_page = 30
    fields = ('name', 'designation', 'photo', 'is_active', 'is_featured', 'is_delete')

    @admin.display(description='Photo')
    def thumb(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width:40px;height:40px;border-radius:50%;object-fit:cover">',
                               obj.photo.url)
        return '-'

    @admin.display(description='Committees')
    def committees(self, obj):
        return ', '.join(sorted({r.committee.title for r in obj.roles.all()}))

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('roles__committee').distinct()


class StatsSectionForm(forms.ModelForm):
    class Meta:
        model = m.StatsSection
        fields = '__all__'
        widgets = {'hover_color': forms.TextInput(attrs={'type': 'color'})}


class StatItemInline(admin.StackedInline):
    model = m.StatItem
    extra = 1
    fields = ('number', 'suffix', 'label', 'description', 'order', 'is_active', 'is_featured', 'is_delete')


@admin.register(m.StatsSection)
class StatsSectionAdmin(SingletonAdmin):
    show_in_website_group = True
    form = StatsSectionForm
    inlines = [StatItemInline]
    fieldsets = (
        ('Visibility', {'fields': ('is_active', 'menu_anchor')}),
        ('Look', {'fields': ('background_image', 'hover_color')}),
    )


class SponsorPackageInline(admin.StackedInline):
    model = m.SponsorPackage
    extra = 1
    fields = ('tier_label', 'title', 'currency_symbol', 'price', 'price_unit', 'description', 'benefits',
              'button_text', 'button_link', 'order', 'is_active', 'is_featured', 'is_delete')


@admin.register(m.SponsorshipSection)
class SponsorshipSectionAdmin(SingletonAdmin):
    show_in_website_group = True
    inlines = [SponsorPackageInline]
    fieldsets = (
        ('Visibility', {'fields': ('is_active', 'menu_anchor')}),
        ('Heading', {'fields': ('pill_icon', 'pill_text', 'heading', 'subtext')}),
        ('Top-right tagline', {'fields': ('show_tagline', 'tagline_words')}),
        ('Background', {'fields': ('background_image',)}),
    )


class MatrixTierInline(admin.TabularInline):
    model = m.MatrixTier
    extra = 0
    fields = ('name', 'price', 'is_highlighted', 'order', 'is_active', 'is_delete')


class MatrixCategoryInline(admin.TabularInline):
    model = m.MatrixCategory
    extra = 0
    fields = ('title', 'order', 'is_active', 'is_delete')


@admin.register(m.MatrixSection)
class MatrixSectionAdmin(SingletonAdmin):
    show_in_website_group = True
    inlines = [MatrixTierInline, MatrixCategoryInline]
    fieldsets = (
        ('Visibility', {'fields': ('is_active', 'menu_anchor')}),
        ('Title bar', {'fields': ('title', 'note', 'first_column_title')}),
    )


class MatrixCellInline(admin.TabularInline):
    model = m.MatrixCell
    extra = 0
    fields = ('tier', 'style', 'text', 'subtext')


@admin.register(m.MatrixRow)
class MatrixRowAdmin(admin.ModelAdmin):
    inlines = [MatrixCellInline]
    list_display = ('label', 'category', 'order', 'is_active', 'is_delete')
    list_filter = ('category', 'is_active', 'is_delete')
    search_fields = ('label',)
    fields = ('category', 'label', 'order', 'is_active', 'is_delete')


class BoothSpaceForm(forms.ModelForm):
    class Meta:
        model = m.BoothSpace
        fields = '__all__'
        widgets = {
            'tint_color': forms.TextInput(attrs={'type': 'color'}),
            'accent_color': forms.TextInput(attrs={'type': 'color'}),
        }


class BoothSpaceInline(admin.StackedInline):
    model = m.BoothSpace
    form = BoothSpaceForm
    extra = 1
    fields = ('icon', 'size_label', 'grid_label', 'space_type', 'dimensions', 'category', 'name',
              'price_label', 'currency_symbol', 'price', 'gst_note', 'button_text', 'button_link',
              'button_style', 'tint_color', 'accent_color', 'flagship_tag',
              'order', 'is_active', 'is_featured', 'is_delete')


@admin.register(m.ExpositionSection)
class ExpositionSectionAdmin(SingletonAdmin):
    show_in_website_group = True
    inlines = [BoothSpaceInline]
    fieldsets = (
        ('Visibility', {'fields': ('is_active', 'menu_anchor')}),
        ('Heading', {'fields': ('pill_text', 'heading', 'subtext')}),
        ('Top-right button', {'fields': ('show_top_button', 'top_button_text', 'top_button_link')}),
        ('Venue card', {'fields': ('venue_image', 'venue_tag', 'venue_title', 'venue_subtext')}),
        ('Pass entitlements', {'fields': ('show_pass_box', 'pass_title', 'pass_tag', 'pass_count',
                                          'pass_headline', 'pass_subline', 'pass_includes', 'pass_excludes',
                                          'gst_footnote', 'footer_link_text', 'footer_link_url')}),
    )


class SpecialSponsorCardForm(forms.ModelForm):
    class Meta:
        model = m.SpecialSponsorCard
        fields = '__all__'
        widgets = {
            'strip_color': forms.TextInput(attrs={'type': 'color'}),
            'deliverables': forms.Textarea(attrs={'rows': 4}),
        }


class SpecialSponsorCardInline(admin.StackedInline):
    model = m.SpecialSponsorCard
    form = SpecialSponsorCardForm
    extra = 1
    fields = ('strip_text', 'strip_color', 'exclusive_tag', 'slot_tag', 'is_highlighted', 'name', 'description',
              'price_label', 'currency_symbol', 'price', 'price_note_prefix', 'deliverables_label', 'deliverables',
              'passes_label', 'passes_value', 'button_text', 'button_link', 'button_style',
              'order', 'is_active', 'is_featured', 'is_delete')


@admin.register(m.SpecialSponsorSection)
class SpecialSponsorSectionAdmin(SingletonAdmin):
    show_in_website_group = True
    inlines = [SpecialSponsorCardInline]
    fieldsets = (
        ('Visibility', {'fields': ('is_active', 'menu_anchor')}),
        ('Heading', {'fields': ('pill_text', 'heading', 'subtext')}),
        ('Top-right tag', {'fields': ('show_tag', 'tag_text')}),
    )


class MeetingRoomDetailInline(admin.TabularInline):
    model = m.MeetingRoomDetail
    extra = 1
    fields = ('icon', 'label', 'text', 'order', 'is_active', 'is_delete')


class MeetingRoomFeatureInline(admin.StackedInline):
    model = m.MeetingRoomFeature
    extra = 1
    fields = ('icon', 'title', 'description', 'order', 'is_active', 'is_featured', 'is_delete')


@admin.register(m.MeetingRoomSection)
class MeetingRoomSectionAdmin(SingletonAdmin):
    show_in_website_group = True
    inlines = [MeetingRoomDetailInline, MeetingRoomFeatureInline]
    fieldsets = (
        ('Visibility', {'fields': ('is_active', 'menu_anchor')}),
        ('Left card', {'fields': ('pill_text', 'title', 'currency_label', 'price', 'price_unit', 'gst_note')}),
        ('Button', {'fields': ('button_text', 'button_link')}),
    )


class TechHiveDeliverableInline(admin.TabularInline):
    model = m.TechHiveDeliverable
    extra = 1
    fields = ('icon', 'title', 'subline', 'order', 'is_active', 'is_delete')


class DelegateRateInline(admin.TabularInline):
    model = m.DelegateRate
    extra = 1
    fields = ('category', 'description', 'note', 'early_price', 'standard_price',
              'order', 'is_active', 'is_featured', 'is_delete')


@admin.register(m.TechHiveSection)
class TechHiveSectionAdmin(SingletonAdmin):
    show_in_website_group = True
    inlines = [TechHiveDeliverableInline, DelegateRateInline]
    fieldsets = (
        ('Visibility', {'fields': ('is_active', 'menu_anchor')}),
        ('Heading', {'fields': ('pill_text', 'heading', 'subtext', 'show_top_button',
                                'top_button_text', 'top_button_link')}),
        ('TechHive panel', {'fields': ('show_panel', 'panel_tag1', 'panel_tag2', 'panel_title',
                                       'panel_description', 'deliverables_label',
                                       'apply_button_text', 'apply_button_link')}),
        ('Fee box', {'fields': ('fee_label', 'fee_tag', 'fee_currency', 'fee_price', 'fee_unit',
                                'fee_gst_note')}),
        ('Delegate investment matrix', {'fields': (
            'show_delegate_matrix', 'matrix_title', 'matrix_subtitle', 'matrix_badge',
            'category_column_title', 'category_column_note', 'early_column_title', 'early_column_note',
            'standard_column_title', 'standard_column_note', 'matrix_gst_note',
            'matrix_button_text', 'matrix_button_link')}),
    )


class GalleryImageInline(admin.TabularInline):
    model = m.GalleryImage
    extra = 1
    fields = ('image', 'caption', 'order', 'is_active', 'is_featured', 'is_delete')


@admin.register(m.GallerySection)
class GallerySectionAdmin(SingletonAdmin):
    show_in_website_group = True
    inlines = [GalleryImageInline]
    fieldsets = (
        ('Visibility', {'fields': ('is_active', 'menu_anchor')}),
        ('Heading', {'fields': ('pill_text', 'heading', 'subtext')}),
    )


class PartnerLogoInline(admin.TabularInline):
    model = m.PartnerLogo
    extra = 1
    fields = ('name', 'logo', 'website', 'order', 'is_active', 'is_delete')


@admin.register(m.PartnersSection)
class PartnersSectionAdmin(SingletonAdmin):
    show_in_website_group = True
    inlines = [PartnerLogoInline]
    fieldsets = (
        ('Visibility', {'fields': ('is_active', 'menu_anchor')}),
        ('Heading', {'fields': ('pill_text', 'heading')}),
        ('Carousel', {'fields': ('autoplay', 'speed_seconds', 'show_arrows')}),
    )


class BannerItemInline(admin.TabularInline):
    model = m.BannerItem
    extra = 1
    fields = ('icon', 'text', 'order', 'is_active', 'is_delete')


class BannerInfoInline(admin.TabularInline):
    model = m.BannerInfo
    extra = 1
    fields = ('icon', 'label', 'value', 'order', 'is_active', 'is_delete')


@admin.register(m.BannerSection)
class BannerSectionAdmin(SingletonAdmin):
    show_in_website_group = True
    inlines = [BannerItemInline, BannerInfoInline]
    fieldsets = (
        ('Visibility', {'fields': ('is_active', 'menu_anchor')}),
        ('Background', {'fields': ('background_image',)}),
        ('Content', {'fields': ('pill_text', 'heading_line1', 'heading_line2', 'description')}),
        ('Button', {'fields': ('button_text', 'button_link')}),
    )


class ContactPersonForm(forms.ModelForm):
    class Meta:
        model = m.ContactPerson
        fields = '__all__'
        widgets = {
            'phones': forms.Textarea(attrs={'rows': 3}),
            'emails': forms.Textarea(attrs={'rows': 3}),
        }


class ContactPersonInline(admin.StackedInline):
    model = m.ContactPerson
    form = ContactPersonForm
    extra = 1
    fields = ('tag', 'name', 'role', 'phones', 'emails', 'order', 'is_active', 'is_featured', 'is_delete')


class ContactQRInline(admin.StackedInline):
    model = m.ContactQR
    extra = 0
    fields = ('label', 'image', 'link', 'order', 'is_active', 'is_delete')
    verbose_name_plural = 'QR codes (shown side by side in the QR card)'


@admin.register(m.ContactSection)
class ContactSectionAdmin(SingletonAdmin):
    show_in_website_group = True
    inlines = [ContactPersonInline, ContactQRInline]
    fieldsets = (
        ('Visibility', {'fields': ('is_active', 'menu_anchor')}),
        ('Heading', {'fields': ('eyebrow', 'heading', 'side_text')}),
        ('QR card', {'fields': ('show_qr', 'qr_pill_text', 'qr_title', 'qr_subtext', 'qr_image', 'qr_background_image', 'qr_caption')}),
        ('Bottom strip', {'fields': ('show_strip', 'strip_label', 'strip_link_text', 'strip_link_url')}),
    )


class ContactLinesForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        widgets = {
            'phones': forms.Textarea(attrs={'rows': 2}),
            'emails': forms.Textarea(attrs={'rows': 2}),
        }


class CoordinatorForm(ContactLinesForm):
    class Meta(ContactLinesForm.Meta):
        model = m.Coordinator


class DeskCardForm(ContactLinesForm):
    class Meta(ContactLinesForm.Meta):
        model = m.DeskCard


class CoordinatorInline(admin.StackedInline):
    model = m.Coordinator
    form = CoordinatorForm
    extra = 1
    fields = ('name', 'phones', 'emails', 'order', 'is_active', 'is_delete')


class DeskCardInline(admin.StackedInline):
    model = m.DeskCard
    form = DeskCardForm
    extra = 1
    fields = ('tag', 'name', 'phones', 'emails', 'order', 'is_active', 'is_delete')


@admin.register(m.CoordinatorsSection)
class CoordinatorsSectionAdmin(SingletonAdmin):
    show_in_website_group = True
    inlines = [CoordinatorInline, DeskCardInline]
    fieldsets = (
        ('Visibility', {'fields': ('is_active', 'menu_anchor')}),
        ('Heading', {'fields': ('eyebrow', 'heading', 'side_text', 'desk_background_image')}),
    )


class FooterSocialInline(admin.TabularInline):
    model = m.FooterSocial
    extra = 1
    fields = ('platform', 'url', 'order', 'is_active', 'is_delete')


class FooterLinkInline(admin.TabularInline):
    model = m.FooterLink
    extra = 1
    fields = ('label', 'link', 'is_highlighted', 'open_in_new_tab', 'use_register_dropdown', 'order', 'is_active', 'is_delete')


class FooterLegalLinkInline(admin.TabularInline):
    model = m.FooterLegalLink
    extra = 1
    fields = ('label', 'link', 'open_in_new_tab', 'order', 'is_active', 'is_delete')


@admin.register(m.FooterSection)
class FooterSectionAdmin(SingletonAdmin):
    show_in_website_group = True
    inlines = [FooterSocialInline, FooterLinkInline, FooterLegalLinkInline]
    fieldsets = (
        ('Visibility', {'fields': ('is_active',)}),
        ('Brand', {'fields': ('tagline',), 'description': 'The footer uses the same logo as the header (Header & Menu).'}),
        ('Website pill', {'fields': ('show_website_pill', 'website_text', 'website_url')}),
        ('Bottom bar', {'fields': ('copyright_text',)}),
    )


@admin.register(m.Credits)
class CreditsAdmin(SingletonAdmin):
    fieldsets = (
        ('Credits line (shown in the footer)', {'fields': ('is_active', 'text', 'url', 'open_in_new_tab')}),
    )


@admin.register(m.FloatingButtons)
class FloatingButtonsAdmin(SingletonAdmin):
    show_in_website_group = True
    fieldsets = (
        ('Visibility', {'fields': ('is_active',)}),
        ('WhatsApp button', {'fields': ('show_whatsapp', 'whatsapp_number', 'whatsapp_message')}),
        ('Call button', {'fields': ('show_call', 'call_number')}),
    )


class LegalPageForm(forms.ModelForm):
    class Meta:
        model = m.LegalPage
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={'rows': 24}),
            'subtitle': forms.Textarea(attrs={'rows': 3}),
        }


@admin.register(m.LegalPage)
class LegalPageAdmin(admin.ModelAdmin):
    form = LegalPageForm
    list_display = ('title', 'slug', 'order', 'is_active', 'is_delete')
    list_filter = ('is_active', 'is_delete')
    search_fields = ('title', 'content')
    fields = ('title', 'slug', 'subtitle', 'content', 'order', 'is_active', 'is_delete')


@admin.register(m.SEOSettings)
class SEOSettingsAdmin(SingletonAdmin):
    fieldsets = (
        ('Page title & meta description', {'fields': ('meta_title', 'meta_description', 'meta_keywords', 'og_image')}),
    )


class EmailSettingsForm(forms.ModelForm):
    class Meta:
        model = m.EmailSettings
        fields = '__all__'
        widgets = {'smtp_password': forms.PasswordInput(render_value=True)}


@admin.register(m.EmailSettings)
class EmailSettingsAdmin(SingletonAdmin):
    form = EmailSettingsForm
    fieldsets = (
        ('Status', {'fields': ('is_active',)}),
        ('SMTP server', {'fields': ('smtp_host', 'smtp_port', 'use_tls', 'use_ssl')}),
        ('Login', {'fields': ('smtp_username', 'smtp_password')}),
        ('Sender & recipients', {'fields': ('sender_name', 'from_email', 'notification_emails', 'subject_prefix')}),
    )
