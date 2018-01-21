from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^home/$', views.Home.as_view(), name='home'),
    url(r'^stories/', views.StoriesOverview.as_view(), name='stories_overview'),
    url(r'^games/', views.GamesOverview.as_view(), name='games_overview'),
    url(r'^story/', views.AddStory.as_view(), name='add_story'),
    url(r'^(?P<storyId>\d+)/', views.delete_story, name="delete_story")
]
