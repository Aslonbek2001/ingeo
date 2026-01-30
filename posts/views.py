from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from .models import Post, PostImages
from .serializers import (
    PostImageSerializer,
    PostManageListSerializer,
    PostManageSerializer,
)
from core.pagination import CustomPageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch


@extend_schema(tags=["News & Announcements"])
class PostManageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "type"]
    search_fields = ["title_uz", "title_ru", "title_en"]
    ordering_fields = ["published_date", "id"]
    ordering = ["-published_date"]

    def get_queryset(self):
        qs = Post.objects.prefetch_related(
            "pages",
            Prefetch("images", queryset=PostImages.objects.all())
        ).order_by("-published_date")

        # Agar user ro‘yxatdan o‘tmagan bo‘lsa
        if not self.request.user.is_authenticated:
            qs = qs.filter(status=True)

        return qs

    def get_serializer_class(self):
        if self.action == "list":
            return PostManageListSerializer
        return PostManageSerializer


# ✅ Swagger uchun path parameterni aniqlab beramiz
@extend_schema(
    tags=["News & Announcements - Images"],
    parameters=[
        OpenApiParameter(
            name="post_pk",
            description="Parent Post ID",
            required=True,
            type=OpenApiTypes.INT,  # 👈 shu joy ogohlantirishni yo‘qotadi
            location=OpenApiParameter.PATH,
        )
    ],
)
class PostImageViewSet(viewsets.ModelViewSet):
    serializer_class = PostImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return PostImages.objects.none()
        post_id = self.kwargs.get("post_pk")  # url dan keladi
        if self.request.user.is_authenticated:
            post = get_object_or_404(Post, id=post_id)
        else:
            post = get_object_or_404(Post, id=post_id, status=True)
        return post.images.all()


    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_pk")
        post = get_object_or_404(Post, id=post_id)
        serializer.save(post=post)
