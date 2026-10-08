# SAE India - APAC 23 landing page

Single landing page built with **Django 5.2**, **Django Jazzmin** admin and **MySQL**.
One Django project (`saeindia`) and one app (`core`). Every section of the page is managed from the admin.

## Setup

1. Create and activate a virtual environment, then install the dependencies:

   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   pip install -r requirements.txt
   ```

2. Create a MySQL database (utf8mb4), for example `sae_india_db`.

3. Copy `.env.example` to `.env` and fill in the database user and password and a new `SECRET_KEY`.

4. Create the tables and the pre-filled content, then a superuser:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. Run the site:

   ```bash
   python manage.py runserver
   ```

   - Website: http://localhost:8000/
   - Admin: http://localhost:8000/admin/

## Where things are

- `core/models.py`, `core/admin.py` - one admin menu per website section (under **Website**).
- `core/templates/core/` - `base.html`, `index.html` and one template per section in `sections/`.
- `core/static/core/css/main.css` - the single stylesheet. `core/static/core/js/main.js` - small scripts (menu, countdown, carousel, lightbox).
- `media/` - uploaded images (logos, photos). In production, serve these from a proper media store.
- Users menu in the admin: **SEO** (page title and meta description), **Email Settings** (Gmail SMTP) and **Credits**.

## Notes

- Fonts: Plus Jakarta Sans (and Caveat for the hero script text). Icons: Google Material Symbols.
- Brand colours: `#334155`, `#0D9488`, `#F07416`, `#CCFBF1`.
- Not built yet: the contact form and its Enquiries inbox, `robots.txt` and `sitemap.xml`.
