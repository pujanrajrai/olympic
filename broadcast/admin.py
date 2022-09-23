from django.contrib import admin
from .models import Categories, Broadcast, News, PlayerProfile


# Register your models here.
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    list_display = ['title', 'categories', 'total_view']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'picture', 'short_desc']


@admin.register(PlayerProfile)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'profile', 'short_desc']
