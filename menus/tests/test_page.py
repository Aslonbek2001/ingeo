from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from menus.models import Page


class PageListCreateAPITests(APITestCase):
    def setUp(self):
        self.list_url = reverse("page-list-create")
        self.user = get_user_model().objects.create_user(
            username="page-user",
            password="pass123",
        )

        self.active_page = Page.objects.create(
            title="Active",
            title_uz="Active uz",
            title_ru="Active ru",
            title_en="Active en",
            description="Desc",
            description_uz="Desc uz",
            description_ru="Desc ru",
            description_en="Desc en",
            slug="active-page",
            status=True,
            type="page",
        )
        self.inactive_page = Page.objects.create(
            title="Inactive",
            title_uz="Inactive uz",
            title_ru="Inactive ru",
            title_en="Inactive en",
            description="Desc",
            description_uz="Desc uz",
            description_ru="Desc ru",
            description_en="Desc en",
            slug="inactive-page",
            status=False,
            type="page",
        )

    def test_anonymous_list_is_paginated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("results", response.data)
        self.assertEqual(response.data["count"], 2)

        returned_ids = {item["id"] for item in response.data["results"]}
        self.assertSetEqual(returned_ids, {self.active_page.id, self.inactive_page.id})

    def test_anonymous_cannot_create_page(self):
        payload = {
            "title_uz": "New uz",
            "title_ru": "New ru",
            "title_en": "New en",
            "description_uz": "New desc uz",
            "description_ru": "New desc ru",
            "description_en": "New desc en",
            "status": True,
            "type": "page",
            "slug": "new-page",
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_page(self):
        self.client.force_authenticate(self.user)
        payload = {
            "title_uz": "New uz",
            "title_ru": "New ru",
            "title_en": "New en",
            "description_uz": "New desc uz",
            "description_ru": "New desc ru",
            "description_en": "New desc en",
            "status": True,
            "type": "page",
            "slug": "new-page",
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Page.objects.filter(id=response.data["id"]).exists())


class PageDetailAPITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="page-detail-user",
            password="pass123",
        )
        self.active_page = Page.objects.create(
            title="Active",
            title_uz="Active uz",
            title_ru="Active ru",
            title_en="Active en",
            description="Desc",
            description_uz="Desc uz",
            description_ru="Desc ru",
            description_en="Desc en",
            slug="active-detail",
            status=True,
            type="page",
        )
        self.inactive_page = Page.objects.create(
            title="Inactive",
            title_uz="Inactive uz",
            title_ru="Inactive ru",
            title_en="Inactive en",
            description="Desc",
            description_uz="Desc uz",
            description_ru="Desc ru",
            description_en="Desc en",
            slug="inactive-detail",
            status=False,
            type="page",
        )
        self.active_detail_url = reverse("page-detail", kwargs={"id": self.active_page.id})
        self.inactive_detail_url = reverse("page-detail", kwargs={"id": self.inactive_page.id})

    def test_anonymous_can_retrieve_active_page(self):
        response = self.client.get(self.active_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.active_page.id)

    def test_anonymous_cannot_retrieve_inactive_page(self):
        response = self.client.get(self.inactive_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_user_can_retrieve_inactive_page(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.inactive_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.inactive_page.id)

    def test_update_requires_authentication(self):
        payload = {
            "title_uz": "Updated uz",
            "title_ru": "Updated ru",
            "title_en": "Updated en",
            "description_uz": "Updated desc uz",
            "description_ru": "Updated desc ru",
            "description_en": "Updated desc en",
            "status": True,
            "type": "page",
            "slug": "active-detail",
        }

        response = self.client.put(self.active_detail_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.user)
        response = self.client.put(self.active_detail_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.active_page.refresh_from_db()
        self.assertEqual(self.active_page.title_uz, payload["title_uz"])

    def test_delete_requires_authentication(self):
        response = self.client.delete(self.active_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.user)
        response = self.client.delete(self.active_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Page.objects.filter(id=self.active_page.id).exists())

