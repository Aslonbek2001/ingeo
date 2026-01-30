from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend, filters
from rest_framework import generics, status
from menus.services.page_services import PageService
from menus.models import Page
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from core.pagination import CustomPageNumberPagination
from menus.serializers.page_serializers import (
    PageDetailSerializerForUsers, PageListSerializer, 
    PageSerializer, PageListSerializerForUsers
)


@extend_schema( tags=["Users - Page"])
class PageDetailForUsers(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PageDetailSerializerForUsers
    def get(self, request, slug):
        page = PageService.get_page_by_slug_for_users(slug)
        serializer = self.serializer_class(page)
        return Response(serializer.data, status=status.HTTP_200_OK)




# ===============================
# 📋 ADMIN - Page List & Create
# ===============================
@extend_schema(
    tags=["Admin - Page"],
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
class PageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Page.objects.filter(type="page")
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "menu", "title", "type"]
    serializer_class = PageSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Page.objects.filter(type="page", status=True)
        return Page.objects.filter(type="page")

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PageListSerializer
        return PageSerializer


@extend_schema(
    tags=["Admin - Page"],
    summary="Retrieve, Update, or Delete a Page",
    description="Retrieve, partially update, or delete a specific page by slug.",
)
class PageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Page.objects.filter(type="page", status=True)
        return Page.objects.filter(type="page")



@extend_schema(tags=["All Pages for Selection"])
class AllPagesForSelection(generics.ListAPIView):
    queryset = Page.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["title_uz", "title_ru", "title_en"]  
    search_fields = ["id", "^title_uz", "^title_ru", "^title_en"]
    serializer_class = PageListSerializerForUsers

    def get_queryset(self):
        # Use .only() to fetch only required fields, reducing data transfer
        qs = Page.objects.only("id", "title_uz", "title_ru", "title_en")
        # Add index check for optimization (ensure indexes exist in model)
        if getattr(self, "swagger_fake_view", False):
            return Page.objects.none()  # For schema generation
        return qs



