from . import views
from django.urls import path

app_name = 'broadcast'

urlpatterns = [
    # login
    path('create/', views.BroadCastCreateView.as_view(), name='create_broadcast'),
    path('list/<str:type>', views.BroadCastListView.as_view(), name='list_broadcast'),
    path('update/<str:pk>', views.BroadCastUpdateView.as_view(), name='update_broadcast'),
    path('delete/', views.delete_video, name='delete_video'),

    path('views/<str:pk>', views.view_video, name='view_video'),

]
