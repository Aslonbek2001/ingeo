from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from menus.models import Page, PageFiles, PageImages


def _make_test_png(name="img.png"):
    png_1x1 = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
        b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc`\x00\x00"
        b"\x00\x02\x00\x01\xe2!\xbc3\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    return SimpleUploadedFile(name, png_1x1, content_type="image/png")


def _make_test_pdf(name="file.pdf"):
    return SimpleUploadedFile(name, b"%PDF-1.4\n%test\n", content_type="application/pdf")


class PageFileAPITests(APITestCase):
    def setUp(self):
        self.list_url = reverse("page-file-list-create")
        self.page = Page.objects.create(
            title="Docs",
            title_uz="Docs uz",
            title_ru="Docs ru",
            title_en="Docs en",
            slug="docs",
            status=True,
            type="page",
        )
        self.active_file = PageFiles.objects.create(
            page=self.page,
            title="Active file",
            title_uz="Active file uz",
            title_ru="Active file ru",
            title_en="Active file en",
            position=1,
            status=True,
            file=SimpleUploadedFile("active.pdf", b"content", content_type="application/pdf"),
        )
        self.inactive_file = PageFiles.objects.create(
            page=self.page,
            title="Inactive file",
            title_uz="Inactive file uz",
            title_ru="Inactive file ru",
            title_en="Inactive file en",
            position=2,
            status=False,
            file=SimpleUploadedFile("inactive.pdf", b"content", content_type="application/pdf"),
        )
        self.staff_user = get_user_model().objects.create_user(
            username="staff",
            password="pass123",
            is_staff=True,
        )

    def test_anonymous_list_returns_only_active_files(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.active_file.id)

    def test_staff_user_sees_all_files(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = {item["id"] for item in response.data}
        self.assertSetEqual(ids, {self.active_file.id, self.inactive_file.id})

    def test_create_requires_authentication(self):
        payload = {
            "page": self.page.id,
            "title_uz": "New file uz",
            "title_ru": "New file ru",
            "title_en": "New file en",
            "position": "3",
            "status": "true",
        }
        response = self.client.post(
            self.list_url,
            {**payload, "file": _make_test_pdf("new.pdf")},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.staff_user)
        response = self.client.post(
            self.list_url,
            {**payload, "file": _make_test_pdf("new.pdf")},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertTrue(PageFiles.objects.filter(id=response.data["id"]).exists())

    def test_detail_update_and_delete(self):
        detail_url = reverse("page-file-detail", kwargs={"id": self.active_file.id})
        response = self.client.patch(detail_url, {"title_uz": "Updated"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.staff_user)
        response = self.client.patch(detail_url, {"title_uz": "Updated"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.active_file.refresh_from_db()
        self.assertEqual(self.active_file.title_uz, "Updated")

        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PageFiles.objects.filter(id=self.active_file.id).exists())


class PageImageAPITests(APITestCase):
    def setUp(self):
        self.list_url = reverse("page-image-list-create")
        self.page = Page.objects.create(
            title="Gallery",
            title_uz="Gallery uz",
            title_ru="Gallery ru",
            title_en="Gallery en",
            slug="gallery",
            status=True,
            type="page",
        )
        self.staff_user = get_user_model().objects.create_user(
            username="image-staff",
            password="pass123",
            is_staff=True,
        )
        self.image = PageImages.objects.create(
            page=self.page,
            image=_make_test_png("existing.png"),
        )

    def test_anonymous_list_images(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.image.id)

    def test_create_image_requires_authentication(self):
        payload = {
            "page": self.page.id,
        }
        response = self.client.post(
            self.list_url,
            {**payload, "image": _make_test_png("new.png")},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.staff_user)
        response = self.client.post(
            self.list_url,
            {**payload, "image": _make_test_png("new.png")},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertTrue(PageImages.objects.filter(id=response.data["id"]).exists())
