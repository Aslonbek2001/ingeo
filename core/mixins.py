import os
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from versatileimagefield.fields import VersatileImageField


def auto_delete_image_with_renditions(model, field_name):
    """
    - Model object o‘chirilganda -> original rasm + renditionlar o‘chadi
    - Modelda image yangilanganda -> eski rasm + renditionlar o‘chadi
    """

    @receiver(post_delete, sender=model)
    def auto_delete_file_on_delete(sender, instance, **kwargs):
        file_field = getattr(instance, field_name, None)
        if file_field and file_field.name:
            # Renditionlarni o‘chirish
            if isinstance(file_field.field, VersatileImageField):
                file_field.delete_all_created_images()
            # Original faylni o‘chirish
            if file_field.path and os.path.isfile(file_field.path):
                os.remove(file_field.path)

    @receiver(pre_save, sender=model)
    def auto_delete_file_on_change(sender, instance, **kwargs):
        if not instance.pk:
            return  # yangi obyekt uchun

        try:
            old_file = getattr(sender.objects.get(pk=instance.pk), field_name, None)
        except sender.DoesNotExist:
            return

        new_file = getattr(instance, field_name, None)

        if old_file and old_file != new_file and old_file.name:
            # Renditionlarni o‘chirish
            if isinstance(old_file.field, VersatileImageField):
                old_file.delete_all_created_images()
            # Original faylni o‘chirish
            if old_file.path and os.path.isfile(old_file.path):
                os.remove(old_file.path)
