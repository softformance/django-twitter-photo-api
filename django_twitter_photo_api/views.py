import logging
import requests
import tweepy 

from .models import TwitterApp, Hashtag, Post
from .utils import sync_by_tag, api_authed_tweepy
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

logger = logging.getLogger('default')

@login_required()
def sync_by_app(request, app_id=None):

    if not app_id:
        app_id = request.POST['app_id']
    if not app_id:
        return

    app = TwitterApp.objects.get(id=app_id)
    api = api_authed_tweepy(app_id)

    is_show = TwitterApp.objects.get(id=app_id).hashtag_is_show
    tags = Hashtag.objects.filter(application_id=app_id)
    for tag in tags:
        sync_by_tag(app_id, tag.name, is_show, api)

    return redirect(reverse('admin:%s_%s_changelist' % (
        app._meta.app_label, 'post')))


def get_posts(request, app_id):
    order_by_param = ('?', 'created_at')
    result_dict = {}
    result_dict['from_site'] = 'twitter'

    try:
        app = TwitterApp.objects.get(id=app_id)
    except:
        result_dict['photos'] = None
        return JsonResponse(result_dict)

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
        .values('media_id', 'photo', 'link', 'caption', 'photo_height', 
            'photo_width')[:count]


    result_dict['photos'] = list(posts)

    return JsonResponse(result_dict)
