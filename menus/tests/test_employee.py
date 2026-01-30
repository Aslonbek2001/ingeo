from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from menus.models import Employee, Page


class EmployeeListCreateAPITests(APITestCase):
    def setUp(self):
        self.url = reverse("employee-list-create")
        self.page = Page.objects.create(
            title="Science",
            title_uz="Science uz",
            title_ru="Science ru",
            title_en="Science en",
            slug="science",
            type="department",
            status=True,
        )
        self.user = get_user_model().objects.create_user(
            username="emp-admin",
            password="pass123",
        )
        self.employee = Employee.objects.create(
            full_name="Alice",
            full_name_uz="Alice uz",
            full_name_ru="Alice ru",
            full_name_en="Alice en",
            position="Scientist",
            position_uz="Scientist uz",
            position_ru="Scientist ru",
            position_en="Scientist en",
            order=1,
            status=True,
        )
        self.employee.pages.add(self.page)

    def test_list_returns_paginated_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(response.data["results"][0]["id"], self.employee.id)

    def test_filter_by_page_id(self):
        page_two = Page.objects.create(
            title="Dean Office",
            title_uz="Dean Office uz",
            title_ru="Dean Office ru",
            title_en="Dean Office en",
            slug="dean-office",
            type="faculty",
            status=True,
        )
        other_employee = Employee.objects.create(
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
        other_employee.pages.add(page_two)

        response = self.client.get(self.url, {"page_id": str(self.page.id)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [item["id"] for item in response.data["results"]]
        self.assertEqual(ids, [self.employee.id])

    def test_create_requires_authentication(self):
        payload = {
            "full_name_uz": "Charlie uz",
            "full_name_ru": "Charlie ru",
            "full_name_en": "Charlie en",
            "position_uz": "Teacher uz",
            "position_ru": "Teacher ru",
            "position_en": "Teacher en",
            "description_uz": "Desc uz",
            "description_ru": "Desc ru",
            "description_en": "Desc en",
            "order": 5,
            "pages": [self.page.id],
            "phone": "+998901234567",
            "email": "charlie@example.com",
            "status": True,
        }

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created = Employee.objects.get(id=response.data["id"])
        self.assertEqual(created.full_name_uz, payload["full_name_uz"])
        self.assertEqual(created.pages.first().id, self.page.id)
