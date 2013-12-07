from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from cityfury.form_views import PostCreateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'cityfury.views.home', name='home'),
    url(r'^upload/', include('fileupload.urls')),
    url(r'^post/$', PostCreateView.as_view(), name='post_form'),
    url(r'^cities/data/$', 'cityfury.form_views.cities_data', name='cities_data'),
    url(r'^areas/data/$', 'cityfury.form_views.areas_data', name='areas_data'),
    url(r'^post/(?P<post_id>[-\d]+)/$', 'cityfury.views.post', name='post'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<category>[-\w]+)/$', 'cityfury.views.category', name='category'),
    url(r'^(?P<category>[-\w]+)/(?P<city>[-\w]+)/$', 'cityfury.views.city', name='city'),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
