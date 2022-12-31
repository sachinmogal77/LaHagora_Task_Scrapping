from django.contrib import admin
from .models import Playstore
# Register your models here.

@admin.register(Playstore)
class PlaystoreAdmin(admin.ModelAdmin):
    list_display = ['title','description','summary','created_at','updated_at','reviews','ratings','histogram']
