===============================
Django Twitter photostream api
===============================

.. image:: https://badge.fury.io/py/django-twitter-photo-api.svg
    :target: https://badge.fury.io/py/django-twitter-photo-api

.. image:: https://travis-ci.org/SoftFormance/django-twitter-photo-api.svg?branch=master
    :target: https://travis-ci.org/SoftFormance/django-twitter-photo-api

.. image:: https://codecov.io/gh/SoftFormance/django-twitter-photo-api/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/SoftFormance/django-twitter-photo-api

Get photos from Twitter by hashtags

Documentation
-------------

The full documentation is at https://django-twitter-photo-api.readthedocs.io.

Quickstart
----------

Install Django Twitter photostream api::

    pip install django-twitter-photo-api

Install Django Twitter photo api from GitHub::

    virtualenv photostream
    source photostream/bin/activate
    pip install -e git+https://github.com/softformance/django-twitter-photo-api.git#egg=django-twitter-photo-api

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_twitter_photo_api',
        ...
    )

Add Django Twitter photostream api's URL patterns:

.. code-block:: python

    from django_twitter_photo_api import urls as django_twitter_photo_api_urls


    urlpatterns = [
        ...
        url(r'^twitter_app/', include(django_twitter_photo_api_urls, 
            namespace="twitter-feed")),
        ...
    ]

- Create at `Twitter Developer <https://dev.twitter.com/>`_ new application.
- Add into Django admin ``Twitter applications`` model your ``consumer key``, ``consumer secret``, ``access token``, ``access token secret``.
- Add a hashtag to your ``Hashtags`` model.
- Sync your posts :)

Features
--------

* Retrieve from Twitter photos by hashtag.
* Sync added hashtags, add a post by URL and add a post manually.
* Get photos from your backend server by simple URL.

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
