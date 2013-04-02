from django.conf.urls.defaults import *

urlpatterns = patterns('',
url(r'^$', 'blog.views.home'),
url(r'^searchpage/$','blog.views.searchView'),
url(r'^(detail|info)/(?P<id>\d+)/((?P<showComments>.*)/)?$', 'blog.views.blog_detail'),
url(r'^search/(.*)$', 'blog.views.blog_search'),
url(r'^editcomment/(?P<id>\d+)/?$','blog.views.editcomment'),
)
