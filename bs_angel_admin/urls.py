# from django.conf.urls import include, url
# from django.contrib import admin

# urlpatterns = [
#     url(r'^admin/', include(admin.site.urls)),
# ]

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^', include('login.urls')),
 )

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
