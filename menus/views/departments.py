from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from menus.models import Page
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from django.shortcuts import get_object_or_404
from core.pagination import CustomPageNumberPagination
from menus.serializers.departments_serializers import (
    DepartmentListSerializer,
    DepartmentSerializer,
)


@extend_schema(
    tags=["Departments"],
    summary="List and Create Pages",
    description="Allows admin users to list all pages or create a new page.",
    parameters=[
        OpenApiParameter(
            name="type",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            enum=[choice[0] for choice in Page.PAGE_TYPES],
            description="Filter pages by type.",
        ),
    ],
)
class DepartmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Page.objects.filter(type="department").order_by("position")
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "menu", "title", "type"]
    serializer_class = DepartmentSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Page.objects.filter(type="department", status=True, is_menu_page=False).order_by("position")
        return Page.objects.filter(type="department", is_menu_page=False).order_by("position")

    def get_serializer_class(self):
        if self.request.method == "GET":
            return DepartmentListSerializer
        return DepartmentSerializer

    def perform_create(self, serializer):
        serializer.save(type="department")


@extend_schema(
    tags=["Departments"],
    summary="Retrieve, Update, or Delete a Page",
    description="Retrieve, partially update, or delete a specific page by id or slug.",
    parameters=[
        OpenApiParameter(
            name="lookup",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            required=True,
            description="Page id (numeric) or slug.",
        ),
    ],
)
class DepartmentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "lookup"

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Page.objects.filter(status=True)
        return Page.objects.all()

    def get_object(self):
        lookup_value = self.kwargs.get(self.lookup_field)
        queryset = self.get_queryset()
        if lookup_value is not None and lookup_value.isdigit():
            return get_object_or_404(queryset, id=int(lookup_value))
        return get_object_or_404(queryset, slug=lookup_value)
