from django.db import transaction
from menus.models import Menu, Page


class MenuService:
    """Menu va Page orasidagi biznes-logika"""

    @staticmethod
    @transaction.atomic
    def create_menu(validated_data):
        has_page = validated_data.get('has_page', False)
        page_slug = validated_data.pop('page_slug', None)
        page_type = validated_data.pop('page_type', None)
        menu = Menu.objects.create(**validated_data)

        if has_page:
            if not page_type:
                page_type = 'page'
            MenuService._create_or_update_page(menu, page_slug, page_type)

        return Menu.objects.select_related("page").get(id=menu.id)

    @staticmethod
    @transaction.atomic
    def update_menu(instance, validated_data):
        has_page = validated_data.get('has_page', instance.has_page)
        page_slug = validated_data.pop('page_slug', None)
        page_type = validated_data.pop('page_type', None)

        # Menuni yangilash
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Page logikasi
        if has_page:
            if not page_type:
                page_type = 'page'
            MenuService._create_or_update_page(instance, page_slug, page_type=page_type)
        else:
            MenuService._delete_page_if_exists(instance)

        return Menu.objects.select_related("page").get(id=instance.id)

    # ======= Private yordamchi metodlar =======

    @staticmethod
    def _create_or_update_page(menu, slug, page_type):
        """Agar Page mavjud bo‘lsa — yangilaydi, bo‘lmasa yaratadi"""
        if not slug:
            raise ValueError("Page slug bo‘sh bo‘lishi mumkin emas")

        if hasattr(menu, 'page'):
            page = menu.page
            page.title = menu.title
            page.title_ru = menu.title_ru
            page.title_en = menu.title_en
            page.slug = slug
            page.type = page_type
            page.save()
        else:
            Page.objects.create(
                title=menu.title,
                title_ru=menu.title_ru,
                title_en=menu.title_en,
                is_menu_page=True,
                slug=slug,
                menu=menu,
                type=page_type,
                status=True
            )

    @staticmethod
    def _delete_page_if_exists(menu):
        """Agar Page mavjud bo‘lsa — o‘chiradi"""
        if hasattr(menu, 'page'):
            menu.page.delete()
