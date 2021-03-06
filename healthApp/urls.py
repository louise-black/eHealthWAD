from django.conf.urls import patterns, url
from healthApp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^category/(?P<user_name_slug>[\w\-]+)/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<user_name_slug>[\w\-]+)/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^search/', views.search, name='search'),
    url(r'^profile_page/$', views.profile_page, name = 'profile_page'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^edit_profile/$', views.editProfile, name='edit_profile'),
    )
