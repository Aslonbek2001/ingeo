from django.db import models
from core.mixins import auto_delete_image_with_renditions


class Company(models.Model):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    address_uz = models.TextField()
    address_ru = models.TextField()
    address_en = models.TextField()
    logo = models.FileField(upload_to="company_logos/")
    stat_1 = models.CharField(max_length=50)
    stat_2 = models.CharField(max_length=50)
    stat_3 = models.CharField(max_length=50)
    stat_4 = models.CharField(max_length=50)
    instagram = models.URLField(blank=True, null=True)
    telegram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()



auto_delete_image_with_renditions(Company, "logo")


    

