from rest_framework import generics, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.db.models import Prefetch
from .base import BaseMenuView
from menus.models import Menu
from menus.serializers.menu_serializers import MenuReadSerializer, MenuWriteSerializer


@extend_schema(
    tags=["Navbar and Menu"],
    summary="List and Create Menus",
    description=(
        "GET → Navbar’ni ichma-ich (nested) holda qaytaradi.\n"
        "POST → Yangi menyu qo‘shish imkonini beradi."
    ),
)
class MenuListCreateAPIView(BaseMenuView, generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuWriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        menu = serializer.save()

        read_serializer = MenuReadSerializer(menu, context={"request": request})
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=["Navbar and Menu"],
    summary="Retrieve, Update, or Delete Menu",
    description=(
        "GET → Bitta menyuni olish\n"
        "PUT/PATCH → Menyuni yangilash\n"
        "DELETE → Menyuni o‘chirish"
    ),
)
class MenuDetailAPIView(BaseMenuView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuWriteSerializer
    lookup_field = "id"
    lookup_url_kwarg = "menu_id"

    def get_queryset(self):
        return (
            Menu.objects.select_related("parent", "page")
            .prefetch_related(
                Prefetch(
                    "children",
                    queryset=Menu.objects.select_related("page").order_by("position")
                )
            )
            .order_by("position")
        )

    def update(self, request, *args, **kwargs):
        """Update dan keyin ham MenuReadSerializer bilan javob qaytaradi"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        menu = serializer.save()

        read_serializer = MenuReadSerializer(menu, context={"request": request})
        return Response(read_serializer.data, status=status.HTTP_200_OK)
