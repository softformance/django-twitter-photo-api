import tweepy

from django.core.management.base import BaseCommand, CommandError
from django_twitter_photo_api.models import TwitterApp, Hashtag, Post
from django_twitter_photo_api.utils import sync_by_tag, save_post

class Command(BaseCommand):
    help = 'Sync your app with hashtags by added list of id.'

    def add_arguments(self, parser):
        parser.add_argument('application_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for app_id in options['application_id']:
            try:
                app = TwitterApp.objects.get(pk=app_id)
            except TwitterApp.DoesNotExist:
                raise CommandError('Application "%s" does not exist' % poll_id)

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
                message = "Cannot oauth to twitter api. Verify your data(key, token) \
                 in Django admin."
                raise CommandError(message)

            tags = Hashtag.objects.filter(application_id=app_id)
            for tag in tags:
                sync_by_tag(app_id, tag.name, is_show, api)