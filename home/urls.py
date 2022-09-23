from . import views
from django.urls import path

app_name = 'home'

urlpatterns = [
    # login
    path('', views.home, name='home'),
    path('news/', views.NewsListView.as_view(), name='news'),
    path('players/', views.PlayerProfileListView.as_view(), name='player'),
    path('news/<str:pk>', views.NewsDetailsListView.as_view(), name='news_details'),
    path('players/<str:pk>', views.PlayerDetailsListView.as_view(), name='players_details'),

    path('live/', views.LiveMatchesListView.as_view(), name='live'),
    path('live/<str:pk>', views.LiveMatchesDetailsListView.as_view(), name='live_details'),


]
