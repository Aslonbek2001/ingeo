from django.db.models import Prefetch
from menus.models import Menu
from menus.serializers.menu_serializers import MenuReadSerializer, MenuWriteSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from core.pagination import CustomPageNumberPagination


class BaseMenuView:
    """
    Menu uchun umumiy konfiguratsiya:
    - serializerlarni avtomatik tanlaydi
    - permission’larni o‘rnatadi
    - querysetni optimallashtiradi
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    # pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return MenuReadSerializer
        return MenuWriteSerializer

    def get_queryset(self):
        """
        Auth → barcha menyular
        Anonymous → faqat status=True
        """
        base_qs = Menu.objects.only(
            "id", "title_uz", "title_ru", "title_en", "status", "position", "parent"
        ).filter(parent__isnull=True)

        # Prefetch bolalar menyularini oldindan olish
        base_qs = base_qs.prefetch_related(
            Prefetch(
                "children",
                queryset=Menu.objects.only(
                    "id", "title_uz", "title_ru", "title_en", "status", "position", "parent"
                ).order_by("position")
            )
        )

        if not self.request.user.is_authenticated:
            base_qs = base_qs.filter(status=True)

        return base_qs.order_by("position")
