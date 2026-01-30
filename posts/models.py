from django.db import models
from versatileimagefield.fields import VersatileImageField
from core.mixins import auto_delete_image_with_renditions
from menus.models import Page
from django.utils import timezone

type_choices = (
    ("news", "Yangilik"),
    ("announcement", "E'lon"),
    ("desertion", "Desertatsiya e'loni"),
)

# Create your models here.
class Post(models.Model):
    
    title = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Sarlavha"
    )
    description = models.TextField(
        help_text="Batafsil ma'lumot", null=True, blank=True
    )
    status = models.BooleanField(
        default=True,
        help_text="Aktiv yoki yo'q"
    )
    published_date = models.DateTimeField(
        default=timezone.now,
        db_index=True,
        help_text="E'lon qilingan sana"
    )
    type = models.CharField(
        max_length=20,
        db_index=True,
        choices=type_choices,
        default="news",
        help_text="Turini tanlang"
    )
    
    pages = models.ManyToManyField(
        Page,
        blank=True,
        related_name='posts',
        help_text="Post qaysi sahifalarga tegishli"
    )

    class Meta:
        db_table = "posts"
        ordering = ["-published_date"]
        indexes = [
            models.Index(fields=["status", "type", "-published_date"]),
        ]
        verbose_name = "Post (Yangilik/E'lon)"
        verbose_name_plural = "Postlar (Yangiliklar va E'lonlar)"

    def __str__(self):
        return f"{self.title}"


class PostImages(models.Model):
    
    
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="images",
        help_text="Postga tegishli rasm"
    )
    image = models.ImageField(
        upload_to="post_images/",
        help_text="Rasm"
    )

    class Meta:
        db_table = "post_images"
        verbose_name = "Post Rasmi"
        verbose_name_plural = "Post Rasmlari"

    def __str__(self):
        return f"Post: {self.post.title} - Rasm ID: {self.id}"


auto_delete_image_with_renditions(PostImages, "image")