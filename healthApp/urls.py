from django.conf.urls import patterns, url
from healthApp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^category/(?P<category_name_slug>\w+)$', views.category, name='category'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>\w+)/add_page/$', views.add_page, name='add_page'),
    url(r'^search/', views.search, name='search'),
    url(r'^bing_search/', views.bing_search, name ='bing_search'),
    url(r'^healthfinder_search/', views.healthfinder_search, name='healthfinder_search'),
    url(r'^medline_search/', views.medline_search, name='medline_search'),
    )
