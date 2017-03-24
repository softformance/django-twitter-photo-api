# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from easy_thumbnails.fields import ThumbnailerImageField


@python_2_unicode_compatible
class TwitterApp(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Application Name'))
    consumer_key = models.CharField(
        max_length=50, verbose_name=_('Twitter App consumer key'))
    consumer_secret = models.CharField(
        max_length=50, verbose_name=_('Twitter App consumer secret'))
    is_auto_access_token = models.BooleanField(
        verbose_name=_('Get access token automatically'), default=True)
    access_token = models.CharField(
        max_length=100, verbose_name=_('Access token'),
        null=True, blank=True)
    access_token_secret = models.CharField(
        max_length=50, verbose_name=_('Access token secret'),
        null=True, blank=True)
    tag_is_show = models.BooleanField(
        verbose_name=_('Show posts'), default=False)

    class Meta:
        verbose_name = _('Twitter Application')
        verbose_name_plural = _('Twitter Applications')

    def __str__(self):
        return '%s. %s' % (self.id, self.name)


@python_2_unicode_compatible
class Hashtag(models.Model):
    application = models.ForeignKey(
        TwitterApp, related_name='app_hashtag', default=1)
    name = models.CharField(max_length=50, verbose_name=_('Hashtag name'))

    class Meta:
        verbose_name = _('Hashtag')
        verbose_name_plural = _('Hashtags')
        unique_together = (("application", "name"),) 

    def __str__(self):
        return '%s - application ID: %s' % (self.name, self.application)

    def save(self, *args, **kwargs):
        self.name = self.name.lower() 
        super(Hashtag, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Post(models.Model):
    application = models.ForeignKey(TwitterApp, related_name='app_post')
    media_id = models.CharField(_('Media ID'), max_length=100)
    photo = ThumbnailerImageField(upload_to='twitter_photos')
    link = models.URLField(_('Link'))
    hashtags = models.ManyToManyField(Hashtag)
    caption = models.TextField(
        verbose_name=_('Caption text'),
        default='', blank=True, null=True)
    username = models.CharField(
        _('Twitter username'), max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    show = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

        unique_together = (("application", "media_id"),)

    def get_thumb_url(self):
        try:
            return self.photo['thumb'].url
        except:
            return None


