import os

from OmniDB import custom_settings
custom_settings.DEV_MODE = False
custom_settings.HOME_DIR = os.path.join(os.path.expanduser('~'), '.omnidb', 'omnidb-server')
custom_settings.PATH = '/omnidb/'

from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OmniDB.settings")
application = get_wsgi_application()
