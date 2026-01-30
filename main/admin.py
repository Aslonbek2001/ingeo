from django.contrib import admin
from main.models import Company
# Register your models here.

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'phone_number', 'email')
    search_fields = ('name_uz', 'name_ru', 'name_en', 'phone_number', 'email')
    list_filter = ('name_uz',)
