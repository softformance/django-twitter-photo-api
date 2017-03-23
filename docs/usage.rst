=====
Usage
=====

To use Django Twitter photostream api in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_twitter_photo_api.apps.DjangoTwitterPhotoApiConfig',
        ...
    )

Add Django Twitter photostream api's URL patterns:

.. code-block:: python

    from django_twitter_photo_api import urls as django_twitter_photo_api_urls


    urlpatterns = [
        ...
        url(r'^', include(django_twitter_photo_api_urls)),
        ...
    ]
