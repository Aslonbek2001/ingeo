from parts.models import Carousel
from parts.serializers import CarouselSerializer
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from drf_spectacular.utils import extend_schema
from core.pagination import CustomPageNumberPagination

@extend_schema(tags=["Carousels"])
class CarouselViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter]
    serializer_class = CarouselSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = [
        "title_uz", "title_ru", "title_en",
    ]
    
    def get_queryset(self):
        """
        Auth user -> barcha carousel
        Anonymous -> faqat status=True
        """
        qs = Carousel.objects.only(
            "id",
            "title_uz", "title_ru", "title_en",
            "description_uz", "description_ru", "description_en",
            "image", "link", "position", "status"
        ).order_by("position")

        
        if not self.request.user.is_authenticated:
            qs = qs.filter(status=True)
        return qs

    def get_serializer_class(self):
        return CarouselSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()) 
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)