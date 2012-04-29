from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'shortcake.views.home', name='home'),
    url(r'^api/$','shortcake.views.api_documentation'),
    url(r'^api/latest/$', 'shortcake.views.latest', name='latest'),
    url(r'^api/latest/(?P<count>\d+)/$', 'shortcake.views.latest', name='latest'),
    url(r'^api/popular/$', 'shortcake.views.top_ten', name='top_ten'),
    url(r'^api/(?P<short_suffix>.+)/accesses/$', 'shortcake.views.shurl_accesses', name='shurl_accesses'),
    url(r'^api/(?P<short_suffix>.+)/stats/$', 'shortcake.views.shurl_stats', name='shurl_stats'),
    # dangerous: this matches everything after api!
    url(r'^api/(?P<short_suffix>.+)/$', 'shortcake.views.forward', name='forward'),
    # even more dangerous: this matches everything!
    url(r'^(?P<short_suffix>.+)/$', 'shortcake.views.forward', name='forward'),
    
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
)
