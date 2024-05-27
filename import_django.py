import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "job_scraping_server.settings")
django.setup()