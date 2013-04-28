from django.conf.urls.defaults import *
from blog.views import *

urlpatterns = patterns('blog.views',
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/'+
        r'(?P<slug>[-\w]+)/$', view=PostDateDetailView.as_view(),
        name='blog_detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/$',
        view = PostDayArchiveView.as_view(), name='blog_archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
        view = PostMonthArchiveView.as_view(), name='blog_archive_month'),
    url(r'^(?P<year>\d{4})/$',
        PostYearArchiveView.as_view(), name='blog_archive_year'),
    url(r'^categories/(?P<slug>[-\w]+)/$', view=CategoryDetailView.as_view(),
        name='blog_category_detail'),
    url (r'^categories/$', view=CategoryListView.as_view(),
         name='blog_category_list'),
    url(r'^tags/(?P<slug>[-\w]+)/$',
        view='tag_detail',
        name='blog_tag_detail'
    ),
    url(r'^page/(?P<page>\d+)/$', PostListView.as_view(), 
        name='blog_index_paginated'),
    url(r'^$', PostListView.as_view(), name='blog_index'
    ),
)
