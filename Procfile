web: python manage.py collectstatic --noinput && python manage.py migrate --noinput && python manage.py bootstrap_site && gunicorn saeindia.wsgi --bind 0.0.0.0:$PORT --workers 2 --timeout 60
