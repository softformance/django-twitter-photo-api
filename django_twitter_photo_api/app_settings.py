from django.conf import settings

#Insert here your settings const.
TW_URL = getattr(settings, 'TW_URL', 'example')

REDIRECT_URI_SUFIX = getattr(settings, 'REDIRECT_URI_SUFIX', 'instagram_app/access_token/token')

GET_MEDIAS_COUNT = getattr(settings, 'GET_MEDIAS_COUNT', 10)