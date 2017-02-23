from django.conf.urls import patterns, include, url
from django.conf import settings

# Routers provide an easy way of automatically determining the URL conf.
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

from django.views.generic import TemplateView

urlpatterns = [

    #static
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),

    #media
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),

    url(r'^demo_2/', include('demo_2.urls',
                            namespace='demo_2')),

]

