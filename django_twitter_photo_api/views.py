import logging
import requests
import tweepy 

from .models import TwitterApp, Hashtag, Post
from .utils import get_redirect_uri, sync_by_tag
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
# from django.core import serializers
from django.contrib.auth.decorators import login_required

logger = logging.getLogger('default')


@login_required()
def access_token(request):
    return NotImplementedError


@login_required()
def access_token_authorize(request, app_id=1):
    return NotImplementedError


@login_required()
def sync_by_app(request, app_id=None):

    if not app_id:
        app_id = request.POST['app_id']
    if not app_id:
        return

    try:
        app = TwitterApp.objects.get(id=app_id)
        is_show = app.hashtag_is_show
        oauth_data = {}
        oauth_data['consumer_key'] = app.consumer_key
        oauth_data['consumer_secret'] = app.consumer_secret
        oauth_data['access_token'] = app.access_token
        oauth_data['access_token_secret'] = app.access_token_secret
    except:
        message = "Tried to sync undefined app"
        logger.exception(message)
        return []

    try:
        auth = tweepy.OAuthHandler(oauth_data['consumer_key'], 
            oauth_data['consumer_secret'])
        auth.set_access_token(oauth_data['access_token'], 
            oauth_data['access_token_secret'])
        api = tweepy.API(auth)
    except:
        message = "Cannot oauth to twitter api. Verify your data(key, token) \
         in Django admin."
        logger.exception(message)
        return []

    tags = Hashtag.objects.filter(application_id=app_id)
    for tag in tags:
        sync_by_tag(app_id, tag.name, is_show, api)

    return redirect(reverse('admin:%s_%s_changelist' % (
        app._meta.app_label, 'post')))


def get_posts(request, app_id):
    order_by_param = ('?', 'created_at')
    try:
        app = TwitterApp.objects.get(id=app_id)
    except:
        return []

    #count
    try:
        count = int(request.GET.get('count'))
    except:
        count = app.hashtag_count

    #order_by
    if request.GET.get('order_by') in order_by_param:
        order_by = request.GET.get('order_by')
    else:
        order_by = app.hashtag_sort_by

    params = {'application_id': app_id}
    tags = request.GET.getlist('tags')
    if tags:
        params['hashtags__name__in'] = tags

    posts = Post.objects.filter(**params)\
        .filter(show=True) \
        .order_by(order_by) \
        .values('media_id', 'photo', 'link', 'caption')[:count]

    return JsonResponse(list(posts), safe=False)
