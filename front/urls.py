from django.conf.urls import patterns, include, url
from front import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^process$', views.process, name='process'),
    url(r'^get_links$', views.get_links, name='get_links')

    # Examples:
    # url(r'^$', 'broken_links_analyzer.views.home', name='home'),
    # url(r'^broken_links_analyzer/', include('broken_links_analyzer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)