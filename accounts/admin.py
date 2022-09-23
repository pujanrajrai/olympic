from django.contrib import admin
from .models import MyUser


# Register your models here.

@admin.register(MyUser)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_blocked', 'is_email_verified']
