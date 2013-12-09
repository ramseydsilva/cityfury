from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'cityfury.views.home', name='home'),
    url(r'^about/$', 'cityfury.views.about', name='about'),
    url(r'^support/$', 'cityfury.views.support', name='support'),
    url(r'^contact/$', 'cityfury.views.contact', name='contact'),

    url(r'^logout/$', 'cityfury.user_views.logout_view', name='logout'),
    url(r'^login/$', 'cityfury.user_views.login_view', name='login'),
    url(r'^register/$', 'cityfury.user_views.register_view', name='register'),
    url(r'^get_login_buttons/$', 'cityfury.user_views.get_login_buttons', name='get_login_buttons'),

    url(r'^get_posts/$', 'cityfury.post_views.get_posts', name="get_posts"),
    url(r'^posts/$', 'cityfury.post_views.posts', name='posts'),
    url(r'^posts/dislike/$', 'cityfury.post_views.dislike', name='dislike'),
    url(r'^posts/resolve/$', 'cityfury.post_views.resolve', name='resolve'),
    url(r'^posts/(?P<post_id>[-\d]+)/$', 'cityfury.post_views.post', name='post'),
    url(r'^posts/(?P<category>[-\w]+)/$', 'cityfury.post_views.category', name='category'),
    url(r'^posts/(?P<category>[-\w]+)/(?P<city>[-\w]+)/$', 'cityfury.post_views.city', name='city'),
    url(r'^post/$', 'cityfury.form_views.post', name='post_form'),

    url(r'^cities/data/$', 'cityfury.form_views.cities_data', name='cities_data'),
    url(r'^areas/data/$', 'cityfury.form_views.areas_data', name='areas_data'),
    url(r'^post/flag/(?P<post_id>[-\d]+)/$', 'cityfury.post_views.flag', name='flag-post'),

    url(r'^contact/(?P<contact_id>[-\d]+)/$', 'cityfury.contact_views.contact', name='contact'),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
