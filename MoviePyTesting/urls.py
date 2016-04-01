from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MoviePyTesting.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'movieTest.views.index', name='create_videos_menu'),
    url(r'^create_video$', 'movieTest.views.create_video', name='create_video'),
    url(r'^create_simple_video$', 'movieTest.views.create_simple_video', name='create_simple_video'),
    url(r'^create_photo_quality_video', 'movieTest.views.create_photo_quality_video', name='create_photo_quality_video'),
    url(r'^create_overall_quality_video', 'movieTest.views.create_overall_quality_video', name='create_overall_quality_video'),
    url(r'^create_presentation_video', 'movieTest.views.create_presentation_video', name='create_presentation_video'),
)
