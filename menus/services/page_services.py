# pages/services/page_service.py
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from menus.models import Page, PageImages, Employee, PageFiles


class PageService:
    """Page obyektlari bilan ishlovchi biznes-logika."""
    
    @staticmethod
    def get_all_pages():
        """Barcha page obyektlarini qaytaradi (prefetch bilan tezlashtirilgan)."""
        return Page.objects.select_related("menu").only(
            "id", "title", "slug", "status", "menu", "type"
        )
    
    @staticmethod
    def create_page(validated_data):
        """Yangi sahifa yaratadi."""
        return Page.objects.create(**validated_data)

    @staticmethod
    def get_page_by_slug_for_users(slug: str):
        queryset = Page.objects.prefetch_related(
            Prefetch("images", queryset=PageImages.objects.only("id", "image", "page_id")),
            Prefetch("employees", queryset=Employee.objects.only(
                "id", "full_name", "position", "order", "image", "email", "phone", "status"
            )),
            Prefetch("files", queryset=PageFiles.objects.only("id", "title", "file", "page_id", "status")),
        ).only(
            "id", "title", "slug", "status", "description", "type",
            "title_uz", "title_ru", "title_en",
            "description_uz", "description_ru", "description_en"
        )

        # Faqat faol sahifalarni topamiz
        page = get_object_or_404(queryset, slug=slug, status=True)
        return page
    

    
