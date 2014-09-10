from django.conf.urls import patterns, include, url
from django.contrib import admin
from NFBasic import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Notifier.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.index, name='index'),

    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),

    url(r'^views/(?:(\d+)/)?$', views.view, name='view'),
    url(r'^archive/(\d{4}-\d{2})/(?:(\d+)/)?$', views.get_archive, name='archive'),
    url(r'^grade/(\w+?)/(?:(\d+)/)?$', views.get_grade, name='grade'),
    url(r'^detail/(\d+)/$', views.detail, name='detail'),
    url(r'^notify/$', views.notify, name='notify'),

)