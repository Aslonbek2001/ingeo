from django.db import models
from core.mixins import auto_delete_image_with_renditions


class Carousel(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='carousel/')
    description = models.TextField(blank=True, null=True, db_index=True)
    link = models.URLField(blank=True, null=True)
    position = models.PositiveIntegerField(default=0, db_index=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title


class Application(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    phone = models.CharField(max_length=20, db_index=True)
    message = models.TextField(blank=True, null=True, db_index=True)
    submitted_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.name} - {self.phone}"

class Collaborations(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    image = models.ImageField(upload_to='collaborations/')
    link = models.URLField(blank=True, null=True)
    position = models.PositiveIntegerField(default=0, db_index=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ['position']
        
    def __str__(self):
        return self.title





auto_delete_image_with_renditions(Carousel, "image")
