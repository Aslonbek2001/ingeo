from parts.models import Application
from parts.serializers import ApplicationSerializer
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, SAFE_METHODS
from drf_spectacular.utils import extend_schema
from core.pagination import CustomPageNumberPagination


class ApplicationPermission(BasePermission):
    """
        Allow only anonymous users to create and authenticated users to read.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        if request.method == "POST":
            return not request.user.is_authenticated
        if request.method == "DELETE":
            return request.user.is_authenticated
        return False


@extend_schema(tags=["Applications"])
class ApplicationViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter]
    serializer_class = ApplicationSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [ApplicationPermission]
    search_fields = [
        "name", "phone", "message",
    ]
    
    def get_queryset(self):
        """
        Auth user -> barcha application
        Anonymous -> hech narsa ko'ra olmaydi
        """
        qs = Application.objects.only(
            "id",
            "name", "phone", "message", "submitted_at"
        ).order_by("-submitted_at")

        
        if not self.request.user.is_authenticated:
            qs = qs.none()
        return qs

    def get_serializer_class(self):
        return ApplicationSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()) 
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
