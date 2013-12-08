from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'cityfury.views.home', name='home'),

    url(r'^logout/$', 'cityfury.user_views.logout_view', name='logout'),
    url(r'^login/$', 'cityfury.user_views.login_view', name='login'),
    url(r'^register/$', 'cityfury.user_views.register_view', name='register'),
    url(r'^get_login_buttons/$', 'cityfury.user_views.get_login_buttons', name='get_login_buttons'),

    url(r'^get_posts/$', 'cityfury.post_views.get_posts', name="get_posts"),
    url(r'^post/$', 'cityfury.form_views.post', name='post_form'),
    url(r'^cities/data/$', 'cityfury.form_views.cities_data', name='cities_data'),
    url(r'^areas/data/$', 'cityfury.form_views.areas_data', name='areas_data'),
    url(r'^dislike/$', 'cityfury.post_views.dislike', name='dislike'),
    url(r'^post/flag/(?P<post_id>[-\d]+)/$', 'cityfury.post_views.flag', name='flag-post'),
    url(r'^post/(?P<post_id>[-\d]+)/$', 'cityfury.views.post', name='post'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<category>[-\w]+)/$', 'cityfury.views.category', name='category'),
    url(r'^(?P<category>[-\w]+)/(?P<city>[-\w]+)/$', 'cityfury.views.city', name='city'),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
