import os
import logging
import requests
from datetime import datetime
import tweepy

from django.core.files.base import ContentFile
from .models import Post, Hashtag
from .models import TwitterApp

logger = logging.getLogger('default')


def invalid_token_handler():
    message = "Your token has expired or invalid."
    mail_admins('Instagram Application', message, fail_silently=True)


def get_redirect_uri(request, app_id):
    host = request.get_host()
    prefix = 'https' if request.is_secure() else 'http'
    return 'null string'


def get_medias_by_tag(tag, access_token):
    url = '%s/v1/tags/%s/media/recent?access_token=%s&count=%s' % (
        IG_URL, tag, access_token, count)
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.json()
        else:
            if resp.status_code == 400:
                invalid_token_handler()
            resp = resp.json()
            message = resp['meta'].get('error_message')
            logger.exception(message)
            raise Exception(message)
    except Exception as e:
        message = "Error while fetching medias_by_tag: %s" % e
        logger.exception(message)
        raise JsonException(message)


def get_media_by_code(id_status, id_application):
    try:
        api = api_authed_tweepy(id_application)
        media_object = api.get_status(int(id_status))
        return None, media_object
    except:
        error = "Error while fetching."
        logger.exception(error)
        return error, None


def save_post(app_id, media, is_show):
    media_id = media.entities['media'][0]['id_str']
    link = media.entities['media'][0]['url']
    caption = media.text
    media_url = media.entities['media'][0]['media_url']
    created_at = media.created_at
    username = media.user.screen_name

    post, created = Post.objects.get_or_create(
        media_id=media_id, application_id=app_id,
        defaults={
            'link': link,
            'username': username,
            'caption': caption,
            'created_at': created_at,
            'show': is_show
        }
    )

    if created:
        # save image
        photo_content = ContentFile(requests.get(media_url).content)
        post.photo.save(os.path.basename(media_url), photo_content)
        # save tags
        app_hashtags = Hashtag.objects.filter(application_id=app_id).iterator()
        hashtags_list = [tag for tag in app_hashtags for hashtag in media.entities['hashtags'] if tag.name == hashtag['text'].lower()]
        for hashtag in hashtags_list:
            post.hashtags.add(hashtag)
        if hashtags_list:
            post.save()
    return post


def get_media_by_url(application, url):
    if url[-1] == '/':
        url = url[:len(url)-1]
    id_status = int(url.split('/')[-1])
    return get_media_by_code(id_status, application.id)


def sync_by_tag(app_id, tag, is_show, api):
    query = '%23' + tag + ' filter:media'
    print(api)
    result_query = api.search(q=query)
    print(result_query)

    if result_query:
        for media in result_query:
            if media and media.entities.get('media'):
                save_post(app_id, media, is_show)

def api_authed_tweepy(app_id):
    try:
        app = TwitterApp.objects.get(id=app_id)
        is_show = app.hashtag_is_show
        oauth_data = {}
        oauth_data['consumer_key'] = app.consumer_key
        oauth_data['consumer_secret'] = app.consumer_secret
        oauth_data['access_token'] = app.access_token
        oauth_data['access_token_secret'] = app.access_token_secret
    except:
        message = "Cannot get application."
        logger.exception(message)
        return None

    try:
        auth = tweepy.OAuthHandler(oauth_data['consumer_key'], 
            oauth_data['consumer_secret'])
        auth.set_access_token(oauth_data['access_token'], 
            oauth_data['access_token_secret'])
        api = tweepy.API(auth)
        return api
    except:
        message = "Cannot auth. Verify your keys, tokens."
        logger.exception(message)
        return None