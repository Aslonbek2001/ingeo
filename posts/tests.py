from django.test import TestCase
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from menus.models import Page
from posts.models import Post, PostImages
from posts.serializers import PostManageSerializer


class PostManageSerializerTests(TestCase):
    def setUp(self):
        self.page = Page.objects.create(title="Sample Page", type="page")
        self.post = Post.objects.create(
            title="Initial title",
            description="Initial description",
            status=True,
            published_date=timezone.now(),
            type="news",
            title_uz="Initial uz",
            title_ru="Initial ru",
            title_en="Initial en",
            description_uz="Initial desc uz",
            description_ru="Initial desc ru",
            description_en="Initial desc en",
        )
        self.post.pages.add(self.page)

        image_content = SimpleUploadedFile("test.jpg", b"fake-image", content_type="image/jpeg")
        self.image1 = PostImages.objects.create(post=self.post, image=image_content)
        image_content2 = SimpleUploadedFile("test2.jpg", b"fake-image-2", content_type="image/jpeg")
        self.image2 = PostImages.objects.create(post=self.post, image=image_content2)

    def test_update_removes_images_not_in_exists_ids(self):
        data = {
            "title_uz": "Updated uz",
            "title_ru": "Updated ru",
            "title_en": "Updated en",
            "description_uz": "Updated desc uz",
            "description_ru": "Updated desc ru",
            "description_en": "Updated desc en",
            "status": True,
            "published_date": timezone.now(),
            "type": "news",
            "pages": [self.page.id],
            "exists_image_ids": [self.image1.id],
            "upload_images": [],
        }

        serializer = PostManageSerializer(instance=self.post, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()

        self.post.refresh_from_db()

        self.assertTrue(self.post.images.filter(id=self.image1.id).exists())
        self.assertFalse(self.post.images.filter(id=self.image2.id).exists())
