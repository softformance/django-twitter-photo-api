from __future__ import absolute_import, unicode_literals
from celery import shared_task

import tweepy
from django_twitter_photo_api.models import TwitterApp, Hashtag, Post
from django_twitter_photo_api.utils import sync_by_tag, save_post


@shared_task(name='Sync Twitter application by id')
def sync_hashtag_by_app_id(*args):
    for app_id in args:
        try:
            app = TwitterApp.objects.get(pk=app_id)
        except TwitterApp.DoesNotExist:
            print('DOESNOT EXIST')
            continue

        is_show = app.hashtag_is_show
        oauth_data = {}
        oauth_data['consumer_key'] = app.consumer_key
        oauth_data['consumer_secret'] = app.consumer_secret
        oauth_data['access_token'] = app.access_token
        oauth_data['access_token_secret'] = app.access_token_secret

        try:
            auth = tweepy.OAuthHandler(oauth_data['consumer_key'], 
                oauth_data['consumer_secret'])
            auth.set_access_token(oauth_data['access_token'], 
                oauth_data['access_token_secret'])
            api = tweepy.API(auth)
        except:
            return None

        tags = Hashtag.objects.filter(application_id=app_id)
        for tag in tags:
            sync_by_tag(app_id, tag.name, is_show, api)