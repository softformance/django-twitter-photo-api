# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-16 17:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import easy_thumbnails.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Hashtag name')),
            ],
            options={
                'verbose_name': 'Hashtag',
                'verbose_name_plural': 'Hashtags',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_id', models.CharField(max_length=100, verbose_name='Media ID')),
                ('photo', easy_thumbnails.fields.ThumbnailerImageField(height_field='photo_height', upload_to='twitter_photos', width_field='photo_width')),
                ('photo_height', models.PositiveIntegerField(default=0, editable=False)),
                ('photo_width', models.PositiveIntegerField(default=0, editable=False)),
                ('link', models.URLField(verbose_name='Link')),
                ('caption', models.TextField(blank=True, default='', null=True, verbose_name='Caption text')),
                ('username', models.CharField(blank=True, max_length=100, null=True, verbose_name='Twitter username')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('show', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
        migrations.CreateModel(
            name='TaskSheduler',
            fields=[
                ('periodictask_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_celery_beat.PeriodicTask')),
            ],
            bases=('django_celery_beat.periodictask',),
        ),
        migrations.CreateModel(
            name='TwitterApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Application Name')),
                ('consumer_key', models.CharField(max_length=50, verbose_name='Twitter App consumer key')),
                ('consumer_secret', models.CharField(max_length=50, verbose_name='Twitter App consumer secret')),
                ('access_token', models.CharField(max_length=100, verbose_name='Access token')),
                ('access_token_secret', models.CharField(max_length=50, verbose_name='Access token secret')),
                ('hashtag_is_show', models.BooleanField(default=False, verbose_name='Show posts')),
                ('hashtag_sort_by', models.CharField(choices=[('created_at', 'DATE'), ('?', 'RANDOM')], default='date', max_length=60, verbose_name='Type of sort')),
                ('hashtag_count', models.PositiveSmallIntegerField(default=6)),
            ],
            options={
                'verbose_name': 'Twitter Application',
                'verbose_name_plural': 'Twitter Applications',
            },
        ),
        migrations.AddField(
            model_name='tasksheduler',
            name='periodic_task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='periodic_task', to='django_twitter_photo_api.TwitterApp'),
        ),
        migrations.AddField(
            model_name='post',
            name='application',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='app_post', to='django_twitter_photo_api.TwitterApp'),
        ),
        migrations.AddField(
            model_name='post',
            name='hashtags',
            field=models.ManyToManyField(to='django_twitter_photo_api.Hashtag'),
        ),
        migrations.AddField(
            model_name='hashtag',
            name='application',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='app_hashtag', to='django_twitter_photo_api.TwitterApp'),
        ),
        migrations.AlterUniqueTogether(
            name='post',
            unique_together=set([('application', 'media_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='hashtag',
            unique_together=set([('application', 'name')]),
        ),
    ]
