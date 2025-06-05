import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weatherApp.settings")
django.setup()