__version__ = '0.1.0'
from easy_thumbnails.alias import aliases
if not aliases.get('thumb'):
    aliases.set('thumb', {'size': (100, 70), 'crop': True})