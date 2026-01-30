from django.contrib import admin
from .models import Post, PostImages

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'published_date', 'status', 'type']
    search_fields = ['title']

@admin.register(PostImages)
class PostImagesAdmin(admin.ModelAdmin):
    list_display = ['post', 'image']
    search_fields = ['post__title']