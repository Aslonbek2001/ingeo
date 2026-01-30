from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from menus.models import Menu, Page


class MenuListCreateAPITests(APITestCase):
    def setUp(self):
        self.url = reverse("menu-list-create")
        self.user = get_user_model().objects.create_user(
            username="menu-admin",
            password="pass123",
        )
        self.root_active = Menu.objects.create(
            title="Root Active",
            title_uz="Root Active uz",
            title_ru="Root Active ru",
            title_en="Root Active en",
            status=True,
            position=1,
        )
        self.child = Menu.objects.create(
            title="Child Active",
            title_uz="Child Active uz",
            title_ru="Child Active ru",
            title_en="Child Active en",
            status=True,
            position=1,
            parent=self.root_active,
        )
        Menu.objects.create(
            title="Root Inactive",
            title_uz="Root Inactive uz",
            title_ru="Root Inactive ru",
            title_en="Root Inactive en",
            status=False,
            position=2,
        )

    def test_anonymous_list_returns_only_active_roots(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.root_active.id)
        self.assertEqual(len(response.data[0]["children"]), 1)
        self.assertEqual(response.data[0]["children"][0]["id"], self.child.id)

    def test_authenticated_list_returns_all_roots(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        root_ids = [item["id"] for item in response.data]
        self.assertCountEqual(root_ids, [self.root_active.id, Menu.objects.filter(status=False).first().id])

    def test_authenticated_user_can_create_menu_with_page(self):
        self.client.force_authenticate(self.user)
        payload = {
            "title_uz": "New Menu uz",
            "title_ru": "New Menu ru",
            "title_en": "New Menu en",
            "page_type": "page",
            "status": True,
            "position": 5,
            "parent": None,
            "has_page": True,
            "page_slug": "new-menu",
        }

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created = Menu.objects.get(id=response.data["id"])
        self.assertTrue(created.has_page)
        self.assertIsNotNone(created.page)
        self.assertEqual(created.page.slug, "new-menu")
        self.assertEqual(created.page.type, "page")

    def test_anonymous_user_cannot_create_menu(self):
        payload = {
            "title_uz": "New Menu uz",
            "title_ru": "New Menu ru",
            "title_en": "New Menu en",
            "page_type": "page",
            "status": True,
            "position": 5,
            "parent": None,
            "has_page": False,
        }

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class MenuDetailAPITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="detail-admin",
            password="pass123",
        )
        self.menu = Menu.objects.create(
            title="Detail Menu",
            title_uz="Detail Menu uz",
            title_ru="Detail Menu ru",
            title_en="Detail Menu en",
            status=True,
            position=1,
            has_page=True,
        )
        self.detail_url = reverse("menu-detail", kwargs={"menu_id": self.menu.id})

    def test_retrieve_requires_no_authentication(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.menu.id)

    def test_update_requires_authentication(self):
        payload = {
            "title_uz": "Updated uz",
            "title_ru": "Updated ru",
            "title_en": "Updated en",
            "page_type": "page",
            "status": True,
            "position": 3,
            "parent": None,
            "has_page": False,
        }
        response = self.client.put(self.detail_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.user)
        response = self.client.put(self.detail_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title_uz"], payload["title_uz"])
        self.menu.refresh_from_db()
        self.assertFalse(self.menu.has_page)

    def test_delete_requires_authentication(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Menu.objects.filter(id=self.menu.id).exists())
