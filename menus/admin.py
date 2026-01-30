from django.contrib import admin
from .models import Menu, Page, PageImages, Employee, PageFiles
# Register your models here.

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "status", "position"]
    list_filter = ["status"]
    search_fields = ["title"]
    ordering = ["position"]

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "type", "status"]
    list_filter = ["status", "type"]
    search_fields = ["title", "description"]
    ordering = ["title"]
    prepopulated_fields = {"slug": ("title",)}

@admin.register(PageImages)
class PageImagesAdmin(admin.ModelAdmin):
    list_display = ["id", "page", "image"]
    search_fields = ["page__title"]
    ordering = ["page"]
    list_filter = ["page"]

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "position", "phone", "email"]
    search_fields = ["full_name", "position", "email", "phone"]
    ordering = ["full_name"]

@admin.register(PageFiles)
class PageFilesAdmin(admin.ModelAdmin):
    list_display = ["id", "file", "page", "position", "status"]
    list_filter = ["status", "page"]
    search_fields = ["file", "title"]
    ordering = ["position"]


