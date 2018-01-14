from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^login/$', views.login_player, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout_player, name='logout'),
    url(r'^home/', views.stories_overview, name='stories_overview'),
]
