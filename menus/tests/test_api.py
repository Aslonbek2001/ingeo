from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from menus.models import Employee, Menu, Page, PageFiles


class MenuAPITests(APITestCase):
    def setUp(self):
        self.list_url = reverse("menu-list-create")
        self.user = get_user_model().objects.create_user(
            username="menu-admin",
            password="pass123",
            is_staff=True,
        )
        self.active_root = Menu.objects.create(
            title="Active root",
            title_uz="Active root uz",
            title_ru="Active root ru",
            title_en="Active root en",
            status=True,
            position=1,
        )
        self.child = Menu.objects.create(
            title="Child",
            title_uz="Child uz",
            title_ru="Child ru",
            title_en="Child en",
            status=True,
            position=1,
            parent=self.active_root,
        )
        Menu.objects.create(
            title="Inactive",
            title_uz="Inactive uz",
            title_ru="Inactive ru",
            title_en="Inactive en",
            status=False,
            position=2,
        )

    def test_anonymous_menu_list_returns_only_active_roots(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        root = response.data[0]
        self.assertEqual(root["id"], self.active_root.id)
        self.assertEqual(len(root["children"]), 1)
        self.assertEqual(root["children"][0]["id"], self.child.id)

    def test_authenticated_user_can_create_menu_with_page(self):
        self.client.force_authenticate(self.user)
        payload = {
            "title_uz": "New menu uz",
            "title_ru": "New menu ru",
            "title_en": "New menu en",
            "page_type": "page",
            "status": True,
            "position": 5,
            "parent": None,
            "has_page": True,
            "page_slug": "new-menu-slug",
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_id = response.data["id"]

        menu = Menu.objects.select_related("page").get(id=created_id)
        self.assertIsNotNone(menu.page)
        self.assertEqual(menu.page.slug, payload["page_slug"])
        self.assertEqual(menu.page.type, payload["page_type"])


class PageAPITests(APITestCase):
    def setUp(self):
        self.page = Page.objects.create(
            title="About",
            title_uz="About uz",
            title_ru="About ru",
            title_en="About en",
            description="Desc",
            description_uz="Desc uz",
            description_ru="Desc ru",
            description_en="Desc en",
            slug="about",
            status=True,
            type="page",
        )
        self.detail_url = reverse("page-for-users", args=[self.page.slug])

    def test_page_detail_for_users_returns_active_page(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["slug"], self.page.slug)

    def test_inactive_page_returns_404(self):
        self.page.status = False
        self.page.save()

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EmployeeAPITests(APITestCase):
    def setUp(self):
        self.list_url = reverse("employee-list-create")
        self.page_one = Page.objects.create(
            title="Department",
            title_uz="Department uz",
            title_ru="Department ru",
            title_en="Department en",
            slug="dept",
            status=True,
            type="department",
        )
        self.page_two = Page.objects.create(
            title="Faculty",
            title_uz="Faculty uz",
            title_ru="Faculty ru",
            title_en="Faculty en",
            slug="faculty",
            status=True,
            type="faculty",
        )
        self.employee_one = Employee.objects.create(
            full_name="Alice",
            full_name_uz="Alice uz",
            full_name_ru="Alice ru",
            full_name_en="Alice en",
            position="Teacher",
            position_uz="Teacher uz",
            position_ru="Teacher ru",
            position_en="Teacher en",
            order=1,
            status=True,
        )
        self.employee_one.pages.add(self.page_one)
        self.employee_two = Employee.objects.create(
            full_name="Bob",
            full_name_uz="Bob uz",
            full_name_ru="Bob ru",
            full_name_en="Bob en",
            position="Assistant",
            position_uz="Assistant uz",
            position_ru="Assistant ru",
            position_en="Assistant en",
            order=2,
            status=True,
        )
        self.employee_two.pages.add(self.page_two)

    def test_employee_list_filters_by_page(self):
        response = self.client.get(self.list_url, {"page_id": str(self.page_one.id)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], self.employee_one.id)


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
        self.assertEqual(len(response.data), 2)
        returned_ids = {item["id"] for item in response.data}
        self.assertSetEqual(returned_ids, {self.active_file.id, self.inactive_file.id})
