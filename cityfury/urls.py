from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # main views
    url(r'^$', 'cityfury.views.home', name='home'),
    url(r'^about/$', 'cityfury.views.about', name='about'),
    url(r'^support/$', 'cityfury.views.support', name='support'),
    url(r'^contact/$', 'cityfury.views.contact', name='contact'),

    # user views
    url(r'^logout/$', 'cityfury.user_views.logout_view', name='logout'),
    url(r'^login/$', 'cityfury.user_views.login_view', name='login'),
    url(r'^register/$', 'cityfury.user_views.register_view', name='register'),
    url(r'^get_login_buttons/$', 'cityfury.user_views.get_login_buttons', name='get_login_buttons'),

    # post views
    url(r'^posts/get_posts/$', 'cityfury.post_views.get_posts', name="get_posts"),
    url(r'^posts/$', 'cityfury.post_views.posts', name='posts'),
    url(r'^posts/dislike/$', 'cityfury.post_views.dislike', name='dislike'),
    url(r'^posts/flag/(?P<post_id>[-\d]+)/$', 'cityfury.post_views.flag', name='flag-post'),
    url(r'^posts/(?P<post_id>[-\d]+)/$', 'cityfury.post_views.post', name='post'),
    url(r'^posts/(?P<category>[-\w]+)/$', 'cityfury.post_views.category', name='category'),
    url(r'^posts/(?P<category>[-\w]+)/(?P<city>[-\w]+)/$', 'cityfury.post_views.city', name='city'),

    # post form views
    url(r'^post/$', 'cityfury.form_views.post', name='post_form'),
    url(r'^post/cities/data/$', 'cityfury.form_views.cities_data', name='cities_data'),
    url(r'^post/areas/data/$', 'cityfury.form_views.areas_data', name='areas_data'),

    # contact views
    url(r'^contacts/resolve/$', 'cityfury.contact_views.resolve', name='resolve'),
    url(r'^contacts/correct/(?P<contact_id>[-\d]+)/$', 'cityfury.contact_views.correct', name='contact_correct'),
    url(r'^contacts/view_corrections/(?P<contact_id>[-\d]+)/$', 'cityfury.contact_views.view_corrections', name='contact_view_corrections'),
    url(r'^contacts/(?P<contact_id>[-\d]+)/$', 'cityfury.contact_views.contact', name='contact'),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('', (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT, 'show_indexes': True}))

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
