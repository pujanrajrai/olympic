from . import views
from django.urls import path

app_name = 'home'

urlpatterns = [
    # login
    path('', views.home, name='home'),
]
