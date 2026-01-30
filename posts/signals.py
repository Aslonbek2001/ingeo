from django.db.models.signals import post_save, post_delete
import os
from django.dispatch import receiver
from .models import Post
from versatileimagefield.image_warmer import VersatileImageFieldWarmer

@receiver(post_save, sender=Post)
def generate_post_images(sender, instance, **kwargs):
    """
    Post saqlanganda avtomatik medium rasm yaratadi
    """
    if instance.image:
        # Warmer yaratamiz
        warmer = VersatileImageFieldWarmer(
            instance_or_queryset=instance,
            rendition_key_set="post_image",
            image_attr="image",
        )
        warmer.warm()
