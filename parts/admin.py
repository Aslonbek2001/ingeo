from django.contrib import admin
from .models import Carousel, Application, Collaborations

@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'position')
    list_editable = ('status', 'position')
    search_fields = ('title',)
    list_filter = ('status',)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'submitted_at')
    search_fields = ('name', 'phone')
    list_filter = ('submitted_at',)

@admin.register(Collaborations)
class CollaborationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'position')
    list_editable = ('status', 'position')
    search_fields = ('title',)
    list_filter = ('status',)