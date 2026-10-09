"""
Django settings for the SAE India project.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

try:
    import MySQLdb  # noqa: F401  (mysqlclient, used locally when installed)
except ImportError:  # production: pure-python driver, nothing to compile
    import pymysql
    pymysql.version_info = (2, 2, 1, 'final', 0)
    pymysql.install_as_MySQLdb()

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dev-only')

DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') if h.strip()]

# Railway gives the public domain in RAILWAY_PUBLIC_DOMAIN
_railway_domain = os.getenv('RAILWAY_PUBLIC_DOMAIN', '').strip()
if _railway_domain:
    ALLOWED_HOSTS.append(_railway_domain)

CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',') if o.strip()]
if _railway_domain:
    CSRF_TRUSTED_ORIGINS.append('https://' + _railway_domain)

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# Application definition

INSTALLED_APPS = [
    'jazzmin',  # must come before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',  # the single app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'saeindia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # templates live in core/templates/core/
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'saeindia.wsgi.application'


# Database (MySQL)

def _env(*names, default=''):
    for n in names:
        v = os.getenv(n)
        if v:
            return v
    return default


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': _env('DB_NAME', 'MYSQLDATABASE', default='sae_india_db'),
        'USER': _env('DB_USER', 'MYSQLUSER', default='root'),
        'PASSWORD': _env('DB_PASSWORD', 'MYSQLPASSWORD'),
        'HOST': _env('DB_HOST', 'MYSQLHOST', default='localhost'),
        'PORT': _env('DB_PORT', 'MYSQLPORT', default='3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True


# Static & media files

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage'},
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Email: the real SMTP values are stored in the admin (Header & Menu > Email Settings)
# and applied at send time. This is only the fallback.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# Jazzmin admin

JAZZMIN_SETTINGS = {
    'site_title': 'SAE India Admin',
    'site_header': 'SAE India',
    'site_brand': 'SAE India',
    'welcome_sign': 'Welcome to SAE India Admin',
    'copyright': 'SAE India',
    'show_ui_builder': False,
    'custom_css': 'core/css/admin.css',
    'changeform_format': 'horizontal_tabs',
    'related_modal_active': True,
    'custom_links': {
        'auth': [
            {'name': 'SEO', 'url': 'admin:core_seosettings_changelist',
             'icon': 'fas fa-search', 'permissions': ['core.change_seosettings']},
            {'name': 'Email Settings', 'url': 'admin:core_emailsettings_changelist',
             'icon': 'fas fa-envelope', 'permissions': ['core.change_emailsettings']},
            {'name': 'Credits', 'url': 'admin:core_credits_changelist',
             'icon': 'fas fa-copyright', 'permissions': ['core.change_credits']},
        ],
    },
    'order_with_respect_to': [
        'core.headersettings', 'core.herosection', 'core.aboutsection', 'core.topicssection',
        'core.takeawayssection', 'core.gainsection', 'core.committeesection', 'core.committeemember',
        'core.statssection', 'core.sponsorshipsection', 'core.matrixsection', 'core.matrixrow',
        'core.expositionsection', 'core.specialsponsorsection', 'core.techhivesection',
        'core.meetingroomsection', 'core.gallerysection', 'core.partnerssection',
        'core.floatingbuttons', 'core.legalpage',
        'core.bannersection', 'core.contactsection',
        'core.coordinatorssection', 'core.footersection',
    ],
    'icons': {
        'auth': 'fas fa-users-cog',
        'auth.user': 'fas fa-user',
        'auth.Group': 'fas fa-users',
        'core': 'fas fa-globe',
        'core.headersettings': 'fas fa-bars',
        'core.herosection': 'fas fa-star',
        'core.aboutsection': 'fas fa-info-circle',
        'core.topicssection': 'fas fa-lightbulb',
        'core.takeawayssection': 'fas fa-bullseye',
        'core.gainsection': 'fas fa-gift',
        'core.statssection': 'fas fa-chart-line',
        'core.sponsorshipsection': 'fas fa-handshake',
        'core.expositionsection': 'fas fa-store',
        'core.specialsponsorsection': 'fas fa-glass-cheers',
        'core.meetingroomsection': 'fas fa-door-open',
        'core.techhivesection': 'fas fa-rocket',
        'core.gallerysection': 'fas fa-images',
        'core.partnerssection': 'fas fa-handshake',
        'core.bannersection': 'fas fa-bullhorn',
        'core.floatingbuttons': 'fas fa-comment-dots',
        'core.legalpage': 'fas fa-file-contract',
        'core.contactsection': 'fas fa-address-book',
        'core.coordinatorssection': 'fas fa-headset',
        'core.footersection': 'fas fa-shoe-prints',
        'core.matrixsection': 'fas fa-table',
        'core.matrixrow': 'fas fa-grip-lines',
        'core.committeesection': 'fas fa-sitemap',
        'core.committeemember': 'fas fa-user-tie',
    },
}

JAZZMIN_UI_TWEAKS = {
    'navbar': 'navbar-dark',
    'navbar_fixed': True,
    'sidebar_fixed': True,
    'brand_colour': 'navbar-teal',
    'accent': 'accent-teal',
    'sidebar': 'sidebar-dark-teal',
    'button_classes': {
        'primary': 'btn-primary',
        'secondary': 'btn-secondary',
        'info': 'btn-info',
        'warning': 'btn-warning',
        'danger': 'btn-danger',
        'success': 'btn-success',
    },
}
