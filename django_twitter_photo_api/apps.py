# -*- coding: utf-8
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoTwitterPhotoApiConfig(AppConfig):
    name = 'django_twitter_photo_api'
    verbose_name = _("Twitter photostream backend")