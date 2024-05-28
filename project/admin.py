from django.contrib import admin
from .models import Ebook, UserReading

@admin.register(Ebook)
class EbookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'description','category','cover','file')


@admin.register(UserReading)
class UserReadingAdmin(admin.ModelAdmin):
    list_display = ('user', 'ebook', 'read_count')
   
