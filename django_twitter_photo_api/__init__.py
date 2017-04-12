__version__ = '0.1.0'
default_app_config = 'django_twitter_photo_api.apps.DjangoTwitterPhotoApiConfig'
from easy_thumbnails.alias import aliases
if not aliases.get('thumb'):
    aliases.set('thumb', {'size': (100, 70), 'crop': True})