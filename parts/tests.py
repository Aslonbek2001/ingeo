from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from parts.models import Application, Carousel
from parts.views.application_view import ApplicationPermission


class CarouselAPITests(APITestCase):
    def setUp(self):
        self.list_url = reverse("carousel-list")
        self.user = get_user_model().objects.create_user(
            username="carousel-admin",
            password="pass123",
        )
        self.active = Carousel.objects.create(
            title="Active",
            title_uz="Active uz",
            title_ru="Active ru",
            title_en="Active en",
            description="Active desc",
            description_uz="Active desc uz",
            description_ru="Active desc ru",
            description_en="Active desc en",
            image=self._uploaded_image("active.jpg"),
            link="https://example.com/active",
            position=1,
            status=True,
        )
        self.inactive = Carousel.objects.create(
            title="Inactive",
            title_uz="Inactive uz",
            title_ru="Inactive ru",
            title_en="Inactive en",
            description="Inactive desc",
            description_uz="Inactive desc uz",
            description_ru="Inactive desc ru",
            description_en="Inactive desc en",
            image=self._uploaded_image("inactive.jpg"),
            link="https://example.com/inactive",
            position=2,
            status=False,
        )

    def _uploaded_image(self, name):
        return SimpleUploadedFile(name, b"fake-image", content_type="image/jpeg")

    def test_anonymous_list_returns_only_active_carousels(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.active.id)

    def test_authenticated_user_can_create_carousel(self):
        self.client.force_authenticate(self.user)
        data = {
            "title": "New Carousel",
            "title_uz": "Yangi Carousel uz",
            "title_ru": "Noviy Carousel ru",
            "title_en": "New Carousel en",
            "description": "New desc",
            "description_uz": "Yangi desc uz",
            "description_ru": "Noviy desc ru",
            "description_en": "New desc en",
            "image": self._uploaded_image("new.jpg"),
            "link": "https://example.com/new",
            "position": 3,
            "status": True,
        }
        response = self.client.post(self.list_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Carousel.objects.filter(id=response.data["id"]).exists())

    def test_authenticated_list_returns_all_carousels(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_ids = {item["id"] for item in response.data}
        self.assertSetEqual(returned_ids, {self.active.id, self.inactive.id})


class ApplicationAPITests(APITestCase):
    def setUp(self):
        self.list_url = reverse("application-list")
        self.user = get_user_model().objects.create_user(
            username="application-admin",
            password="pass123",
        )
        self.app1 = Application.objects.create(
            name="Alice",
            phone="+998901112233",
            message="Need help",
        )
        self.app2 = Application.objects.create(
            name="Bob",
            phone="+998907778899",
            message="Request info",
        )

    def test_authenticated_user_can_list_applications(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = response.data.get("results", response.data)
        returned_ids = {item["id"] for item in payload}
        self.assertSetEqual(returned_ids, {self.app1.id, self.app2.id})

    def test_anonymous_user_cannot_list_applications(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_user_can_create_application(self):
        data = {"name": "Charlie", "phone": "+998901112200", "message": "Hello"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Application.objects.filter(id=response.data["id"]).exists())

    def test_authenticated_user_cannot_create_application(self):
        self.client.force_authenticate(self.user)
        data = {"name": "Delta", "phone": "+998909998877", "message": "Nope"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_delete_application(self):
        self.client.force_authenticate(self.user)
        detail_url = reverse("application-detail", args=[self.app1.id])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Application.objects.filter(id=self.app1.id).exists())

    def test_anonymous_user_cannot_delete_application(self):
        detail_url = reverse("application-detail", args=[self.app1.id])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ApplicationPermissionTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.permission = ApplicationPermission()
        self.user = get_user_model().objects.create_user(
            username="perm-user",
            password="pass123",
        )

    def test_authenticated_user_can_read(self):
        request = self.factory.get("/applications/")
        request.user = self.user
        self.assertTrue(self.permission.has_permission(request, None))

    def test_anonymous_user_cannot_read(self):
        request = self.factory.get("/applications/")
        request.user = AnonymousUser()
        self.assertFalse(self.permission.has_permission(request, None))

    def test_anonymous_user_can_create(self):
        request = self.factory.post("/applications/")
        request.user = AnonymousUser()
        self.assertTrue(self.permission.has_permission(request, None))

    def test_authenticated_user_cannot_create(self):
        request = self.factory.post("/applications/")
        request.user = self.user
        self.assertFalse(self.permission.has_permission(request, None))

    def test_authenticated_user_can_delete(self):
        request = self.factory.delete("/applications/1/")
        request.user = self.user
        self.assertTrue(self.permission.has_permission(request, None))
