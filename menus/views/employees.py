from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from menus.models import Employee
from menus.serializers.employee_serializers import (
    EmployeeListSerializer, EmployeeDetailSerializer
)
from core.pagination import CustomPageNumberPagination
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Employees"])
class EmployeeListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # SEARCH + ORDERING
    search_fields = ['full_name', 'position', 'phone', 'email']
    ordering_fields = ['order', 'full_name', 'id']
    ordering = ('order', 'full_name')

    # FILTERLAR
    filterset_fields = {
        'status': ['exact'],
        'order': ['exact', 'gte', 'lte'],
        'pages__id': ['exact', 'in'],   # <— BU ENG TO‘G‘RISI!
    }

    def get_queryset(self):
        queryset = Employee.objects.all()

        # Agar frontchi ?page_id=5 deb yuborsa — ham ishlatamiz
        page_id = self.request.query_params.get('page_id') or self.request.query_params.get('pages__id')
        if page_id:
            try:
                # Bir nechta id: 1,5,10
                ids = [int(x) for x in page_id.split(',') if x.isdigit()]
                if ids:
                    queryset = queryset.filter(pages__id__in=ids)
            except:
                pass  # xato bo‘lsa ignore qilamiz

        return queryset.distinct()  # <— MUHIM! duplicate bo‘lmasin

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EmployeeDetailSerializer
        return EmployeeListSerializer

    
@extend_schema(tags=["Employees"])
class EmployeeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'
