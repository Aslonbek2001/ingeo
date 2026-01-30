from django.db import models
from django.utils.text import slugify
from core.mixins import auto_delete_image_with_renditions


class Menu(models.Model):
    title = models.CharField(max_length=200, db_index=True,)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        db_index=True,
        blank=True,
        null=True
    )
    status = models.BooleanField(default=True)
    has_page = models.BooleanField(default=False, db_index=True)
    position = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title


class Page(models.Model):
    PAGE_TYPES = (
        ('department', "Bo‘lim"),
        ('faculty', 'Kafedra'),
        ('news', 'Yangiliklar'),
        ('lab', 'Laboratoriya'),
        ('leadership', 'Rahbariyat'),
        ('page', 'Sahifa'),
        ("scientific_direction", "Ilmiy yo‘nalish"),
        ('postgraduate_education', "Oliy ta'limdan keyingi ta'lim")
    )
    title = models.CharField(max_length=200, db_index=True,)
    sub_title = models.TextField(null=True, blank=True, db_index=True)
    direction = models.CharField(null=True, blank=True, max_length=250)
    duration = models.CharField(null=True, blank=True, max_length=20)
    position = models.IntegerField(null=True, blank=True)
    logo = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=30, db_index=True, choices=PAGE_TYPES, default='page')
    menu = models.OneToOneField(
        Menu,
        on_delete=models.CASCADE,
        related_name='page',
        db_index=True,
        null=True, blank=True
    )
    slug = models.SlugField(unique=True, db_index=True, max_length=100, null=True, blank=True)
    status = models.BooleanField(default=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    is_menu_page = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            if not self.menu:
                self.slug = slugify(self.title)
            else: self.slug = slugify(self.menu.title)

        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['title', 'type', 'status']),
            models.Index(fields=['title_uz', 'title_ru', 'title_en'], name='page_trans_titles_idx'),
        ]
    


class PageImages(models.Model):
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name="images",
        db_index=True,
        help_text="Paga tegishli rasm"
    )
    image = models.ImageField(
        upload_to="page_images/",
        help_text="Rasm"
    )

    class Meta:
        db_table = "page_images"
        verbose_name = "Post Rasmi"
        verbose_name_plural = "Post Rasmlari"

    def __str__(self):
        return f"Post: {self.page.title} - Rasm ID: {self.id}"


class Employee(models.Model):
    full_name = models.CharField(max_length=200, db_index=True,)
    position = models.CharField(max_length=200, db_index=True,)
    description = models.TextField(blank=True, null=True)
    pages = models.ManyToManyField(
        Page,
        related_name="employees",
        db_index=True,
        blank=True
    )
    order = models.PositiveIntegerField(default=0, db_index=True,)
    image = models.ImageField(upload_to='employees/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name


class PageFiles(models.Model):
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="files",
        help_text="Fayl tegishli xodim"
    )
    title = models.CharField(max_length=200, db_index=True, blank=True, null=True)
    file = models.FileField(
        upload_to="employee_files/",
        help_text="Fayl"
    )
    position = models.PositiveIntegerField(default=0, db_index=True,)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "page_files"
        verbose_name = "Page Fayli"
        verbose_name_plural = "Page Fayllari"

    def __str__(self):
        return f"Page: {self.title} - Fayl ID: {self.id}"
    

auto_delete_image_with_renditions(PageImages, "image")
auto_delete_image_with_renditions(PageFiles, "file")
auto_delete_image_with_renditions(Employee, "image")