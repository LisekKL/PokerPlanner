from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^home/', views.stories_overview, name='stories_overview'),
]
